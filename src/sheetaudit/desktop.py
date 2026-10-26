"""Offline desktop interface; workers never access Tk widgets or send document data."""
import json
import os
import queue
import sys
import threading
import uuid
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from . import __version__
from .cli import build_parser, collect, read_json, run
from .privacy import private_summary
from .i18n import translate, check_language, load_language, save_language


class LocalizedStringVar(tk.StringVar):
    """Keep the application message, so switching never translates customer input."""
    def __init__(self, language, value=""):
        self.language = language
        self.original = value
        super().__init__(value=translate(value, language()))

    def set(self, value):
        self.original = value
        super().set(translate(value, self.language()))

    def refresh(self):
        super().set(translate(self.original, self.language()))


def sample_directory():
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "samples"
    return Path(__file__).resolve().parents[2] / "examples" / "pdfs"


def default_output_directory():
    """Keep portable reports beside the program, including when the folder moves."""
    if getattr(sys, "frozen", False):
        app_directory = Path(sys.executable).resolve().parent
        if app_directory.name == "程序":
            return app_directory.parent / "输出报告"  # Preserve existing installations.
        base = app_directory.parent if app_directory.name.lower() == "program" else app_directory
        return base / "reports"
    return Path.home() / "Documents" / "SheetAudit Reports"


def new_output(parent, kind="audit"):
    if not str(parent).strip():
        raise ValueError("请先选择报告保存位置")
    return Path(parent).expanduser().resolve() / (
        kind + "-" + datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6])


def audit_arguments(files, parent, tolerance="0.01", places="2", number_format="en", language="zh"):
    if str(places) not in ("0", "1", "2", "3", "4"):
        raise ValueError("小数位须在 0 到 4 之间")
    try:
        value = Decimal(tolerance)
    except InvalidOperation:
        raise ValueError("允许差额请填写数字，例如 0.01") from None
    if not value.is_finite() or not 0 <= value <= 1000:
        raise ValueError("允许差额须在 0 到 1000 之间")
    paths = collect(files)
    out = new_output(parent)
    return build_parser(language).parse_args(["audit", *map(str, paths), "--out", str(out),
        "--tolerance", str(value), "--decimal-places", str(places), "--number-format", number_format])


def review_arguments(extracted, corrections, source, parent, language="zh"):
    for label, raw, suffix in (("原提取记录", extracted, ".json"),
                               ("已保存的复核表", corrections, ".xlsx"),
                               ("原始 PDF", source, ".pdf")):
        path = Path(raw)
        if not raw.strip() or not path.is_file() or path.suffix.lower() != suffix:
            raise ValueError("请选择有效的" + label)
    return build_parser(language).parse_args(["review", extracted, "--corrections", corrections,
        "--source", source, "--out", str(new_output(parent, "review"))])


def execute_job(args, progress=None):
    code = run(args, progress=progress, announce=lambda text: None)
    return {"output": str(args.out), "code": code,
            "summary": private_summary(read_json(args.out / "summary.json"))}


class Desktop:
    def __init__(self, root, language=None, settings_path=None):
        self.root = root
        self.language = check_language(language or load_language(settings_path))
        self.settings_path = settings_path
        self.widget_messages = {}
        self.files = []
        self.output = None
        self.busy = False
        self.events = queue.Queue()
        self.locked = []
        self.review_docs = []
        self.source_lookup = {}
        root.title("SheetAudit · 本地单据核对")
        root.geometry("1000x800")
        root.minsize(940, 770)
        root.configure(bg="#f4f6fa")
        root.protocol("WM_DELETE_WINDOW", self.close)
        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("TFrame", background="#f4f6fa")
        style.configure("Card.TFrame", background="white")
        style.configure("TLabel", background="#f4f6fa", foreground="#25334b", font=("Microsoft YaHei UI", 10))
        style.configure("Title.TLabel", font=("Microsoft YaHei UI", 21, "bold"))
        style.configure("Sub.TLabel", foreground="#778399", font=("Microsoft YaHei UI", 9))
        style.configure("Card.TLabel", background="white")
        style.configure("CardTitle.TLabel", background="white", font=("Microsoft YaHei UI", 11, "bold"))
        style.configure("CardSub.TLabel", background="white", foreground="#778399", font=("Microsoft YaHei UI", 9))
        style.configure("TButton", font=("Microsoft YaHei UI", 10), padding=(12, 8),
                        background="#edf1f7", foreground="#40516b", relief="flat", borderwidth=0)
        style.map("TButton", background=[("active", "#e1e8f2"), ("disabled", "#f0f2f6")],
                  foreground=[("disabled", "#a6afbd")])
        style.configure("Primary.TButton", background="#3268dc", foreground="white")
        style.map("Primary.TButton", background=[("active", "#2457c4"), ("disabled", "#b6c8ec")],
                  foreground=[("disabled", "white")])
        style.configure("TEntry", padding=7, fieldbackground="#fafbfd", bordercolor="#e3e8ef", lightcolor="#e3e8ef", darkcolor="#e3e8ef")
        style.configure("TCombobox", padding=6, arrowsize=12)
        style.configure("TSpinbox", padding=6, arrowsize=12)
        style.configure("Horizontal.TProgressbar", background="#3268dc", troughcolor="#e5eaf2", borderwidth=0)
        outer = ttk.Frame(root, padding=(24, 18))
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(2, weight=1)
        head = ttk.Frame(outer)
        head.grid(row=0, column=0, sticky="ew")
        ttk.Label(head, text="SheetAudit", style="Title.TLabel").pack(side="left")
        ttk.Label(head, text="单据核对  ·  本地运行", style="Sub.TLabel").pack(side="left", padx=16, pady=(8, 0))
        ttk.Button(head, text="使用说明", command=self.help).pack(side="right")
        self.language_choice = tk.StringVar()
        self.language_selector = ttk.Combobox(head, textvariable=self.language_choice,
            values=("English", "简体中文"), width=10, state="readonly")
        self.language_selector.pack(side="right", padx=(6, 12))
        self.language_selector.bind("<<ComboboxSelected>>", self.switch_language)
        ttk.Label(head, text="语言", style="Sub.TLabel").pack(side="right")
        nav = ttk.Frame(outer)
        nav.grid(row=1, column=0, sticky="w", pady=(16, 12))
        self.module_buttons = {}
        for index, label in enumerate(("新建核对", "人工核算")):
            b = tk.Button(nav, text=label, width=14, height=1, font=("Microsoft YaHei UI", 10),
                bd=0, relief="flat", highlightthickness=0, padx=0, pady=9,
                cursor="hand2", command=lambda i=index: self.show_page(i))
            b.grid(row=0, column=index, padx=(0, 6))
            self.module_buttons[index] = b
        # Both pages occupy the same fixed host. Child requests never resize it.
        self.page_host = ttk.Frame(outer, style="Card.TFrame", width=1, height=1)
        self.page_host.grid(row=2, column=0, sticky="nsew")
        self.page_host.grid_propagate(False)
        self.page_host.rowconfigure(0, weight=1)
        self.page_host.columnconfigure(0, weight=1)
        self.audit_tab = ttk.Frame(self.page_host, style="Card.TFrame", padding=18)
        self.review_tab = ttk.Frame(self.page_host, style="Card.TFrame", padding=18)
        for page in (self.audit_tab, self.review_tab):
            page.grid(row=0, column=0, sticky="nsew")
        self.parent = tk.StringVar(value=str(default_output_directory()))
        self.tolerance = tk.StringVar(value="0.01")
        self.places = tk.StringVar(value="2")
        self.number_format = tk.StringVar(value="1,234.56")
        self.status = LocalizedStringVar(lambda: self.language, value="准备就绪，可先加载样例体验。")
        self.stats = LocalizedStringVar(lambda: self.language, value="生成报告后，在这里查看处理结果。")
        self.build_audit()
        self.build_review()
        save = ttk.Frame(outer, style="Card.TFrame", padding=(18, 12))
        save.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        ttk.Label(save, text="保存位置", style="CardSub.TLabel").pack(anchor="w", pady=(0, 6))
        pathrow = ttk.Frame(save, style="Card.TFrame")
        pathrow.pack(fill="x")
        entry = ttk.Entry(pathrow, textvariable=self.parent)
        entry.pack(side="left", fill="x", expand=True)
        self.locked.append(entry)
        self.button(pathrow, "选择位置", self.choose_parent, width=10).pack(side="left", padx=8)
        self.action_button = self.button(pathrow, "生成报告", self.start_audit, style="Primary.TButton", width=15)
        self.action_button.pack(side="left")
        bottom = ttk.Frame(outer, style="Card.TFrame", padding=(18, 12), height=104)
        bottom.grid(row=4, column=0, sticky="ew", pady=(10, 0))
        bottom.pack_propagate(False)
        ttk.Label(bottom, textvariable=self.stats, style="Card.TLabel").pack(anchor="w")
        actions = ttk.Frame(bottom, style="Card.TFrame")
        actions.pack(fill="x", pady=(8, 0))
        self.report_button = ttk.Button(actions, text="打开报告", width=12, command=lambda: self.open_result("report.xlsx"), state="disabled")
        self.report_button.pack(side="left")
        self.folder_button = ttk.Button(actions, text="打开文件夹", width=12, command=lambda: self.open_result(), state="disabled")
        self.folder_button.pack(side="left", padx=8)
        ttk.Button(actions, text="查看复核表", width=12, command=self.select_review).pack(side="left")
        self.progress = ttk.Progressbar(outer, mode="determinate", length=100)
        self.progress.grid(row=5, column=0, sticky="ew", pady=(12, 6), ipady=0)
        self.progress.configure(style="Horizontal.TProgressbar")
        footer = ttk.Frame(outer)
        footer.grid(row=6, column=0, sticky="ew")
        footer.columnconfigure(0, weight=1)
        ttk.Label(footer, textvariable=self.status, style="Sub.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(footer, text="仅本机处理  ·  " + __version__, style="Sub.TLabel").grid(row=0, column=1, sticky="e")
        self.show_page(0)
        self.capture_messages(root)
        self.apply_language(self.language, persist=False)
        root.after(100, self.poll)

    def tr(self, message):
        return translate(message, self.language)

    def capture_messages(self, parent):
        for widget in parent.winfo_children():
            keys = widget.keys()
            if "text" in keys and not ("textvariable" in keys and str(widget.cget("textvariable"))):
                self.widget_messages[widget] = str(widget.cget("text"))
            self.capture_messages(widget)

    def text(self, widget, message):
        self.widget_messages[widget] = message
        widget.configure(text=self.tr(message))

    def apply_language(self, language, persist=True):
        self.language = check_language(language)
        self.language_choice.set("English" if language == "en" else "简体中文")
        self.root.title(self.tr("SheetAudit · 本地单据核对"))
        for widget, message in self.widget_messages.items():
            widget.configure(text=self.tr(message))
            if isinstance(widget, ttk.Label) and len(self.tr(message)) > 75:
                widget.configure(wraplength=850)
        self.status.refresh()
        self.stats.refresh()
        self.show_page(self.current_page)
        if persist:
            save_language(language, self.settings_path)

    def switch_language(self, event=None):
        if not self.busy:
            self.apply_language("en" if self.language_choice.get() == "English" else "zh")

    def message(self, kind, title, message, **options):
        options.setdefault("parent", self.root)
        return getattr(messagebox, kind)(self.tr(title), self.tr(message), **options)

    def button(self, parent, text, command, **kw):
        b = ttk.Button(parent, text=text, command=command, **kw)
        self.locked.append(b)
        return b

    def build_audit(self):
        self.audit_tab.columnconfigure(0, weight=1)
        self.audit_tab.rowconfigure(2, weight=1)
        title = ttk.Frame(self.audit_tab, style="Card.TFrame")
        title.grid(row=0, column=0, sticky="ew")
        ttk.Label(title, text="选择 PDF 单据", style="CardTitle.TLabel").pack(side="left")
        ttk.Label(title, text="文字型 PDF · 一份一单 · 最多 100 份", style="CardSub.TLabel").pack(side="right")
        row = ttk.Frame(self.audit_tab, style="Card.TFrame")
        row.grid(row=1, column=0, sticky="ew", pady=(12, 10))
        for text, command in (("添加 PDF", self.add_files), ("添加文件夹", self.add_folder),
                              ("加载样例", self.load_samples), ("移除选中", self.remove_files)):
            self.button(row, text, command, width=14).pack(side="left", padx=(0, 8))
        files = ttk.Frame(self.audit_tab, style="Card.TFrame")
        files.grid(row=2, column=0, sticky="nsew")
        self.listbox = tk.Listbox(files, height=4, selectmode="extended", font=("Microsoft YaHei UI", 10),
            bg="#fafbfd", fg="#40516b", relief="flat", highlightthickness=1, highlightbackground="#e6ebf2",
            selectbackground="#e1ebff", selectforeground="#2457c4", activestyle="none", bd=8)
        scroll = ttk.Scrollbar(files, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.listbox.pack(fill="both", expand=True)
        policy = ttk.Frame(self.audit_tab, style="Card.TFrame")
        policy.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        ttk.Label(policy, text="允许差额", style="CardSub.TLabel").pack(side="left")
        t = ttk.Entry(policy, textvariable=self.tolerance, width=8)
        t.pack(side="left", padx=(8, 18))
        self.locked.append(t)
        ttk.Label(policy, text="小数位", style="CardSub.TLabel").pack(side="left")
        ttk.Spinbox(policy, from_=0, to=4, width=4, textvariable=self.places, state="readonly").pack(side="left", padx=(8, 18))
        ttk.Label(policy, text="数字格式", style="CardSub.TLabel").pack(side="left")
        ttk.Combobox(policy, values=("1,234.56", "1.234,56"), textvariable=self.number_format, width=12, state="readonly").pack(side="left", padx=8)
        ttk.Label(self.audit_tab, text="差额大于容差才标记；严格一致填 0。扫描件需要转换或人工录入。", style="CardSub.TLabel").grid(row=4, column=0, sticky="w", pady=(8, 0))

    def build_review(self):
        ttk.Label(self.review_tab, text="人工核算", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(self.review_tab, text="修改并保存复核表，再选择对应原件重新核算。", style="CardSub.TLabel").pack(anchor="w", pady=(6, 10))
        batch = ttk.Frame(self.review_tab, style="Card.TFrame")
        batch.pack(fill="x", pady=(0, 8))
        self.doc_choice = ttk.Combobox(batch, state="readonly")
        self.doc_choice.pack(side="left", fill="x", expand=True)
        self.doc_choice.bind("<<ComboboxSelected>>", self.use_document)
        self.button(batch, "打开复核表", self.open_review, width=11).pack(side="left", padx=(8, 0))
        self.extracted = tk.StringVar()
        self.corrections = tk.StringVar()
        self.source = tk.StringVar()
        for title, var, pattern in (("提取记录  ·  extracted.json", self.extracted, "*.json"),
                                    ("已保存的复核表  ·  review.xlsx", self.corrections, "*.xlsx"),
                                    ("原始 PDF", self.source, "*.pdf")):
            ttk.Label(self.review_tab, text=title, style="CardSub.TLabel").pack(anchor="w", pady=(6, 4))
            row = ttk.Frame(self.review_tab, style="Card.TFrame")
            row.pack(fill="x")
            e = ttk.Entry(row, textvariable=var)
            e.pack(side="left", fill="x", expand=True)
            self.locked.append(e)
            self.button(row, "选择文件", lambda v=var, p=pattern: self.pick(v, p), width=11).pack(side="left", padx=(8, 0))
        ttk.Label(self.review_tab, text="请填写实际复核签注。未知值留空，原件须匹配；修改报告快照不会重算。", style="CardSub.TLabel").pack(anchor="w", pady=(10, 0))

    def show_page(self, index):
        self.current_page = index
        (self.audit_tab if index == 0 else self.review_tab).tkraise()
        for i, button in self.module_buttons.items():
            button.configure(bg="white" if i == index else "#e9edf4",
                             fg="#3268dc" if i == index else "#778399",
                             activebackground="white", activeforeground="#3268dc")
        self.text(self.action_button, "生成报告" if index == 0 else "重新核算")
        self.action_button.configure(command=self.start_audit if index == 0 else self.start_review)

    def pick(self, var, pattern):
        value = filedialog.askopenfilename(parent=self.root, filetypes=[(self.tr("所需文件"), pattern)])
        if value:
            var.set(value)

    def choose_parent(self):
        value = filedialog.askdirectory(parent=self.root, title=self.tr("选择报告保存位置"))
        if value:
            self.parent.set(value)

    def add(self, paths):
        combined = list(dict.fromkeys([*self.files, *(str(Path(p).resolve()) for p in paths)]))
        if len(combined) > 100:
            self.message("showwarning", "单批数量限制", "每批最多 100 份 PDF，请分批处理。", parent=self.root)
            return
        self.files = combined
        self.listbox.delete(0, "end")
        for i, p in enumerate(self.files, 1):
            self.listbox.insert("end", f"{i:02d}   {Path(p).name}")
        self.status.set(f"已选择 {len(self.files)} 份 PDF。")

    def add_files(self):
        self.add(filedialog.askopenfilenames(parent=self.root, filetypes=[(self.tr("PDF 单据"), "*.pdf")]))

    def add_folder(self):
        path = filedialog.askdirectory(parent=self.root)
        if path:
            try:
                self.add(collect([path]))
            except ValueError as exc:
                self.message("showwarning", "无法添加", str(exc), parent=self.root)

    def load_samples(self):
        paths = sorted(sample_directory().glob("*.pdf"))
        if not paths:
            self.message("showerror", "样例未找到", "请保留程序的完整文件夹，或手动添加 PDF。", parent=self.root)
            return
        if self.files and not self.message("askyesno", "替换当前列表？", "将清空当前选择并加载合成样例。原文件不变。", parent=self.root):
            return
        self.files = []
        self.add(paths)
        self.status.set("已加载合成样例，含预设差异、扫描件和不支持版式，用于演示提示。")

    def remove_files(self):
        selected = set(self.listbox.curselection())
        remaining = [p for i, p in enumerate(self.files) if i not in selected]
        self.files = []
        self.add(remaining)

    def start_audit(self):
        if self.busy:
            return
        try:
            args = audit_arguments(self.files, self.parent.get(), self.tolerance.get(),
                self.places.get(), "de" if self.number_format.get() == "1.234,56" else "en", self.language)
        except (ValueError, OSError) as exc:
            self.message("showwarning", "请检查输入", str(exc), parent=self.root)
            return
        self.source_lookup = {str(Path(p).resolve()): p for p in self.files}
        self.begin(args)

    def start_review(self):
        if self.busy:
            return
        try:
            args = review_arguments(self.extracted.get(), self.corrections.get(), self.source.get(), self.parent.get(), self.language)
        except (ValueError, OSError) as exc:
            self.message("showwarning", "请检查复核文件", str(exc), parent=self.root)
            return
        self.source_lookup = {str(Path(self.source.get()).resolve()): self.source.get()}
        self.begin(args)

    def begin(self, args):
        self.busy = True
        self.language_selector.configure(state="disabled")
        for widget in self.locked:
            widget.configure(state="disabled")
        self.report_button.configure(state="disabled")
        self.folder_button.configure(state="disabled")
        self.output = None
        self.progress["value"] = 0
        self.stats.set("正在本机处理，请稍候。")
        self.status.set("正在准备……")
        threading.Thread(target=self.worker, args=(args,), daemon=True).start()

    def worker(self, args):
        try:
            result = execute_job(args, lambda n, total, text: self.events.put(("progress", (n, total, text))))
            self.events.put(("done", result))
        except Exception as exc:
            # No document text or raw tracebacks in alerts or persistent logs.
            message = str(exc) if type(exc) is ValueError else "处理未完成。请检查文件权限、PDF 是否加密、复核文件及保存位置后重试。"
            self.events.put(("error", message))

    def poll(self):
        try:
            while True:
                kind, data = self.events.get_nowait()
                if kind == "progress":
                    n, total, text = data
                    self.progress["value"] = min(90, n / max(total, 1) * 90)
                    self.status.set(f"{text}  {n}/{total}" if total else text)
                else:
                    self.busy = False
                    self.language_selector.configure(state="readonly")
                    for widget in self.locked:
                        widget.configure(state="normal")
                    if kind == "error":
                        self.stats.set("处理未完成，请检查提示后重试。")
                        self.status.set(data)
                        self.message("showerror", "处理未完成", data, parent=self.root)
                    else:
                        self.output = Path(data["output"])
                        s = data["summary"]
                        self.stats.set(f"成功 {s['documents']} 份  ·  失败 {s['failed']} 份  ·  明细 {s['items']} 行  ·  差异 {s['differences']} 处  ·  无法核验 {s['uncheckable']} 项  ·  待复核 {s['open_notices']} 项")
                        self.status.set("报告已生成，请查看差异及待复核提示。" + (" 部分文件失败，请在报告错误清单中查看。" if s["failed"] else ""))
                        self.progress["value"] = 100
                        self.report_button.configure(state="normal")
                        self.folder_button.configure(state="normal")
                        self.populate_review()
        except queue.Empty:
            pass
        self.root.after(100, self.poll)

    def populate_review(self):
        self.review_docs = sorted((self.output / "documents").glob("*/extracted.json"))
        labels = []
        for p in self.review_docs:
            try:
                d = read_json(p)
                labels.append(p.parent.name + "  ·  " + d["source"].get("file", "单据"))
            except (ValueError, KeyError, OSError):
                labels.append(p.parent.name)
        self.doc_choice.configure(values=labels)
        if labels:
            self.doc_choice.current(0)
            self.use_document()
        else:
            self.doc_choice.set("")
            for v in (self.extracted, self.corrections, self.source):
                v.set("")

    def use_document(self, event=None):
        idx = self.doc_choice.current()
        if idx < 0 or idx >= len(self.review_docs):
            return
        p = self.review_docs[idx]
        self.extracted.set(str(p))
        self.corrections.set(str(p.with_name("review.xlsx")))
        # Bind only to a source chosen in this session; never open a path from JSON.
        self.source.set("")
        d = read_json(p)
        name = d["source"].get("file", "")
        matches = [v for v in self.source_lookup.values() if Path(v).name == name]
        if len(matches) == 1:
            self.source.set(matches[0])

    def select_review(self):
        self.show_page(1)

    def open_path(self, path):
        try:
            if not path.exists():
                raise OSError()
            os.startfile(str(path))
        except OSError:
            self.message("showwarning", "无法打开", "请确认文件存在，并安装可打开 Excel 的应用；也可在文件夹中手动打开。", parent=self.root)

    def open_result(self, name=None):
        if self.output:
            self.open_path(self.output / name if name else self.output)

    def open_review(self):
        if self.corrections.get():
            self.open_path(Path(self.corrections.get()))

    def close(self):
        if self.busy:
            self.message("showinfo", "正在处理", "请等待当前批次完成后再关闭，以免中断报告写入。", parent=self.root)
        else:
            self.root.destroy()

    def help(self):
        self.message("showinfo", "使用说明", "1. 添加 PDF 或加载合成样例。\n2. 选择保存位置，点击生成报告。\n3. 查看差异、无法核验项和待复核提示。\n4. 如需修正，编辑 review.xlsx 并保存。\n5. 在“人工核算”中选择原件和复核表，点击重新核算。\n\n默认容差 0.01；差异大于容差才标记。缺值不等于零。\n算术一致不代表单据完整、真实或可以付款。\n文件本机处理，输出不加密，不自动上传或删除。", parent=self.root)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="SheetAudit desktop / SheetAudit 桌面程序")
    parser.add_argument("--language", choices=("en", "zh"), default=None)
    args = parser.parse_args()
    root = tk.Tk()
    Desktop(root, language=args.language)
    root.mainloop()


if __name__ == "__main__":
    main()

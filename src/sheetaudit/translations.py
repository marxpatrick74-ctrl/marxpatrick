"""English presentation catalog. Keys retain the legacy Chinese record vocabulary.

Only application-owned messages are translated. Source evidence is never translated.
"""

ENGLISH = {'待人工复核': 'Awaiting human review',
 '容差须为 0–1000 的有限数；小数位须为 0–4': 'Tolerance must be finite and between 0 and 1000; decimal places must be 0-4',
 '明细原金额合计→小计': 'Sum of stated line amounts -> subtotal',
 '小计+税额−折扣+运费→总计': 'Subtotal + tax - discount + shipping -> total',
 '数据已变化或旧版签注，需重新复核（非自动批准）': 'Data changed or legacy sign-off; review again (not payment approval)',
 '数量×单价': 'Quantity x unit price',
 '先按指定小数位四舍五入；差异=原金额−计算金额。行级折扣/税额须人工确认。': 'Round to the selected precision first; difference = stated - '
                                          'calculated. Confirm line discounts/taxes manually.',
 '含未解析金额或零行时不核验；提取完整性仍需人工确认。': 'Not checked with missing amounts or zero lines. Confirm extraction coverage '
                               'manually.',
 '缺失税/折扣/运费不擅自按 0 处理；可人工确认后在修正 JSON 中填 0。': 'Missing tax/discount/shipping is not zero. Enter zero in '
                                            'corrections only after human confirmation.',
 '确认币种及当前金额小数位是否适用': 'Confirm the currency and selected decimal precision',
 '零条明细，不能得出单据无差异结论': 'No line items: the document cannot be declared free of discrepancies',
 '局部复核已记录，完整性未确认（非自动批准）': 'Partial review recorded; coverage unconfirmed (not payment approval)',
 '无法核验': 'Uncheckable',
 '缺少关键字段 {0}': 'Missing required field {0}',
 '复核已记录，仍有待处理项（非自动批准）': 'Review recorded; unresolved items remain (not payment approval)',
 '本次复核完成（非自动批准）': 'Review complete for this version (not payment approval)',
 '差异': 'Difference',
 '算术一致': 'Consistent',
 '数据集必须声明为 synthetic 或 authorized_real': 'Declare dataset_type as synthetic or authorized_real',
 '验证集须包含 1–100 个已标注案例': 'The benchmark requires 1-100 annotated cases',
 '人工标注必须包含全部字段，未知为 null': 'Ground truth must include every field; use null for unknown values',
 '人工明细标注需要有效页码和名称': 'Ground-truth items require a valid page and description',
 'JSON 超过 20 MB': 'JSON exceeds 20 MB',
 '单批须包含 1–100 个 PDF；目录只扫描一层': 'A batch requires 1-100 PDFs; directories are scanned one level deep',
 'SheetAudit AI — 本地 PDF 提取与金额核对': 'SheetAudit AI - local PDF extraction and arithmetic checks',
 '提取 PDF 并生成 Excel/JSON 报告': 'Extract PDFs and generate Excel/JSON reports',
 'PDF 文件或目录': 'PDF files or directories',
 '已安装的 Ollama 本地模型名；不下载模型': 'An already installed local Ollama model; no model downloads',
 '只对少文字页面运行本地 Tesseract': 'Run local Tesseract only on pages with little readable text',
 '如 chi_sim+eng；须已安装语言包': 'For example chi_sim+eng; language packs must already be installed',
 '本机 Tesseract 可执行文件路径': 'Path to the local Tesseract executable',
 '应用人工修正，验证原 PDF 指纹，输出新版本': 'Apply human corrections, verify the source PDF and create a new result',
 '只输出匿名统计，不显示文件名、金额、原文或签注': 'Print counts only, without filenames, amounts, evidence or reviewer details',
 '包含 summary.json 的报告目录': 'Report directory containing summary.json',
 '对带人工标注和指纹的样本进行规则提取验证': 'Evaluate rules extraction against annotated, hash-bound samples',
 '新的验证结果 JSON 文件': 'A new benchmark result JSON file',
 '容差须为 0–1000 的有限十进制数': 'Tolerance must be a finite decimal between 0 and 1000',
 '输出目录已存在；请选择新目录以保留历史报告': 'Output directory already exists; choose a new directory to preserve prior reports',
 'Ollama 模式需要 --model 指定已安装本地模型': 'Ollama mode requires --model with an already installed local model',
 '报告已生成：成功 {0}，失败 {1}，差异 {2}，无法核验 {3}，待复核提示 {4}。': 'Report generated: processed {0}, failed {1}, differences '
                                                   '{2}, uncheckable {3}, open notices {4}.',
 '输出：report.xlsx；每份单据的 documents 子目录包含可编辑 review.xlsx。': 'Output: report.xlsx; each document folder contains '
                                                         'an editable review.xlsx.',
 '新的输出目录；拒绝覆盖已有目录': 'A new output directory; existing directories are never overwritten',
 '绝对差异≤容差视为算术一致（默认 0.01）': 'An absolute difference at or below tolerance is consistent (default 0.01)',
 '存在差异、无法核验或待复核提示时返回 1': 'Return 1 when differences, uncheckable checks or open notices remain',
 '验证结果文件已存在，请选择新文件': 'Benchmark output already exists; choose a new file',
 '正在核算并生成 Excel': 'Checking arithmetic and generating Excel',
 '参数、文件或 JSON schema 无效；请参照 README 和 review-template.json': 'Invalid arguments, file or JSON schema; see '
                                                            'README and review-template.json',
 '输入必须为现有 PDF 或包含 PDF 的目录': 'Inputs must be existing PDFs or directories containing PDFs',
 '正在读取和提取': 'Reading and extracting',
 '已完成提取': 'Extraction complete',
 'source.json 的来源指纹不符': 'The source.json fingerprint does not match',
 '读取/提取失败，请检查文件、PDF 加密或本地 OCR/模型依赖': 'Read/extraction failed; check the file, PDF encryption or local '
                                     'OCR/model dependencies',
 '批次内存在内容完全相同的 PDF；保留每份，避免误删合法记录': 'Identical PDFs occur in this batch; all copies are retained to preserve '
                                   'legitimate records',
 '核对': 'Audit',
 '输出报告': 'Reports',
 '请先选择报告保存位置': 'Choose a report output location first',
 '小数位须在 0 到 4 之间': 'Decimal places must be between 0 and 4',
 '允许差额须在 0 到 1000 之间': 'Tolerance must be between 0 and 1000',
 '原提取记录': 'original extraction record',
 '已保存的复核表': 'saved review workbook',
 '原始 PDF': 'Original PDF',
 'SheetAudit · 本地单据核对': 'SheetAudit - Local document audit',
 '生成报告': 'Generate report',
 '已选择 {0} 份 PDF。': 'Selected {0} PDF(s).',
 '已加载合成样例，含预设差异、扫描件和不支持版式，用于演示提示。': 'Synthetic examples loaded, including discrepancies, scans and '
                                    'unsupported layouts.',
 '正在本机处理，请稍候。': 'Processing locally. Please wait.',
 '正在准备……': 'Preparing...',
 '使用说明': 'Help',
 '1. 添加 PDF 或加载合成样例。\n2. 选择保存位置，点击生成报告。\n3. 查看差异、无法核验项和待复核提示。\n4. 如需修正，编辑 review.xlsx 并保存。\n5. 在“人工核算”中选择原件和复核表，点击重新核算。\n\n默认容差 0.01；差异大于容差才标记。缺值不等于零。\n算术一致不代表单据完整、真实或可以付款。\n文件本机处理，输出不加密，不自动上传或删除。': '1. '
                                                                                                                                                                                                       'Add '
                                                                                                                                                                                                       'PDFs '
                                                                                                                                                                                                       'or '
                                                                                                                                                                                                       'load '
                                                                                                                                                                                                       'the '
                                                                                                                                                                                                       'synthetic '
                                                                                                                                                                                                       'examples.\n'
                                                                                                                                                                                                       '2. '
                                                                                                                                                                                                       'Choose '
                                                                                                                                                                                                       'an '
                                                                                                                                                                                                       'output '
                                                                                                                                                                                                       'folder '
                                                                                                                                                                                                       'and '
                                                                                                                                                                                                       'click '
                                                                                                                                                                                                       'Generate '
                                                                                                                                                                                                       'report.\n'
                                                                                                                                                                                                       '3. '
                                                                                                                                                                                                       'Check '
                                                                                                                                                                                                       'differences, '
                                                                                                                                                                                                       'uncheckable '
                                                                                                                                                                                                       'items '
                                                                                                                                                                                                       'and '
                                                                                                                                                                                                       'open '
                                                                                                                                                                                                       'notices.\n'
                                                                                                                                                                                                       '4. '
                                                                                                                                                                                                       'To '
                                                                                                                                                                                                       'correct '
                                                                                                                                                                                                       'data, '
                                                                                                                                                                                                       'edit '
                                                                                                                                                                                                       'review.xlsx '
                                                                                                                                                                                                       'and '
                                                                                                                                                                                                       'save '
                                                                                                                                                                                                       'it.\n'
                                                                                                                                                                                                       '5. '
                                                                                                                                                                                                       'In '
                                                                                                                                                                                                       'Human '
                                                                                                                                                                                                       'review, '
                                                                                                                                                                                                       'select '
                                                                                                                                                                                                       'the '
                                                                                                                                                                                                       'original '
                                                                                                                                                                                                       'PDF '
                                                                                                                                                                                                       'and '
                                                                                                                                                                                                       'saved '
                                                                                                                                                                                                       'workbook, '
                                                                                                                                                                                                       'then '
                                                                                                                                                                                                       'click '
                                                                                                                                                                                                       'Recalculate.\n'
                                                                                                                                                                                                       '\n'
                                                                                                                                                                                                       'Default '
                                                                                                                                                                                                       'tolerance: '
                                                                                                                                                                                                       '0.01. '
                                                                                                                                                                                                       'Only '
                                                                                                                                                                                                       'larger '
                                                                                                                                                                                                       'differences '
                                                                                                                                                                                                       'are '
                                                                                                                                                                                                       'flagged. '
                                                                                                                                                                                                       'Unknown '
                                                                                                                                                                                                       'is '
                                                                                                                                                                                                       'not '
                                                                                                                                                                                                       'zero.\n'
                                                                                                                                                                                                       'Arithmetic '
                                                                                                                                                                                                       'agreement '
                                                                                                                                                                                                       'does '
                                                                                                                                                                                                       'not '
                                                                                                                                                                                                       'prove '
                                                                                                                                                                                                       'completeness, '
                                                                                                                                                                                                       'authenticity '
                                                                                                                                                                                                       'or '
                                                                                                                                                                                                       'permission '
                                                                                                                                                                                                       'to '
                                                                                                                                                                                                       'pay.\n'
                                                                                                                                                                                                       'Processing '
                                                                                                                                                                                                       'is '
                                                                                                                                                                                                       'local. '
                                                                                                                                                                                                       'Outputs '
                                                                                                                                                                                                       'are '
                                                                                                                                                                                                       'not '
                                                                                                                                                                                                       'encrypted, '
                                                                                                                                                                                                       'automatically '
                                                                                                                                                                                                       'uploaded '
                                                                                                                                                                                                       'or '
                                                                                                                                                                                                       'deleted.',
 '程序': 'program',
 '允许差额请填写数字，例如 0.01': 'Enter a numeric tolerance, for example 0.01',
 '新建核对': 'New audit',
 '人工核算': 'Human review',
 '准备就绪，可先加载样例体验。': 'Ready. Load examples to try an audit.',
 '生成报告后，在这里查看处理结果。': 'Processing results will appear here.',
 '打开报告': 'Open report',
 '打开文件夹': 'Open folder',
 '添加 PDF': 'Add PDFs',
 '添加文件夹': 'Add folder',
 '加载样例': 'Load examples',
 '移除选中': 'Remove selected',
 '提取记录  ·  extracted.json': 'Extraction record - extracted.json',
 '已保存的复核表  ·  review.xlsx': 'Saved workbook - review.xlsx',
 '选择报告保存位置': 'Choose a report output folder',
 '单批数量限制': 'Batch limit',
 '每批最多 100 份 PDF，请分批处理。': 'A batch supports up to 100 PDFs. Split larger batches.',
 '样例未找到': 'Examples not found',
 '请保留程序的完整文件夹，或手动添加 PDF。': 'Keep the complete program folder, or add PDFs manually.',
 '正在处理': 'Processing',
 '请等待当前批次完成后再关闭，以免中断报告写入。': 'Wait for this batch to finish before closing, so report writing is not '
                            'interrupted.',
 '请选择有效的': 'Select a valid ',
 '复核': 'Review',
 '选择位置': 'Browse',
 '打开复核表': 'Open review',
 '重新核算': 'Recalculate',
 '替换当前列表？': 'Replace the current list?',
 '将清空当前选择并加载合成样例。原文件不变。': 'Replace the selection with synthetic examples? Original files will not change.',
 '请检查输入': 'Check input',
 '请检查复核文件': 'Check review files',
 '处理未完成。请检查文件权限、PDF 是否加密、复核文件及保存位置后重试。': 'Processing did not finish. Check file permissions, PDF encryption, '
                                         'review files and the output folder.',
 '无法打开': 'Cannot open',
 '请确认文件存在，并安装可打开 Excel 的应用；也可在文件夹中手动打开。': 'Check the file and install an Excel-compatible application, or '
                                          'open it manually from its folder.',
 '单据核对  ·  本地运行': 'Document audit - local processing',
 '保存位置': 'Output folder',
 '查看复核表': 'Review files',
 '选择 PDF 单据': 'Select PDF documents',
 '文字型 PDF · 一份一单 · 最多 100 份': 'Text PDFs - one document per file - up to 100 files',
 '允许差额': 'Tolerance',
 '小数位': 'Decimals',
 '数字格式': 'Number format',
 '差额大于容差才标记；严格一致填 0。扫描件需要转换或人工录入。': 'Flag differences above tolerance; use 0 for exact agreement. Scans need '
                                    'OCR or manual input.',
 '修改并保存复核表，再选择对应原件重新核算。': 'Edit and save the review workbook, then select the matching original PDF to '
                          'recalculate.',
 '选择文件': 'Browse',
 '请填写实际复核签注。未知值留空，原件须匹配；修改报告快照不会重算。': 'Use a real human sign-off. Leave unknown values blank. Editing the '
                                      'report snapshot does not recalculate it.',
 '所需文件': 'Required files',
 '无法添加': 'Cannot add',
 '仅本机处理  ·  ': 'Local processing - ',
 'PDF 单据': 'PDF documents',
 '处理未完成，请检查提示后重试。': 'Processing did not finish. Check the message and retry.',
 '处理未完成': 'Processing incomplete',
 '成功 {0} 份  ·  失败 {1} 份  ·  明细 {2} 行  ·  差异 {3} 处  ·  无法核验 {4} 项  ·  待复核 {5} 项': 'Processed {0} | Failed {1} '
                                                                                 '| Lines {2} | Differences '
                                                                                 '{3} | Uncheckable {4} | '
                                                                                 'Open {5}',
 '单据': 'Document',
 '报告已生成，请查看差异及待复核提示。': 'Report generated. Check differences and open notices.',
 ' 部分文件失败，请在报告错误清单中查看。': ' Some files failed; see the report error list.',
 '找不到本机 Tesseract，请安装并配置 PATH 或 --tesseract': 'Local Tesseract was not found; install it and configure PATH '
                                              'or --tesseract',
 'PDF 超过 50 MB，请拆分后处理': 'PDF exceeds 50 MB; split it before processing',
 '拒绝本地模型服务的重定向': 'Redirects from the local model service are rejected',
 '必须指定已安装的本地模型名；不接受 cloud 模型': 'Specify an installed local model; cloud models are not accepted',
 '本机模型端口无效': 'Invalid local model port',
 '模型输入超过 45000 字符，请拆分 PDF；不会静默截断': 'Model input exceeds 45000 characters; split the PDF. Input is never '
                                   'silently truncated',
 '模型响应过大': 'Model response is too large',
 '模型输出未完成或达到长度上限': 'Model output is incomplete or reached its length limit',
 'PDF 在读取期间发生变化，请使用稳定副本重试': 'The PDF changed during reading; retry with a stable copy',
 '请对照原 PDF 确认页数、明细行数、税费/折扣口径；算术一致不证明提取完整': 'Check every page, line and tax/discount convention against the '
                                           'original PDF; arithmetic agreement does not prove complete '
                                           'extraction',
 'OCR 需要安装 "sheetaudit-ai[ocr]"': 'OCR requires installing "sheetaudit-ai[ocr]"',
 'Tesseract 识别失败；检查语言包与本机安装': 'Tesseract recognition failed; check the installed language packs and local '
                              'installation',
 'PDF 页数须在 1–{0} 之间': 'PDF page count must be between 1 and {0}',
 '本地模型提取结果可能漏行或编造，逐项对照原 PDF': 'Local model extraction may omit or invent rows; compare every item with the '
                              'original PDF',
 '{0} 出现不同值；保留首个值待复核': 'Conflicting values for {0}; the first value is retained for human review',
 '本页存在未直接映射列名的网格；请对照原页确认是否已由坐标提取覆盖': 'This page has a grid without mapped column labels; confirm that '
                                     'coordinate extraction covered it',
 '本页未提取到明细；确认是封面/附页还是漏提取': 'No line items extracted on this page; confirm whether it is a cover/attachment '
                           'or an omission',
 '模型证据未在该页文字中精确匹配': 'Model evidence does not match the page text exactly',
 'OCR 页必须对照原图核实字符、列位和漏行': 'Compare OCR characters, column alignment and missing lines with the original '
                          'image',
 '本页无足够可读文字；可能为扫描件，需本地 OCR 或人工录入': 'Insufficient readable text; this may be a scan requiring local OCR or '
                                   'manual entry',
 '{0} 数字无法解析': 'Cannot parse the number in {0}',
 '明细名称缺失': 'Missing item description',
 '本页明细沿用上一页列位；必须确认这是同一张单据的续表': 'Column positions inherited from the previous page; confirm this is the same '
                               'document continued',
 '{0} 数字无法解析；原值见明细证据': 'Cannot parse the number in {0}; see original line evidence',
 '无法明确解析数字（分隔符、单位或 OCR 字符需要复核）': 'Ambiguous number: review separators, units or OCR characters',
 '数字超过 MVP 支持的 15 位有效数字': 'The MVP supports at most 15 significant digits',
 'JSON 数字必须是无千分位的十进制字符串或 null': 'JSON numbers must be decimal strings without grouping, or null',
 '提取内容必须且只能包含 fields 和 items': 'Extraction content must contain exactly fields and items',
 'fields 必须包含 schema 中的全部字段；未知值填 null': 'fields must include every schema field; use null for unknown values',
 'items 必须为不超过 10000 行的列表': 'items must be a list of at most 10000 rows',
 '不支持的提取记录版本': 'Unsupported extraction record version',
 '提取记录的 document_id 无效': 'Invalid extraction document_id',
 '提取记录的 source 无效': 'Invalid extraction source',
 '提取记录的来源指纹无效': 'Invalid extraction source fingerprint',
 '提取记录页数无效': 'Invalid extraction page count',
 '提取记录文件名无效': 'Invalid extraction filename',
 '提取记录缺少来源证据或提示列表': 'Extraction record is missing source evidence or the notice list',
 '字段 {0} 必须为短字符串或 null': 'Field {0} must be a short string or null',
 '明细行字段不匹配 schema': 'Item fields do not match the schema',
 'row_id 必须为唯一的字母数字 ID': 'row_id must be a unique alphanumeric ID',
 '明细页码超出 PDF 范围': 'Item page is outside the PDF page range',
 '明细 {0} 必须为非空短字符串': 'Item {0} must be a nonempty short string',
 '单据汇总': 'Documents',
 '固定快照，不跨币种汇总金额。算术一致不代表发票真实、提取完整或可入账。修正数据须通过 review 命令重跑。': 'Snapshot only. Do not sum currencies. Agreement '
                                                            'does not prove authenticity, completeness or '
                                                            'posting eligibility. Use review to recalculate '
                                                            'corrections.',
 '明细核对': 'Line checks',
 '差异=原金额−四舍五入后的数量×单价；计算由 Python Decimal 完成。表内数字为运行时快照，改 Excel 不会重算。': 'Difference = stated amount - rounded '
                                                                      'quantity x price. Python Decimal '
                                                                      'performs calculations. Editing this '
                                                                      'Excel snapshot does not recalculate '
                                                                      'it.',
 '差异与复核': 'Exceptions and review',
 '此表用于查看结果；实际修正请编辑对应单据的 review.xlsx。已解决提示保留处理依据，计算差异不能手动关闭。': 'For corrections, edit the document '
                                                              'review.xlsx. Resolved notices retain reasons. '
                                                              'Arithmetic differences cannot be manually '
                                                              'dismissed.',
 '字段与来源': 'Fields and sources',
 'source.json 保存原始页面文字与表格，extracted.json 保存提取结果。SHA-256 用于绑定人工修正与原 PDF。': 'source.json retains page text and '
                                                                          'tables; extracted.json retains '
                                                                          'extraction results. SHA-256 binds '
                                                                          'corrections to the original PDF.',
 '单据 ID': 'Document ID',
 '文件': 'File',
 '单据号': 'Document number',
 '类型': 'Type',
 '币种': 'Currency',
 '明细数': 'Lines',
 '差异数': 'Differences',
 '提取提示数': 'Extraction notices',
 '人工复核': 'Human review',
 '处理状态': 'Processing status',
 '行 ID': 'Row ID',
 '页码': 'Page',
 '品名': 'Description',
 '数量': 'Quantity',
 '单价': 'Unit price',
 '原金额': 'Stated amount',
 '计算金额': 'Calculated amount',
 '结果': 'Result',
 '原文证据': 'Source evidence',
 '检查代码': 'Check code',
 '检查/原因': 'Check / reason',
 '计算值': 'Expected',
 '原值': 'Original value',
 '说明': 'Notes',
 '复核人': 'Reviewer',
 '处理备注': 'Resolution notes',
 '字段': 'Field',
 '提取值': 'Extracted value',
 '来源页码': 'Source pages',
 '来源证据/元信息': 'Source evidence / metadata',
 '报告已生成': 'Report generated',
 '容差={0}；金额小数位={1}': 'Tolerance={0}; decimal places={1}',
 '待人工处理': 'Needs manual attention',
 '处理失败': 'Failed',
 '待复核': 'Needs review',
 '人工已解决': 'Resolved by reviewer',
 '引擎：': 'Engine: ',
 '{0}；完整性确认={1}；{2}': '{0}; coverage confirmed={1}; {2}',
 '见原 PDF 和 source.json；推断字段/模型或人工提取无独立字段定位': 'See the original PDF and source.json; inferred/model/manual '
                                             'values have no independent field location',
 '修正文件 schema 不匹配': 'Correction schema does not match',
 '修正文件与原 PDF 指纹不符': 'Correction fingerprint does not match the original PDF',
 '原提取结果已变化，请重新生成复核模板': 'The base extraction changed; regenerate the review template',
 '复核时间必须带时区': 'Review timestamp must include a timezone',
 'coverage_confirmed 必须为 true 或 false': 'coverage_confirmed must be true or false',
 'resolutions 必须为列表': 'resolutions must be a list',
 '复核人、时间和说明必须填写': 'Reviewer, timestamp and notes are required',
 '复核时间必须为 ISO 8601，例如 2026-10-24T20:00:00+08:00': 'Use an ISO 8601 review timestamp, for example '
                                                  '2026-10-24T20:00:00+08:00',
 '问题处理记录格式无效': 'Invalid issue resolution record',
 '问题 ID 不存在或重复；不能手动关闭算术差异': 'Unknown or duplicate issue ID; arithmetic differences cannot be manually '
                            'dismissed',
 '问题状态必须为 open 或 resolved': 'Issue action must be open or resolved',
 '问题处理说明格式无效': 'Invalid issue resolution notes',
 '关闭提取提示必须填写处理依据': 'Resolving an extraction notice requires a reason',
 '未确认完整性时不能关闭完整性复核提示': 'Cannot resolve the coverage notice without confirming coverage',
 '金额': 'Amount',
 '操作': 'Action',
 '含义': 'Meaning',
 '修正值（空白=未知）': 'Corrected value (blank = unknown)',
 '请选择确认状态': 'Select coverage status',
 '仅支持未确认或已确认': 'Choose Unconfirmed or Confirmed',
 '复核签注': 'Review sign-off',
 '先在本机打开原 PDF，再编辑黄色单元格。保存后执行 review 命令；Excel 中不自动重算。': 'Open the original PDF locally, then edit yellow '
                                                       'cells. Save and run review; Excel does not '
                                                       'recalculate automatically.',
 '字段修正': 'Field corrections',
 '仅编辑 D 列；未知留空，确认无此项时填 0。标识符和金额按文本保留，避免丢失前导零。': 'Edit column D only. Leave unknowns blank; enter 0 only when '
                                                'confirmed absent. Keep identifiers and amounts as text to '
                                                'preserve leading zeros.',
 '明细修正': 'Item corrections',
 '编辑现有行时保留行 ID；删行请选择“删除”，不要直接移除整行。新增行须填写新的唯一 ID、页码和证据。': 'Keep existing row IDs. Select Delete instead of '
                                                         'removing a row. New rows require a unique ID, page '
                                                         'and evidence.',
 '原始明细': 'Original items',
 '本次修正前的数值快照，不可编辑；更早版本保存在 before-review.json。': 'Read-only snapshot before these corrections. Earlier '
                                                'versions are retained in before-review.json.',
 '问题处理': 'Issue resolutions',
 '提取提示可标记已解决并填写依据；算术差异必须通过数据修正后重新计算，不允许手动隐藏。': 'Resolve extraction notices with reasons. Arithmetic '
                                               'differences require corrected data and recalculation; they '
                                               'cannot be hidden manually.',
 '单据类型': 'Document type',
 '日期': 'Date',
 '销售方': 'Seller',
 '购买方': 'Buyer',
 '小计': 'Subtotal',
 '税额': 'Tax',
 '折扣': 'Discount',
 '运费': 'Shipping',
 '总计': 'Total',
 '项目': 'Item',
 '填写值': 'Your value',
 '填写实际复核人，不由代理代签': 'Enter the actual human reviewer; an agent must not sign on their behalf',
 '带时区时间，例如 2026-10-25T10:00:00+08:00': 'Timestamp with timezone, for example 2026-10-25T10:00:00+08:00',
 '未确认': 'Unconfirmed',
 '逐页确认行数、字段和税费口径后选择“已确认”': 'Check every page, line, field and tax convention, then choose Confirmed',
 '本次核对与修改的依据，必填': 'Required: explain the basis for this review and corrections',
 '原 PDF 文件名；下面命令的 --source 指向该原件': 'Original PDF filename; --source must point to that original',
 '金额采用指定小数位四舍五入；不自动推断业务口径': 'Amounts use the selected precision and ROUND_HALF_UP; business rules are not '
                            'inferred',
 '生成时小数位；默认在重算时沿用': 'Precision when generated; inherited during recalculation by default',
 '生成时容差；需要改变时在 review 命令显式指定': 'Tolerance when generated; specify an explicit review option to change it',
 '"未确认,已确认"': '"Unconfirmed,Confirmed"',
 '"保留,删除"': '"Keep,Delete"',
 '问题 ID': 'Issue ID',
 '提示': 'Notice',
 '处理依据': 'Resolution reason',
 '"待处理,已解决"': '"Open,Resolved"',
 '复核工作簿超过 20 MB': 'Review workbook exceeds 20 MB',
 '已确认': 'Confirmed',
 '金额或数量必须为明确的十进制数值': 'Amounts and quantities must be explicit decimal values',
 '保留': 'Keep',
 '待处理': 'Open',
 '复核工作簿解压体积过大': 'Uncompressed review workbook is too large',
 '复核工作簿缺少工作表或包含未知工作表': 'Review workbook has missing or unknown sheets',
 '复核工作簿与当前原提取版本不匹配': 'Review workbook does not match this extraction version',
 '复核完整性请选择已确认或未确认': 'Choose Confirmed or Unconfirmed for coverage',
 '字段行被删除、重复或字段名被更改': 'Field rows were removed, duplicated or renamed',
 '原始明细被修改；请只编辑明细修正工作表': 'Original items were modified; edit the Item corrections sheet only',
 '删除': 'Delete',
 '原明细行被直接删除或 ID 被改动；请使用操作列的删除选项': 'An original row was removed or its ID changed; use Delete in the Action '
                                  'column',
 '原问题行被删除': 'An original issue row was removed',
 '复核工作簿列顺序或表头被修改': 'Review workbook column order or headers were changed',
 '复核工作簿行列超出限制': 'Review workbook row/column limits exceeded',
 '原值列被修改；请仅编辑字段修正列': 'An original value was modified; edit the corrected-value column only',
 '行 ID 缺失或重复': 'Missing or duplicate row ID',
 '每条明细的操作必须为保留或删除': 'Each item action must be Keep or Delete',
 '问题 ID 被修改或重复': 'Issue ID was changed or duplicated',
 '原问题内容被修改；请只编辑处理状态和依据': 'Original issue content was changed; edit only its status and reason',
 '已解决': 'Resolved',
 '问题状态必须为待处理或已解决': 'Issue status must be Open or Resolved',
 '复核工作簿不接受公式；请粘贴明确数值': 'Review workbooks reject formulas; paste explicit values',
 '单据号、名称等字段必须是文本；请避免 Excel 自动转换标识符': 'Document identifiers and names must be text; prevent Excel from '
                                     'converting identifiers',
 '语言': 'Language',
 '界面和报告语言': 'Interface and report language',
 '仅本机处理  ·  {0}': 'Local processing - {0}',
 '复核工作簿元信息无效': 'Invalid review workbook metadata',
 '请选择有效的原提取记录': 'Select a valid original extraction record',
 '请选择有效的已保存的复核表': 'Select a valid saved review workbook',
 '请选择有效的原始 PDF': 'Select a valid original PDF'}

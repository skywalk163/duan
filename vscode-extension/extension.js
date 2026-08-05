// 段言 VSCode 扩展入口
const vscode = require('vscode');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');

// =============================================================================
// 全局状态
// =============================================================================

/** @type {vscode.LanguageClient} */
let client = null;

/** @type {vscode.StatusBarItem} */
let statusBarItem = null;

/** @type {vscode.DiagnosticCollection} */
let diagnosticCollection = null;

/** @type {vscode.OutputChannel} */
let outputChannel = null;

// =============================================================================
// 工具函数
// =============================================================================

/**
 * 获取 Python 解释器路径
 */
function getPythonPath() {
    const configPath = vscode.workspace.getConfiguration('duan').get('pythonPath');
    if (configPath && configPath.trim()) return configPath;
    return process.platform === 'win32' ? 'python' : 'python3';
}

/**
 * 获取项目根目录（duan 源码目录）
 */
function getProjectRoot() {
    const extPath = vscode.extensions.getExtension('duan-lang.duan-language')?.extensionPath;
    if (extPath) {
        // 扩展目录在 vscode-extension/ 下，项目根目录是上一级
        const candidates = [
            path.join(extPath, '..'),
            path.join(extPath, '..', '..'),
        ];
        for (const p of candidates) {
            try {
                if (fs.existsSync(path.join(p, 'cli', 'duan.py'))) {
                    return p;
                }
            } catch (_) {}
        }
    }
    // 默认：相对于工作区
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri?.fsPath;
    return workspaceRoot || '.';
}

/**
 * 在终端中执行段言 CLI 命令
 */
function runDuanCommand(command, terminalName) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('没有打开的编辑器');
        return;
    }
    const filePath = editor.document.uri.fsPath;
    const projectRoot = getProjectRoot();
    const pythonCmd = getPythonPath();

    const terminal = vscode.window.createTerminal(terminalName || '段言');
    terminal.show();
    terminal.sendText(`cd "${projectRoot}" ; ${pythonCmd} -m cli.duan ${command} "${filePath}"`);
}

/**
 * 获取当前段言文件路径
 */
function getActiveDuanFile() {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.document.languageId !== 'duan') {
        vscode.window.showInformationMessage('请打开一个段言 (.duan) 文件');
        return null;
    }
    return editor.document.uri.fsPath;
}

/**
 * 格式化错误输出为 file:line:col: message 格式
 */
function formatErrorOutput(output) {
    const diagnostics = [];
    const lines = output.split('\n');
    for (const line of lines) {
        // 匹配常见错误格式: 文件:行:列: 消息
        const match = line.match(/^(.+?):(\d+):(\d+):\s*(.+)$/);
        if (match) {
            diagnostics.push({
                file: match[1],
                line: parseInt(match[2]) - 1,
                col: parseInt(match[3]) - 1,
                message: match[4]
            });
        }
    }
    return diagnostics;
}

// =============================================================================
// LSP 服务器管理
// =============================================================================

/**
 * 查找 LSP 服务器路径
 */
function findServerPath() {
    const configPath = vscode.workspace.getConfiguration('duan').get('serverPath');
    if (configPath && configPath.trim()) return configPath;

    const projectRoot = getProjectRoot();
    const candidates = [
        path.join(projectRoot, 'lsp', 'duan_lsp.py'),
        path.join(projectRoot, '..', 'lsp', 'duan_lsp.py'),
    ];
    for (const p of candidates) {
        try {
            if (fs.existsSync(p)) return p;
        } catch (_) {}
    }
    return path.join(projectRoot, 'lsp', 'duan_lsp.py');
}

/**
 * 启动 LSP 客户端
 */
function startLSP(context) {
    const serverPath = findServerPath();
    const pythonCmd = getPythonPath();

    outputChannel.appendLine(`[段言] 启动 LSP 服务器: ${pythonCmd} ${serverPath}`);

    const serverOptions = {
        command: pythonCmd,
        args: [serverPath],
        options: {
            cwd: path.dirname(serverPath),
        }
    };

    const clientOptions = {
        documentSelector: [{ scheme: 'file', language: 'duan' }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/*.duan')
        },
        outputChannel: outputChannel,
        traceOutputChannel: vscode.window.createOutputChannel('段言 LSP Trace'),
    };

    client = new vscode.LanguageClient(
        'duan-lsp',
        '段言语言服务器',
        serverOptions,
        clientOptions
    );

    client.onDidChangeState(e => {
        if (e.newState === vscode.State.Running) {
            outputChannel.appendLine('[段言] LSP 服务器已启动');
            updateStatusBar('running');
        } else if (e.newState === vscode.State.Stopped) {
            outputChannel.appendLine('[段言] LSP 服务器已停止');
            updateStatusBar('offline');
        }
    });

    client.onReady().then(() => {
        updateStatusBar('running');
    }).catch(err => {
        outputChannel.appendLine(`[段言] LSP 启动失败: ${err.message}`);
        updateStatusBar('error');
    });

    context.subscriptions.push(client.start());
}

// =============================================================================
// 状态栏指示器
// =============================================================================

function createStatusBar(context) {
    statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right,
        100
    );
    statusBarItem.command = 'duan.restartLSP';
    context.subscriptions.push(statusBarItem);
    updateStatusBar('offline');
}

function updateStatusBar(status) {
    if (!statusBarItem) return;
    switch (status) {
        case 'running':
            statusBarItem.text = '$(check) 段言';
            statusBarItem.tooltip = '段言语言服务运行中';
            statusBarItem.backgroundColor = undefined;
            break;
        case 'error':
            statusBarItem.text = '$(error) 段言';
            statusBarItem.tooltip = '段言语言服务错误 - 点击重启';
            statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
            break;
        case 'offline':
        default:
            statusBarItem.text = '$(circle-slash) 段言';
            statusBarItem.tooltip = '段言语言服务离线 - 点击重启';
            statusBarItem.backgroundColor = undefined;
            break;
    }
    statusBarItem.show();
}

// =============================================================================
// 问题面板集成
// =============================================================================

function createDiagnosticCollection(context) {
    diagnosticCollection = vscode.languages.createDiagnosticCollection('duan');
    context.subscriptions.push(diagnosticCollection);
}

/**
 * 运行 CLI 命令并将输出解析为诊断信息，输出到 Problems 面板
 */
function runCommandWithDiagnostics(command, args, sourceName) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    const filePath = editor.document.uri.fsPath;
    const projectRoot = getProjectRoot();
    const pythonCmd = getPythonPath();

    const fullArgs = ['-m', 'cli.duan', command, filePath, ...args];
    const cwd = projectRoot;

    outputChannel.appendLine(`[段言] 执行: ${pythonCmd} ${fullArgs.join(' ')}`);

    exec(
        `"${pythonCmd}" ${fullArgs.map(a => `"${a}"`).join(' ')}`,
        { cwd, encoding: 'utf-8' },
        (error, stdout, stderr) => {
            const output = stderr || stdout || '';
            outputChannel.appendLine(`[段言] 输出: ${output.trim()}`);

            const uri = editor.document.uri;
            const diagnostics = [];

            // 解析错误输出
            const lines = output.split('\n');
            let currentLine = 0;
            let currentCol = 0;

            for (const line of lines) {
                // 格式: 文件:行:列: 消息
                const match = line.match(/^(.+?):(\d+):(\d+):\s*(.+)$/);
                if (match) {
                    const errLine = Math.max(0, parseInt(match[2]) - 1);
                    const errCol = Math.max(0, parseInt(match[3]) - 1);
                    diagnostics.push(new vscode.Diagnostic(
                        new vscode.Range(errLine, errCol, errLine, errCol + 1),
                        match[4],
                        vscode.DiagnosticSeverity.Error
                    ));
                }
                // 格式: 错误: 或 ❌ 开头的行
                else if (line.includes('错误') || line.includes('❌')) {
                    diagnostics.push(new vscode.Diagnostic(
                        new vscode.Range(currentLine, currentCol, currentLine, currentCol + 1),
                        line.trim(),
                        vscode.DiagnosticSeverity.Error
                    ));
                }
                // 格式: ⚠ 开头的行
                else if (line.includes('⚠') || line.includes('警告')) {
                    diagnostics.push(new vscode.Diagnostic(
                        new vscode.Range(currentLine, currentCol, currentLine, currentCol + 1),
                        line.trim(),
                        vscode.DiagnosticSeverity.Warning
                    ));
                }
            }

            diagnosticCollection.set(uri, diagnostics);

            if (diagnostics.length > 0) {
                outputChannel.appendLine(`[段言] ${sourceName}: 发现 ${diagnostics.length} 个问题`);
                outputChannel.show(true);
            } else if (!error) {
                vscode.window.showInformationMessage(`段言: ${sourceName}通过`);
            }
        }
    );
}

// =============================================================================
// Task Provider
// =============================================================================

class DuanTaskProvider {
    constructor(projectRoot, pythonCmd) {
        this.projectRoot = projectRoot;
        this.pythonCmd = pythonCmd;
    }

    provideTasks() {
        const tasks = [];

        // 编译任务 (Ctrl+Shift+B)
        const compileTask = new vscode.Task(
            { type: 'duan', task: 'compile' },
            vscode.TaskScope.Workspace,
            '段言: 编译当前文件',
            '段言',
            new vscode.ShellExecution(
                `"${this.pythonCmd}" -m cli.duan compile "\${file}"`,
                { cwd: this.projectRoot }
            ),
            '$duan'
        );
        compileTask.group = vscode.TaskGroup.Build;
        compileTask.problemMatchers = ['$duan'];
        tasks.push(compileTask);

        // LLVM 编译任务
        const llvmTask = new vscode.Task(
            { type: 'duan', task: 'compile-llvm' },
            vscode.TaskScope.Workspace,
            '段言: 编译当前文件 (LLVM-Typed)',
            '段言',
            new vscode.ShellExecution(
                `"${this.pythonCmd}" -m cli.duan compile "\${file}" --backend llvm-typed`,
                { cwd: this.projectRoot }
            ),
            '$duan'
        );
        llvmTask.group = vscode.TaskGroup.Build;
        llvmTask.problemMatchers = ['$duan'];
        tasks.push(llvmTask);

        // 运行任务
        const runTask = new vscode.Task(
            { type: 'duan', task: 'run' },
            vscode.TaskScope.Workspace,
            '段言: 运行当前文件',
            '段言',
            new vscode.ShellExecution(
                `"${this.pythonCmd}" -m cli.duan run "\${file}"`,
                { cwd: this.projectRoot }
            ),
            '$duan'
        );
        runTask.group = vscode.TaskGroup.Test;
        tasks.push(runTask);

        // 语法检查任务
        const checkTask = new vscode.Task(
            { type: 'duan', task: 'check' },
            vscode.TaskScope.Workspace,
            '段言: 语法检查当前文件',
            '段言',
            new vscode.ShellExecution(
                `"${this.pythonCmd}" -m cli.duan check "\${file}"`,
                { cwd: this.projectRoot }
            ),
            '$duan'
        );
        checkTask.group = vscode.TaskGroup.Test;
        checkTask.problemMatchers = ['$duan'];
        tasks.push(checkTask);

        return tasks;
    }

    resolveTask(task) {
        return task;
    }
}

// =============================================================================
// 补全提供器
// =============================================================================

class DuanCompletionProvider {
    provideCompletionItems(document, position) {
        const items = [];

        // 关键字补全
        const keywords = [
            { label: '设', detail: '变量赋值', insertText: '设 ${1:变量名} 为 ${2:值}' },
            { label: '为', detail: '赋值关键字' },
            { label: '如果', detail: '条件判断', insertText: '如果 ${1:条件}：\n    ${2:代码}' },
            { label: '否则', detail: '否则分支', insertText: '否则：\n    ${1:代码}' },
            { label: '否则如果', detail: '否则如果分支', insertText: '否则如果 ${1:条件}：\n    ${2:代码}' },
            { label: '遍历', detail: '遍历循环', insertText: '遍历 ${1:项} 于 ${2:列表}：\n    ${3:代码}' },
            { label: '当', detail: '当循环', insertText: '当 ${1:条件}：\n    ${2:代码}' },
            { label: '段落', detail: '定义段落(函数)', insertText: '段落 ${1:名称} 接收 ${2:参数}：\n    ${3:代码}' },
            { label: '函数', detail: '定义函数', insertText: '函数 ${1:名称}(${2:参数})：\n    ${3:代码}' },
            { label: '返回', detail: '返回值', insertText: '返回 ${1:值}' },
            { label: '类', detail: '定义类', insertText: '类 ${1:名称}：\n    属性 ${2:属性名}\n\n    构造 接收 ${3:参数}：\n        己${2:属性名} 为 ${3:参数}\n\n    段落 ${4:方法名}()：\n        ${5:代码}' },
            { label: '继承', detail: '类继承' },
            { label: '属性', detail: '类属性声明' },
            { label: '构造', detail: '构造函数' },
            { label: '己', detail: '自身引用(self)' },
            { label: '父', detail: '父类引用(super)' },
            { label: '新建', detail: '创建对象实例', insertText: '新建 ${1:类名}(${2:参数})' },
            { label: '导入', detail: '导入模块', insertText: '导入《${1:模块名》' },
            { label: '导出', detail: '导出符号', insertText: '导出 ${1:符号}' },
            { label: '从', detail: '从模块导入', insertText: '从《${1:模块名》导入《${2:符号》' },
            { label: '真', detail: '布尔值 true' },
            { label: '假', detail: '布尔值 false' },
            { label: '空', detail: '空值 None' },
            { label: '打印', detail: '输出到控制台', insertText: '打印(${1:值})' },
            { label: '尝试', detail: '异常捕获' },
            { label: '捕获', detail: '捕获异常' },
            { label: '抛出', detail: '抛出异常', insertText: '抛出 ${1:异常}' },
            { label: '跳出', detail: '跳出循环' },
            { label: '跳过', detail: '跳过当前迭代' },
            { label: '异步', detail: '异步函数' },
            { label: '等待', detail: 'await 表达式' },
            { label: '接口', detail: '定义接口' },
            { label: '实现', detail: '实现接口' },
            { label: '匹配', detail: '模式匹配', insertText: '匹配 ${1:值}：\n    情况 ${2:模式}：\n        ${3:代码}' },
        ];

        for (const kw of keywords) {
            const item = new vscode.CompletionItem(kw.label, vscode.CompletionItemKind.Keyword);
            item.detail = kw.detail;
            if (kw.insertText) {
                item.insertText = new vscode.SnippetString(kw.insertText);
            }
            item.range = document.getWordRangeAtPosition(position);
            items.push(item);
        }

        // 内置函数补全
        const builtins = [
            { label: '类型', detail: '获取值的类型', insertText: '类型(${1:值})' },
            { label: '长度', detail: '获取列表/字符串长度', insertText: '长度(${1:列表})' },
            { label: '转整数', detail: '转换为整数', insertText: '转整数(${1:值})' },
            { label: '转小数', detail: '转换为浮点数', insertText: '转小数(${1:值})' },
            { label: '转字符串', detail: '转换为字符串', insertText: '转字符串(${1:值})' },
            { label: '取整', detail: '向下取整', insertText: '取整(${1:值})' },
            { label: '绝对值', detail: '绝对值', insertText: '绝对值(${1:值})' },
            { label: '最大值', detail: '最大值', insertText: '最大值(${1:值}, ${2:值})' },
            { label: '最小值', detail: '最小值', insertText: '最小值(${1:值}, ${2:值})' },
            { label: '范围', detail: '生成范围', insertText: '范围(${1:开始}, ${2:结束})' },
            { label: '解析JSON', detail: '解析 JSON 字符串', insertText: '解析JSON(${1:字符串})' },
            { label: '序列化JSON', detail: '序列化为 JSON', insertText: '序列化JSON(${1:值})' },
            { label: '输入', detail: '读取用户输入', insertText: '输入(${1:提示})' },
        ];

        for (const fn of builtins) {
            const item = new vscode.CompletionItem(fn.label, vscode.CompletionItemKind.Function);
            item.detail = fn.detail;
            if (fn.insertText) {
                item.insertText = new vscode.SnippetString(fn.insertText);
            }
            items.push(item);
        }

        // 运算符补全
        const operators = [
            { label: '加', detail: '加法运算' },
            { label: '减', detail: '减法运算' },
            { label: '乘', detail: '乘法运算' },
            { label: '除', detail: '除法运算' },
            { label: '模', detail: '取模运算' },
            { label: '幂', detail: '幂运算' },
            { label: '大于', detail: '大于比较' },
            { label: '小于', detail: '小于比较' },
            { label: '等于', detail: '等于比较' },
            { label: '不等于', detail: '不等于比较' },
            { label: '大于等于', detail: '大于等于比较' },
            { label: '小于等于', detail: '小于等于比较' },
            { label: '且', detail: '逻辑与' },
            { label: '或', detail: '逻辑或' },
            { label: '非', detail: '逻辑非' },
        ];

        for (const op of operators) {
            const item = new vscode.CompletionItem(op.label, vscode.CompletionItemKind.Operator);
            item.detail = op.detail;
            items.push(item);
        }

        return items;
    }
}

// =============================================================================
// 悬浮提示提供器
// =============================================================================

class DuanHoverProvider {
    provideHover(document, position) {
        const wordRange = document.getWordRangeAtPosition(position);
        if (!wordRange) return null;

        const word = document.getText(wordRange);

        const hoverDocs = {
            '设': '### 设\n\n变量赋值语句。\n\n```\n设 变量名 为 值\n```\n\n示例：\n```\n设 甲 为 10\n设 姓名 为 "张三"\n```',
            '为': '### 为\n\n赋值关键字，与 `设` 配合使用。',
            '如果': '### 如果\n\n条件判断语句。\n\n```\n如果 条件：\n    代码\n否则如果 条件：\n    代码\n否则：\n    代码\n```',
            '否则': '### 否则\n\n条件判断的否则分支，与 `如果` 配合使用。',
            '否则如果': '### 否则如果\n\n多条件判断链，与 `如果` 配合使用。',
            '遍历': '### 遍历\n\n遍历循环，迭代列表中的每个元素。\n\n```\n遍历 项 于 列表：\n    代码\n```',
            '当': '### 当\n\n当循环，条件为真时重复执行。\n\n```\n当 条件：\n    代码\n```',
            '段落': '### 段落\n\n定义段落（函数）。\n\n```\n段落 名称 接收 参数：\n    代码\n    返回 值\n```',
            '函数': '### 函数\n\n定义函数（现代语法）。\n\n```\n函数 名称(参数)：\n    代码\n    返回 值\n```',
            '返回': '### 返回\n\n从段落（函数）中返回值。\n\n```\n返回 值\n```',
            '类': '### 类\n\n定义类。\n\n```\n类 类名：\n    属性 属性名\n    构造 接收 参数：\n        己属性名 为 参数\n    段落 方法名()：\n        代码\n```',
            '己': '### 己\n\n自身引用，等同于 Python 的 `self`。\n\n```\n己属性名\n己方法名()\n```',
            '父': '### 父\n\n父类引用，等同于 Python 的 `super()`。\n\n```\n父.构造(参数)\n```',
            '新建': '### 新建\n\n创建对象实例。\n\n```\n新建 类名(参数)\n```',
            '真': '### 真\n\n布尔值 `true`。',
            '假': '### 假\n\n布尔值 `false`。',
            '空': '### 空\n\n空值，等同于 Python 的 `None`。',
            '打印': '### 打印\n\n输出值到控制台。\n\n```\n打印("你好")\n打印(变量)\n打印("值：")打印(值)\n```',
            '导入': '### 导入\n\n导入模块。\n\n```\n导入《模块名》\n从《模块名》导入《符号》\n```',
            '导出': '### 导出\n\n声明模块的导出符号。\n\n```\n导出 符号一 符号二\n```',
            '跳出': '### 跳出\n\n跳出当前循环（等同于 Python 的 `break`）。',
            '跳过': '### 跳过\n\n跳过当前循环迭代（等同于 Python 的 `continue`）。',
            '尝试': '### 尝试\n\n异常捕获语句。\n\n```\n尝试：\n    代码\n捕获 异常变量：\n    处理代码\n```',
            '抛出': '### 抛出\n\n抛出异常。\n\n```\n抛出 异常值\n```',
            '匹配': '### 匹配\n\n模式匹配语句。\n\n```\n匹配 值：\n    情况 模式：\n        代码\n```',
            '异步': '### 异步\n\n声明异步函数。\n\n```\n异步 段落 名称 接收 参数：\n    await 操作\n```',
            '等待': '### 等待\n\n等待异步操作完成（等同于 Python 的 `await`）。',
            '长度': '### 长度\n\n获取列表或字符串的长度。\n\n```\n长度(列表)\n长度("字符串")\n```',
            '类型': '### 类型\n\n获取值的类型名称。\n\n```\n类型(值)\n```',
            '转整数': '### 转整数\n\n将值转换为整数。\n\n```\n转整数("42")  → 42\n```',
            '转小数': '### 转小数\n\n将值转换为浮点数。\n\n```\n转小数("3.14")  → 3.14\n```',
            '转字符串': '### 转字符串\n\n将值转换为字符串。\n\n```\n转字符串(42)  → "42"\n```',
            '范围': '### 范围\n\n生成整数范围。\n\n```\n范围(1, 10)  → [1, 2, ..., 10]\n```',
            '解析JSON': '### 解析JSON\n\n将 JSON 字符串解析为 Python 对象。',
            '序列化JSON': '### 序列化JSON\n\n将 Python 对象序列化为 JSON 字符串。',
        };

        if (hoverDocs[word]) {
            return new vscode.Hover(new vscode.MarkdownString(hoverDocs[word]));
        }

        return null;
    }
}

// =============================================================================
// 命令注册
// =============================================================================

function registerCommands(context) {
    // --- 运行文件 ---
    const runCmd = vscode.commands.registerCommand('duan.run', () => {
        const filePath = getActiveDuanFile();
        if (!filePath) return;

        const terminal = vscode.window.createTerminal(`段言运行: ${path.basename(filePath)}`);
        terminal.show();
        const projectRoot = getProjectRoot();
        const pythonCmd = getPythonPath();
        terminal.sendText(`cd "${projectRoot}" ; ${pythonCmd} -m cli.duan run "${filePath}"`);
    });

    // --- 语法检查 ---
    const checkCmd = vscode.commands.registerCommand('duan.check', () => {
        const filePath = getActiveDuanFile();
        if (!filePath) return;
        runCommandWithDiagnostics('check', [], '语法检查');
    });

    // --- 编译 ---
    const compileCmd = vscode.commands.registerCommand('duan.compile', () => {
        const filePath = getActiveDuanFile();
        if (!filePath) return;

        const terminal = vscode.window.createTerminal(`段言编译: ${path.basename(filePath)}`);
        terminal.show();
        const projectRoot = getProjectRoot();
        const pythonCmd = getPythonPath();
        terminal.sendText(`cd "${projectRoot}" ; ${pythonCmd} -m cli.duan compile "${filePath}"`);
    });

    // --- LLVM-Typed 编译 ---
    const compileLLVMCmd = vscode.commands.registerCommand('duan.compileLLVM', () => {
        const filePath = getActiveDuanFile();
        if (!filePath) return;

        const terminal = vscode.window.createTerminal(`段言 LLVM 编译: ${path.basename(filePath)}`);
        terminal.show();
        const projectRoot = getProjectRoot();
        const pythonCmd = getPythonPath();
        const outPath = filePath.replace(/\.duan$/, '.exe');
        terminal.sendText(`cd "${projectRoot}" ; ${pythonCmd} -m cli.duan compile "${filePath}" --backend llvm-typed -o "${outPath}"`);
    });

    // --- 类型检查 ---
    const typeCheckCmd = vscode.commands.registerCommand('duan.typeCheck', () => {
        const filePath = getActiveDuanFile();
        if (!filePath) return;
        runCommandWithDiagnostics('type-check', ['--level', '表达式'], '类型检查');
    });

    // --- REPL ---
    const replCmd = vscode.commands.registerCommand('duan.repl', () => {
        const projectRoot = getProjectRoot();
        const pythonCmd = getPythonPath();
        const terminal = vscode.window.createTerminal('段言 REPL');
        terminal.show();
        terminal.sendText(`cd "${projectRoot}" ; ${pythonCmd} -m cli.duan repl`);
    });

    // --- 重启 LSP ---
    const restartCmd = vscode.commands.registerCommand('duan.restartLSP', async () => {
        updateStatusBar('offline');
        if (client) {
            try {
                await client.stop();
            } catch (e) {
                outputChannel.appendLine(`[段言] 停止 LSP 失败: ${e.message}`);
            }
        }
        try {
            startLSP(context);
            vscode.window.showInformationMessage('段言 LSP 服务器已重启');
        } catch (e) {
            outputChannel.appendLine(`[段言] 启动 LSP 失败: ${e.message}`);
            updateStatusBar('error');
            vscode.window.showErrorMessage('段言 LSP 服务器重启失败');
        }
    });

    context.subscriptions.push(
        runCmd, checkCmd, compileCmd, compileLLVMCmd,
        typeCheckCmd, replCmd, restartCmd
    );
}

// =============================================================================
// 扩展激活 / 停用
// =============================================================================

function activate(context) {
    console.log('段言语言扩展已激活');

    // 输出通道
    outputChannel = vscode.window.createOutputChannel('段言');
    context.subscriptions.push(outputChannel);
    outputChannel.appendLine('段言语言扩展 v1.0.0 已激活');

    // 问题面板
    createDiagnosticCollection(context);

    // 状态栏
    createStatusBar(context);

    // 启动 LSP 语言服务器
    try {
        startLSP(context);
    } catch (e) {
        outputChannel.appendLine(`[段言] LSP 启动失败: ${e.message}`);
        updateStatusBar('error');
        vscode.window.showWarningMessage('段言 LSP 服务器启动失败，部分功能不可用');
    }

    // 注册命令
    registerCommands(context);

    // 注册 Task Provider
    const projectRoot = getProjectRoot();
    const pythonCmd = getPythonPath();
    const taskProvider = new DuanTaskProvider(projectRoot, pythonCmd);
    context.subscriptions.push(
        vscode.tasks.registerTaskProvider('duan', taskProvider)
    );

    // 注册补全提供器
    context.subscriptions.push(
        vscode.languages.registerCompletionItemProvider(
            { scheme: 'file', language: 'duan' },
            new DuanCompletionProvider()
        )
    );

    // 注册悬浮提示提供器
    context.subscriptions.push(
        vscode.languages.registerHoverProvider(
            { scheme: 'file', language: 'duan' },
            new DuanHoverProvider()
        )
    );

    outputChannel.appendLine('[段言] 扩展初始化完成');
}

function deactivate() {
    if (statusBarItem) {
        statusBarItem.dispose();
    }
    if (diagnosticCollection) {
        diagnosticCollection.clear();
    }
    if (outputChannel) {
        outputChannel.appendLine('[段言] 扩展已停用');
    }
    if (client) {
        return client.stop();
    }
    return undefined;
}

module.exports = { activate, deactivate };
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
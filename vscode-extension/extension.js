// 编译模式（用于 vsce package）
if (process.argv.includes('--compile')) {
    console.log('编译完成');
    process.exit(0);
}

// 段言 VSCode 扩展 - 主入口文件
const vscode = require('vscode');
const path = require('path');
const { spawn } = require('child_process');
const { LanguageClient, TransportKind } = require('vscode-languageclient/node');

let client = null;
let diagnosticCollection = null;

// 获取 LSP 服务器路径
function getServerPath() {
    const config = vscode.workspace.getConfiguration('duan-lang');
    const customPath = config.get('serverPath', '');
    if (customPath) {
        return customPath;
    }
    // 默认路径：相对于扩展目录
    const extPath = __dirname;
    return path.join(extPath, '..', 'lsp', 'duan_lsp_server.py');
}

// 启动 LSP 服务器
function startServer() {
    const serverPath = getServerPath();
    const pythonPath = 'python'; // 假设 python 在 PATH 中

    const serverOptions = {
        run: {
            command: pythonPath,
            args: [serverPath],
            options: {
                cwd: path.join(__dirname, '..', '..')
            }
        },
        debug: {
            command: pythonPath,
            args: [serverPath],
            options: {
                cwd: path.join(__dirname, '..', '..')
            }
        }
    };

    const clientOptions = {
        documentSelector: [{ scheme: 'file', language: 'duan' }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/*.duan')
        },
        outputChannelName: '段言 LSP'
    };

    // 使用 Node.js 的 Language Client 来启动 LSP
    const { LanguageClient, TransportKind } = require('vscode-languageclient/node');

    client = new LanguageClient(
        'duan-lang',
        '段言 LSP 服务器',
        serverOptions,
        clientOptions
    );

    client.start();
    client.onReady().then(() => {
        console.log('段言 LSP 服务器已启动');
    }).catch(err => {
        console.error('启动 LSP 服务器失败:', err);
    });
}

// 激活扩展
function activate(context) {
    console.log('段言扩展已激活');

    // 创建诊断集合
    diagnosticCollection = vscode.languages.createDiagnosticCollection('duan');
    context.subscriptions.push(diagnosticCollection);

    // 注册启动命令
    const startCommand = vscode.commands.registerCommand('duan-lang.startServer', () => {
        startServer();
    });
    context.subscriptions.push(startCommand);

    // 自动启动 LSP 服务器
    startServer();

    // 注册文档变化监听器，用于手动验证
    vscode.workspace.onDidOpenTextDocument((doc) => {
        if (doc.languageId === 'duan') {
            validateDocument(doc);
        }
    });

    // 注册内容变更监听器
    vscode.workspace.onDidChangeTextDocument((event) => {
        if (event.document.languageId === 'duan') {
            validateDocument(event.document);
        }
    });

    // 注册文档关闭监听器
    vscode.workspace.onDidCloseTextDocument((doc) => {
        if (doc.languageId === 'duan') {
            diagnosticCollection.delete(doc.uri);
        }
    });
}

// 验证段言文档
async function validateDocument(document) {
    if (!document) return;

    const diagnostics = [];
    const text = document.getText();

    if (!text.trim()) {
        diagnosticCollection.set(document.uri, []);
        return;
    }

    try {
        // 使用子进程调用段言编译器进行语法检查
        const { execSync } = require('child_process');
        const extPath = path.join(__dirname, '..');
        const compilerPath = path.join(extPath, 'cli', 'duanc.py');

        const result = execSync(`python "${compilerPath}" --check "${document.uri.fsPath}"`, {
            encoding: 'utf-8',
            cwd: extPath,
            timeout: 5000
        });

        // 解析错误输出
        const lines = result.split('\n');
        for (const line of lines) {
            const match = line.match(/Line (\d+): (.+)/);
            if (match) {
                const lineNum = parseInt(match[1], 10) - 1;
                const message = match[2];
                const range = new vscode.Range(lineNum, 0, lineNum, 200);
                diagnostics.push(new vscode.Diagnostic(range, message, vscode.DiagnosticSeverity.Error));
            }
        }
    } catch (error) {
        // 解析错误输出（stderr）
        const errorOutput = error.stdout || error.stderr || '';
        const lines = errorOutput.split('\n');
        for (const line of lines) {
            const match = line.match(/Error:|错误:|SyntaxError:|ParseError:|(.+)\.duan:(\d+):(.+)/);
            if (match) {
                let lineNum = 0;
                let message = line;

                const lineMatch = line.match(/:(\d+):/);
                if (lineMatch) {
                    lineNum = parseInt(lineMatch[1], 10) - 1;
                }

                const range = new vscode.Range(lineNum, 0, lineNum, 200);
                diagnostics.push(new vscode.Diagnostic(range, message, vscode.DiagnosticSeverity.Error));
            }
        }
    }

    diagnosticCollection.set(document.uri, diagnostics);
}

// 停用扩展
function deactivate() {
    if (client) {
        client.stop();
        client = null;
    }
}

module.exports = {
    activate,
    deactivate
};


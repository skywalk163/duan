// 段言 VSCode 扩展入口
const vscode = require('vscode');
const { exec } = require('child_process');
const path = require('path');

function activate(context) {
    console.log('段言语言扩展已激活');

    // 注册 "运行段言文件" 命令
    const runCmd = vscode.commands.registerCommand('duan.run', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('没有打开的段言文件');
            return;
        }
        const filePath = editor.document.uri.fsPath;
        if (!filePath.endsWith('.duan')) {
            vscode.window.showErrorMessage('当前文件不是段言文件');
            return;
        }

        const terminal = vscode.window.createTerminal('段言运行');
        terminal.show();
        terminal.sendText(`python cli/duan.py run "${filePath}"`);
    });

    // 注册 "检查段言语法" 命令
    const checkCmd = vscode.commands.registerCommand('duan.check', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('没有打开的段言文件');
            return;
        }
        const filePath = editor.document.uri.fsPath;
        if (!filePath.endsWith('.duan')) {
            vscode.window.showErrorMessage('当前文件不是段言文件');
            return;
        }

        const terminal = vscode.window.createTerminal('段言检查');
        terminal.show();
        terminal.sendText(`python cli/duan.py check "${filePath}" --backend src`);
    });

    context.subscriptions.push(runCmd, checkCmd);
}

function deactivate() {
    console.log('段言语言扩展已停用');
}

module.exports = { activate, deactivate };

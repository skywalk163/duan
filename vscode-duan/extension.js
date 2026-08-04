/**
 * 段言 (Duan) VS Code 扩展 v4.0
 * 提供运行、解析命令
 */
const vscode = require('vscode');
const { execSync, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

/**
 * 激活扩展
 */
function activate(context) {
    console.log('段言 v4.0 扩展已激活');

    // 运行当前文件
    const runCmd = vscode.commands.registerCommand('duan.runFile', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('请先打开一个 .duan 文件');
            return;
        }

        const filePath = editor.document.uri.fsPath;
        const pythonPath = vscode.workspace.getConfiguration('duan').get('pythonPath', 'python');

        // 保存文件
        await editor.document.save();

        // 创建输出通道
        const outputChannel = vscode.window.createOutputChannel('段言 运行');
        outputChannel.show(true);
        outputChannel.appendLine(`=== 运行: ${path.basename(filePath)} ===\n`);

        try {
            const projectRoot = findProjectRoot(filePath);
            const cmd = `"${pythonPath}" -c "
import sys
sys.path.insert(0, r'${projectRoot}')
sys.path.insert(0, r'${path.join(projectRoot, 'src')}')
from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator

with open(r'${filePath}', 'r', encoding='utf-8') as f:
    code = f.read()

parser = DuanParser()
ast = parser.parse(code)
if ast is None:
    print('解析错误:', parser.errors)
    sys.exit(1)

gen = PythonCodeGenerator()
py_code = gen.generate(ast)
exec(py_code, {'__name__': '__main__'})
"`;

            const result = execSync(cmd, {
                cwd: projectRoot,
                encoding: 'utf-8',
                timeout: 30000,
                maxBuffer: 10 * 1024 * 1024
            });

            outputChannel.appendLine(result || '(无输出)');
            outputChannel.appendLine('\n=== 运行完成 ===');
        } catch (error) {
            outputChannel.appendLine(`错误: ${error.stderr || error.message}`);
            outputChannel.appendLine('\n=== 运行失败 ===');
        }
    });

    // 解析当前文件 (AST)
    const parseCmd = vscode.commands.registerCommand('duan.parseFile', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('请先打开一个 .duan 文件');
            return;
        }

        const filePath = editor.document.uri.fsPath;
        const pythonPath = vscode.workspace.getConfiguration('duan').get('pythonPath', 'python');

        await editor.document.save();

        const outputChannel = vscode.window.createOutputChannel('段言 AST');
        outputChannel.show(true);
        outputChannel.appendLine(`=== AST 解析: ${path.basename(filePath)} ===\n`);

        try {
            const projectRoot = findProjectRoot(filePath);
            const cmd = `"${pythonPath}" -c "
import sys, json
sys.path.insert(0, r'${projectRoot}')
sys.path.insert(0, r'${path.join(projectRoot, 'src')}')
from duan_parser_v3 import DuanParser

with open(r'${filePath}', 'r', encoding='utf-8') as f:
    code = f.read()

parser = DuanParser()
ast = parser.parse(code)
if ast is None:
    print('解析错误:')
    for e in parser.errors:
        print(f'  {e}')
else:
    print(f'语句数: {len(ast.statements)}')
    for i, stmt in enumerate(ast.statements):
        print(f'[{i}] {type(stmt).__name__}')
        for attr in dir(stmt):
            if not attr.startswith('_'):
                try:
                    val = getattr(stmt, attr)
                    if not callable(val) and val is not None:
                        print(f'    {attr}: {val}')
                except:
                    pass
"`;

            const result = execSync(cmd, {
                cwd: projectRoot,
                encoding: 'utf-8',
                timeout: 10000,
                maxBuffer: 10 * 1024 * 1024
            });

            outputChannel.appendLine(result);
            outputChannel.appendLine('\n=== 解析完成 ===');
        } catch (error) {
            outputChannel.appendLine(`错误: ${error.stderr || error.message}`);
        }
    });

    context.subscriptions.push(runCmd, parseCmd);
}

/**
 * 查找项目根目录（包含 src/ 目录的父目录）
 */
function findProjectRoot(filePath) {
    let dir = path.dirname(filePath);
    while (dir !== path.dirname(dir)) {
        if (fs.existsSync(path.join(dir, 'src', 'duan_parser_v3.py'))) {
            return dir;
        }
        dir = path.dirname(dir);
    }
    return path.dirname(filePath);
}

function deactivate() {}

module.exports = { activate, deactivate };
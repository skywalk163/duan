# -*- coding: utf-8 -*-
"""
段言编程语言 - Language Server Protocol (LSP) 实现

提供 VS Code 等编辑器的智能提示支持。
"""

import sys
import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lexer import Lexer
from duan_parser_v3 import DuanParser
from keywords import ALL_KEYWORDS, VERB_ARITY


# =============================================================================
# LSP 常量
# =============================================================================

LSP_METHODS = {
    # 初始化
    'initialize': 'initialize',
    'initialized': 'initialized',
    'shutdown': 'shutdown',
    'exit': 'exit',
    
    # 文本文档
    'textDocument/didOpen': 'textDocument/didOpen',
    'textDocument/didChange': 'textDocument/didChange',
    'textDocument/didClose': 'textDocument/didClose',
    'textDocument/didSave': 'textDocument/didSave',
    
    # 诊断
    'textDocument/publishDiagnostics': 'textDocument/publishDiagnostics',
    
    # 代码补全
    'textDocument/completion': 'textDocument/completion',
    'completionItem/resolve': 'completionItem/resolve',
    
    # 悬停
    'textDocument/hover': 'textDocument/hover',
    
    # 跳转定义
    'textDocument/definition': 'textDocument/definition',
    'textDocument/typeDefinition': 'textDocument/typeDefinition',
    'textDocument/declaration': 'textDocument/declaration',
    
    # 查找引用
    'textDocument/references': 'textDocument/references',
    
    # 文档符号
    'textDocument/documentSymbol': 'textDocument/documentSymbol',
    
    # 格式化
    'textDocument/formatting': 'textDocument/formatting',
    'textDocument/rangeFormatting': 'textDocument/rangeFormatting',
    
    # 光标位置
    'textDocument/documentHighlight': 'textDocument/documentHighlight',
}


# =============================================================================
# LSP 响应构建器
# =============================================================================

def lsp_response(id: Any, result: Any) -> Dict:
    """构建 LSP 响应"""
    return {
        'jsonrpc': '2.0',
        'id': id,
        'result': result
    }


def lsp_error(id: Any, code: int, message: str) -> Dict:
    """构建 LSP 错误响应"""
    return {
        'jsonrpc': '2.0',
        'id': id,
        'error': {
            'code': code,
            'message': message
        }
    }


def lsp_notification(method: str, params: Dict) -> Dict:
    """构建 LSP 通知"""
    return {
        'jsonrpc': '2.0',
        'method': method,
        'params': params
    }


# =============================================================================
# 文档管理器
# =============================================================================

class Document:
    """LSP 文档"""
    def __init__(self, uri: str, text: str):
        self.uri = uri
        self.text = text
        self.lines = text.split('\n')
        self.version = 1
        
    def update(self, changes: List[Dict]):
        """更新文档内容"""
        for change in changes:
            range_info = change.get('range')
            if range_info:
                start_line = range_info['start']['line']
                start_char = range_info['start']['character']
                end_line = range_info['end']['line']
                end_char = range_info['end']['character']
                
                # 应用更改
                start_offset = sum(len(self.lines[i]) + 1 for i in range(start_line)) + start_char
                end_offset = sum(len(self.lines[i]) + 1 for i in range(end_line)) + end_char
                
                self.text = self.text[:start_offset] + change['text'] + self.text[end_offset:]
            else:
                # 整个文档替换
                self.text = change.get('text', '')
            
            self.lines = self.text.split('\n')
            self.version += 1
    
    def get_line(self, line: int) -> str:
        """获取指定行"""
        if 0 <= line < len(self.lines):
            return self.lines[line]
        return ''
    
    def get_position(self, line: int, character: int) -> int:
        """将 (line, character) 转换为字符偏移"""
        offset = 0
        for i in range(min(line, len(self.lines))):
            offset += len(self.lines[i]) + 1
        return offset + min(character, len(self.lines[line]) if line < len(self.lines) else 0)


class DocumentManager:
    """文档管理器"""
    def __init__(self):
        self.documents: Dict[str, Document] = {}
        self.symbols: Dict[str, List] = {}  # uri -> symbols
        self.definitions: Dict[str, Dict] = {}  # uri -> {name: location}
        self.type_info: Dict[str, Dict] = {}  # uri -> {name: type_str}

    def open_document(self, uri: str, text: str):
        """打开文档"""
        doc = Document(uri, text)
        self.documents[uri] = doc
        self._analyze_document(doc)

    def update_document(self, uri: str, changes: List[Dict]):
        """更新文档"""
        if uri in self.documents:
            self.documents[uri].update(changes)
            self._analyze_document(self.documents[uri])

    def close_document(self, uri: str):
        """关闭文档"""
        self.documents.pop(uri, None)
        self.symbols.pop(uri, None)
        self.definitions.pop(uri, None)
        self.type_info.pop(uri, None)
    
    def get_document(self, uri: str) -> Optional[Document]:
        """获取文档"""
        return self.documents.get(uri)
    
    def _analyze_document(self, doc: Document):
        """分析文档，提取符号、定义和类型信息"""
        try:
            lexer = Lexer()
            tokens = lexer.tokenize(doc.text)

            parser = DuanParser()
            ast = parser.parse_tokens(tokens)

            self.symbols[doc.uri] = self._extract_symbols(ast)
            self.definitions[doc.uri] = self._extract_definitions(ast, doc)

            # 类型推断
            try:
                from type_inferencer import TypeInferencer
                inferencer = TypeInferencer()
                inferencer.infer(ast)
                self.type_info[doc.uri] = self._extract_type_info(ast, inferencer)
            except Exception:
                self.type_info[doc.uri] = {}

        except Exception:
            pass

    def _extract_type_info(self, ast, inferencer) -> Dict:
        """提取变量/函数的类型信息"""
        info = {}

        def walk(node):
            if node is None:
                return
            node_type = type(node).__name__
            name = getattr(node, 'name', None)
            if name and node_type in ('VarDecl', 'VariableDeclaration', 'VarDef',
                                       'FuncDef', 'FunctionDef', 'SegmentDefinition',
                                       'Paragraph'):
                # 检查类型标注
                ta = getattr(node, 'type_annotation', None)
                if ta:
                    info[str(name)] = str(ta)
                else:
                    # 尝试从推断器获取
                    value = getattr(node, 'value', None)
                    if value and inferencer:
                        inferred = inferencer.type_cache.get(id(value))
                        if inferred:
                            info[str(name)] = str(inferred)

            for child_name in dir(node):
                if child_name.startswith('_'):
                    continue
                try:
                    child = getattr(node, child_name)
                    if isinstance(child, list):
                        for item in child:
                            if hasattr(item, '__class__') and hasattr(item, '__dict__'):
                                walk(item)
                    elif hasattr(child, '__class__') and hasattr(child, '__dict__') and hasattr(child, 'line'):
                        walk(child)
                except Exception:
                    pass

        walk(ast)
        return info
    
    def _extract_symbols(self, ast) -> List[Dict]:
        """提取文档符号"""
        symbols = []
        
        def walk(node):
            if node is None:
                return
                
            node_type = type(node).__name__
            
            line = getattr(node, 'line', 1) - 1
            col = getattr(node, 'col', 0)
            
            if node_type == 'FuncDef':
                name = getattr(node, 'name', '?')
                params = getattr(node, 'params', [])
                param_strs = []
                for p in params:
                    pname = getattr(p, 'name', '?') if hasattr(p, 'name') else str(p)
                    param_strs.append(pname)
                detail = f"({', '.join(param_strs)})"
                
                symbols.append({
                    'name': name,
                    'kind': 12,  # Function
                    'detail': detail,
                    'range': {
                        'start': {'line': line, 'character': col},
                        'end': {'line': line, 'character': col + len(name)}
                    },
                    'selectionRange': {
                        'start': {'line': line, 'character': col},
                        'end': {'line': line, 'character': col + len(name)}
                    }
                })
            elif node_type == 'ClassDef':
                name = getattr(node, 'name', '?')
                symbols.append({
                    'name': name,
                    'kind': 5,  # Class
                    'detail': '类',
                    'range': {
                        'start': {'line': line, 'character': col},
                        'end': {'line': line, 'character': col + len(name)}
                    },
                    'selectionRange': {
                        'start': {'line': line, 'character': col},
                        'end': {'line': line, 'character': col + len(name)}
                    }
                })
            elif node_type == 'VarDef':
                name = getattr(node, 'name', '?')
                symbols.append({
                    'name': name,
                    'kind': 6,  # Variable
                    'detail': '变量',
                    'range': {
                        'start': {'line': line, 'character': col},
                        'end': {'line': line, 'character': col + len(name)}
                    },
                    'selectionRange': {
                        'start': {'line': line, 'character': col},
                        'end': {'line': line, 'character': col + len(name)}
                    }
                })
            
            for child_name in dir(node):
                if child_name.startswith('_'):
                    continue
                try:
                    child = getattr(node, child_name)
                    if isinstance(child, list):
                        for item in child:
                            if hasattr(item, '__class__') and hasattr(item, '__dict__'):
                                walk(item)
                    elif hasattr(child, '__class__') and hasattr(child, '__dict__') and hasattr(child, 'line'):
                        walk(child)
                except Exception:
                    pass

        walk(ast)
        return symbols
    
    def _extract_definitions(self, ast, doc) -> Dict:
        """提取定义"""
        definitions = {}
        
        def walk(node):
            if node is None:
                return
                
            node_type = type(node).__name__
            line = getattr(node, 'line', 1) - 1
            col = getattr(node, 'col', 0)
            
            if node_type in ('VarDef', 'FuncDef', 'ClassDef', 'MethodDef'):
                name = getattr(node, 'name', None)
                if name:
                    definitions[name] = {
                        'uri': doc.uri,
                        'range': {
                            'start': {'line': line, 'character': col},
                            'end': {'line': line, 'character': col + len(str(name))}
                        }
                    }
                    
                    # 额外保存节点信息用于悬停
                    if node_type == 'FuncDef':
                        params = getattr(node, 'params', [])
                        param_strs = []
                        for p in params:
                            pname = getattr(p, 'name', '?') if hasattr(p, 'name') else str(p)
                            param_strs.append(pname)
                        definitions[name + '__info'] = {
                            'type': '函数',
                            'params': param_strs,
                            'line': line,
                            'col': col
                        }
            
            for child_name in dir(node):
                if child_name.startswith('_'):
                    continue
                try:
                    child = getattr(node, child_name)
                    if isinstance(child, list):
                        for item in child:
                            if hasattr(item, '__class__') and hasattr(item, '__dict__'):
                                walk(item)
                    elif hasattr(child, '__class__') and hasattr(child, '__dict__') and hasattr(child, 'line'):
                        walk(child)
                except Exception:
                    pass

        walk(ast)
        return definitions


# =============================================================================
# LSP 服务器
# =============================================================================

class DuanLanguageServer:
    """段言 LSP 服务器"""
    
    def __init__(self):
        self.doc_manager = DocumentManager()
        self.capabilities = {
            'textDocumentSync': 1,  # Full sync
            'completionProvider': {
                'resolveProvider': True,
                'triggerCharacters': [' ', '设', '定', '打', '定', '导', '类', '接', '返', '当', '遍', '如']
            },
            'hoverProvider': True,
            'definitionProvider': True,
            'referencesProvider': True,
            'documentSymbolProvider': True,
            'documentFormattingProvider': True,
            'documentRangeFormattingProvider': True,
            'renameProvider': True,
            'codeActionProvider': {
                'codeActionKinds': ['quickfix', 'refactor']
            },
            'diagnosticProvider': {
                'interFileDependencies': False,
                'workspaceDiagnostics': False
            }
        }
        
    def handle_request(self, method: str, params: Dict, id: Any) -> Optional[Dict]:
        """处理请求"""
        handlers = {
            'initialize': self._handle_initialize,
            'textDocument/didOpen': self._handle_did_open,
            'textDocument/didChange': self._handle_did_change,
            'textDocument/didClose': self._handle_did_close,
            'textDocument/didSave': self._handle_did_save,
            'textDocument/completion': self._handle_completion,
            'textDocument/hover': self._handle_hover,
            'textDocument/definition': self._handle_definition,
            'textDocument/references': self._handle_references,
            'textDocument/documentSymbol': self._handle_document_symbol,
            'textDocument/formatting': self._handle_formatting,
            'textDocument/rangeFormatting': self._handle_range_formatting,
            'textDocument/rename': self._handle_rename,
            'textDocument/codeAction': self._handle_code_action,
        }
        
        handler = handlers.get(method)
        if handler:
            try:
                return lsp_response(id, handler(params))
            except Exception as e:
                return lsp_error(id, -32603, str(e))
        
        return None
    
    def _handle_initialize(self, params: Dict) -> Dict:
        """处理初始化请求"""
        return {
            'capabilities': self.capabilities,
            'serverInfo': {
                'name': '段言语言服务器',
                'version': '1.6.0'
            }
        }
    
    def _handle_did_close(self, params: Dict):
        """处理文档关闭"""
        text_doc = params.get('textDocument', {})
        uri = text_doc.get('uri')
        self.doc_manager.close_document(uri)
        return None

    def _handle_did_save(self, params: Dict):
        """处理文档保存"""
        text_doc = params.get('textDocument', {})
        uri = text_doc.get('uri')
        # 重新分析文档并发布诊断
        if uri in self.doc_manager.documents:
            doc = self.doc_manager.documents[uri]
            self.doc_manager._analyze_document(doc)
            self._publish_diagnostics(uri)
        return None

    def _handle_completion(self, params: Dict) -> Dict:
        """处理代码补全"""
        doc = self.doc_manager.get_document(params.get('textDocument', {}).get('uri', ''))
        if not doc:
            return {'isIncomplete': False, 'items': []}
        
        position = params.get('position', {})
        line = position.get('line', 0)
        character = position.get('character', 0)
        
        # 获取当前行的前缀
        line_text = doc.get_line(line)
        # 找到当前词的起始位置
        start = character
        while start > 0:
            ch = line_text[start - 1]
            if ch.isalnum() or '\u4e00' <= ch <= '\u9fff':
                start -= 1
            else:
                break
        prefix = line_text[start:character]
        
        completions = []
        
        # 关键字补全
        for kw in sorted(ALL_KEYWORDS):
            if not prefix or kw.startswith(prefix):
                # 关键字文档
                kw_docs = {
                    '定义': '定义变量：定义 变量名 等于 值。',
                    '设': '设变量为值：设 变量名 为 值。',
                    '如果': '条件语句：如果 条件 那么：...结束。',
                    '若': '条件语句（简写）：若 条件 则：...结束。',
                    '那么': '条件语句 then 分支',
                    '否则': '条件语句 else 分支',
                    '否则若': '条件语句 elif 分支',
                    '遍历': '遍历循环：遍历 变量 于 列表：...结束。',
                    '当': '条件循环：当 条件：...结束。',
                    '返回': '返回语句：返回 表达式。',
                    '跳出': '跳出循环：跳出。',
                    '跳过': '跳过本次迭代：跳过。',
                    '段落': '段落（函数）定义：段落 段名 接收 参数：...结束。',
                    '类': '类定义：类 类名：...结束。',
                    '接口': '接口定义：接口 接口名：...结束。',
                    '尝试': '异常处理：尝试：...捕获 异常：...结束。',
                    '抛出': '抛出异常：抛出 异常对象。',
                    '导入': '导入模块：导入 模块名。',
                    '匹配': '模式匹配：匹配 表达式：情况 模式：...结束。',
                    '异步': '异步函数定义：异步 段落 段名...',
                    '等待': '等待异步操作：等待 异步调用。',
                }
                item = {
                    'label': kw,
                    'kind': 14,  # Keyword
                    'detail': '关键字',
                    'sortText': f'1_{kw}',
                    'filterText': kw,
                    'insertText': kw[len(prefix):] if prefix and kw.startswith(prefix) else kw
                }
                if kw in kw_docs:
                    item['documentation'] = {'kind': 'markdown', 'value': kw_docs[kw]}
                completions.append(item)
        
        # 动词元数补全
        for verb, arity in sorted(VERB_ARITY.items()):
            if not prefix or verb.startswith(prefix):
                completions.append({
                    'label': verb,
                    'kind': 15,  # Snippet
                    'detail': f'动词 (元数: {arity})',
                    'sortText': f'2_{verb}',
                    'filterText': verb
                })
        
        # 本地变量/函数补全
        if doc.uri in self.doc_manager.definitions:
            for name in sorted(self.doc_manager.definitions[doc.uri].keys()):
                if name.endswith('__info'):
                    continue
                if not prefix or name.startswith(prefix):
                    info = self.doc_manager.definitions[doc.uri].get(name + '__info', {})
                    kind = 6  # Variable
                    detail = '变量'
                    if info.get('type') == '函数':
                        kind = 12  # Function
                        detail = f"函数({', '.join(info.get('params', []))})"
                    
                    completions.append({
                        'label': name,
                        'kind': kind,
                        'detail': detail,
                        'sortText': f'3_{name}',
                        'filterText': name
                    })
        
        return {
            'isIncomplete': False,
            'items': completions
        }
    
    def _handle_hover(self, params: Dict) -> Optional[Dict]:
        """处理悬停请求"""
        doc = self.doc_manager.get_document(params.get('textDocument', {}).get('uri', ''))
        if not doc:
            return None
        
        position = params.get('position', {})
        line = position.get('line', 0)
        character = position.get('character', 0)
        
        # 获取当前位置的词
        line_text = doc.get_line(line)
        start = character
        end = character
        
        while start > 0:
            ch = line_text[start - 1]
            if ch.isalnum() or '\u4e00' <= ch <= '\u9fff':
                start -= 1
            else:
                break
        while end < len(line_text):
            ch = line_text[end]
            if ch.isalnum() or '\u4e00' <= ch <= '\u9fff':
                end += 1
            else:
                break
        
        word = line_text[start:end]
        if not word:
            return None
        
        # 构造悬停内容
        contents = []
        
        # 检查是否是关键字
        if word in ALL_KEYWORDS:
            contents.append(f"**关键字**: `{word}`")
        
        # 检查是否是动词
        if word in VERB_ARITY:
            contents.append(f"**动词**: `{word}` (元数: {VERB_ARITY[word]})")
        
        # 检查是否是本地定义
        if doc.uri in self.doc_manager.definitions:
            info = self.doc_manager.definitions[doc.uri].get(word + '__info')
            if info:
                if info['type'] == '函数':
                    params_str = ', '.join(info['params'])
                    contents.append(f"**函数**: `{word}({params_str})`")

            if word in self.doc_manager.definitions[doc.uri]:
                def_info = self.doc_manager.definitions[doc.uri][word]
                def_line = def_info['range']['start']['line'] + 1
                contents.append(f"定义于第 {def_line} 行")

        # 类型信息
        if doc.uri in self.doc_manager.type_info:
            t = self.doc_manager.type_info[doc.uri].get(word)
            if t:
                contents.append(f"**类型**: `{t}`")
        
        if not contents:
            return None
        
        return {
            'contents': {
                'kind': 'markdown',
                'value': '\n\n'.join(contents)
            },
            'range': {
                'start': {'line': line, 'character': start},
                'end': {'line': line, 'character': end}
            }
        }
    
    def _handle_definition(self, params: Dict) -> Optional[Dict]:
        """处理跳转定义请求"""
        doc = self.doc_manager.get_document(params.get('textDocument', {}).get('uri', ''))
        if not doc:
            return None
        
        position = params.get('position', {})
        line = position.get('line', 0)
        character = position.get('character', 0)
        
        # 获取当前位置的词
        line_text = doc.get_line(line)
        start = character
        end = character
        
        while start > 0:
            ch = line_text[start - 1]
            if ch.isalnum() or '\u4e00' <= ch <= '\u9fff':
                start -= 1
            else:
                break
        while end < len(line_text):
            ch = line_text[end]
            if ch.isalnum() or '\u4e00' <= ch <= '\u9fff':
                end += 1
            else:
                break
        
        word = line_text[start:end]
        
        # 查找定义
        if doc.uri in self.doc_manager.definitions:
            if word in self.doc_manager.definitions[doc.uri]:
                return self.doc_manager.definitions[doc.uri][word]
        
        return None
    
    def _handle_document_symbol(self, params: Dict) -> List[Dict]:
        """处理文档符号请求"""
        uri = params.get('textDocument', {}).get('uri', '')
        return self.doc_manager.symbols.get(uri, [])
    
    def _handle_references(self, params: Dict) -> List[Dict]:
        """处理查找引用请求"""
        doc = self.doc_manager.get_document(params.get('textDocument', {}).get('uri', ''))
        if not doc:
            return []

        position = params.get('position', {})
        line = position.get('line', 0)
        character = position.get('character', 0)

        line_text = doc.get_line(line)
        start = character
        end = character
        while start > 0:
            ch = line_text[start - 1]
            if ch.isalnum() or '\u4e00' <= ch <= '\u9fff':
                start -= 1
            else:
                break
        while end < len(line_text):
            ch = line_text[end]
            if ch.isalnum() or '\u4e00' <= ch <= '\u9fff':
                end += 1
            else:
                break

        word = line_text[start:end]
        if not word:
            return []

        references = []
        for uri, doc_obj in self.doc_manager.documents.items():
            for i, line_text in enumerate(doc_obj.lines):
                pos = 0
                while True:
                    idx = line_text.find(word, pos)
                    if idx == -1:
                        break
                    references.append({
                        'uri': uri,
                        'range': {
                            'start': {'line': i, 'character': idx},
                            'end': {'line': i, 'character': idx + len(word)}
                        }
                    })
                    pos = idx + len(word)

        return references

    def _handle_formatting(self, params: Dict) -> List[Dict]:
        """处理文档格式化请求"""
        uri = params.get('textDocument', {}).get('uri', '')
        doc = self.doc_manager.get_document(uri)
        if not doc:
            return []

        options = params.get('options', {})
        tab_size = options.get('tabSize', 4)
        insert_spaces = options.get('insertSpaces', True)

        edits = self._format_document(doc.text, tab_size, insert_spaces)
        return edits

    def _handle_range_formatting(self, params: Dict) -> List[Dict]:
        """处理范围格式化请求"""
        uri = params.get('textDocument', {}).get('uri', '')
        doc = self.doc_manager.get_document(uri)
        if not doc:
            return []

        range_info = params.get('range', {})
        options = params.get('options', {})
        tab_size = options.get('tabSize', 4)
        insert_spaces = options.get('insertSpaces', True)

        # 提取范围内的文本
        start_line = range_info.get('start', {}).get('line', 0)
        end_line = range_info.get('end', {}).get('line', 0)
        lines = doc.text.split('\n')
        range_text = '\n'.join(lines[start_line:end_line + 1])

        edits = self._format_document(
            doc.text, tab_size, insert_spaces,
            start_line=start_line, end_line=end_line
        )
        return edits

    def _format_document(self, text: str, tab_size: int, insert_spaces: bool,
                         start_line: int = None, end_line: int = None) -> List[Dict]:
        """格式化文档内容"""
        indent = ' ' * tab_size if insert_spaces else '\t'
        lines = text.split('\n')
        total_lines = len(lines)

        if start_line is None:
            start_line = 0
        if end_line is None:
            end_line = total_lines - 1

        # 计算缩进级别
        formatted_lines = list(lines)
        indent_level = 0

        for i in range(start_line, end_line + 1):
            line = lines[i].strip()

            if not line:
                continue

            # 减少缩进：结束、否则、否则若、捕获、最终
            decrease_keywords = ['结束', '否则', '否则若', '捕获', '最终']
            for kw in decrease_keywords:
                if line.startswith(kw):
                    indent_level = max(0, indent_level - 1)
                    break

            # 应用缩进
            formatted_lines[i] = indent * indent_level + line

            # 增加缩进：如果...那么、遍历...、当...、段落...、类...、尝试...、匹配...
            if any(line.endswith(kw) for kw in ['：', ':']):
                if any(line.startswith(kw) for kw in
                       ['如果', '若', '遍历', '当', '段落', '类', '接口', '尝试', '匹配', '否则', '否则若', '捕获']):
                    indent_level += 1
                elif any(kw in line for kw in ['接收', '构造']):
                    indent_level += 1

        new_text = '\n'.join(formatted_lines)

        if new_text == text:
            return []

        return [{
            'range': {
                'start': {'line': start_line, 'character': 0},
                'end': {'line': end_line, 'character': len(lines[end_line])}
            },
            'newText': '\n'.join(formatted_lines[start_line:end_line + 1])
        }]

    def _handle_rename(self, params: Dict) -> Optional[Dict]:
        """处理重命名请求"""
        uri = params.get('textDocument', {}).get('uri', '')
        doc = self.doc_manager.get_document(uri)
        if not doc:
            return None

        position = params.get('position', {})
        new_name = params.get('newName', '')
        line = position.get('line', 0)
        character = position.get('character', 0)

        # 获取当前光标处的词
        line_text = doc.get_line(line)
        start = character
        end = character
        while start > 0:
            ch = line_text[start - 1]
            if ch.isalnum() or '\u4e00' <= ch <= '\u9fff':
                start -= 1
            else:
                break
        while end < len(line_text):
            ch = line_text[end]
            if ch.isalnum() or '\u4e00' <= ch <= '\u9fff':
                end += 1
            else:
                break
        old_name = line_text[start:end]

        if not old_name or not new_name:
            return None

        # 查找所有引用
        changes = {}
        for doc_uri, doc_obj in self.doc_manager.documents.items():
            doc_edits = []
            for i, doc_line in enumerate(doc_obj.lines):
                pos = 0
                while True:
                    idx = doc_line.find(old_name, pos)
                    if idx == -1:
                        break
                    # 检查是否是完整词（前后不是中文字符或字母数字）
                    before_ok = idx == 0 or not (
                        doc_line[idx - 1].isalnum() or '\u4e00' <= doc_line[idx - 1] <= '\u9fff'
                    )
                    after_ok = idx + len(old_name) >= len(doc_line) or not (
                        doc_line[idx + len(old_name)].isalnum() or
                        '\u4e00' <= doc_line[idx + len(old_name)] <= '\u9fff'
                    )
                    if before_ok and after_ok:
                        doc_edits.append({
                            'range': {
                                'start': {'line': i, 'character': idx},
                                'end': {'line': i, 'character': idx + len(old_name)}
                            },
                            'newText': new_name
                        })
                    pos = idx + len(old_name)

            if doc_edits:
                changes[doc_uri] = doc_edits

        if not changes:
            return None

        return {'changes': changes}

    def _handle_code_action(self, params: Dict) -> List[Dict]:
        """处理代码操作请求（快速修复）"""
        uri = params.get('textDocument', {}).get('uri', '')
        doc = self.doc_manager.get_document(uri)
        if not doc:
            return []

        context = params.get('context', {})
        diagnostics = context.get('diagnostics', [])
        code_actions = []

        for diag in diagnostics:
            msg = diag.get('message', '')
            d_range = diag.get('range', {})

            # 语法错误快速修复建议
            if '意外的标记' in msg:
                code_actions.append({
                    'title': '查看段言语法文档',
                    'kind': 'quickfix',
                    'diagnostics': [diag],
                    'command': {
                        'title': '打开语法文档',
                        'command': 'vscode.open',
                        'arguments': ['https://github.com/duan-lang/duan/blob/main/docs/syntax.md']
                    }
                })
            elif '名称未定义' in msg or '未定义' in msg:
                code_actions.append({
                    'title': '添加变量定义',
                    'kind': 'quickfix',
                    'diagnostics': [diag],
                    'edit': {
                        'changes': {
                            uri: [{
                                'range': d_range,
                                'newText': f'定义 {msg.split("'")[1] if "'" in msg else "变量"} 等于 空。\n'
                            }]
                        }
                    }
                })

        return code_actions

    def _handle_did_open(self, params: Dict):
        """处理文档打开"""
        text_doc = params.get('textDocument', {})
        uri = text_doc.get('uri')
        text = text_doc.get('text', '')
        self.doc_manager.open_document(uri, text)
        # 发布初始诊断
        self._publish_diagnostics(uri)
    
    def _handle_did_change(self, params: Dict):
        """处理文档更改"""
        text_doc = params.get('textDocument', {})
        uri = text_doc.get('uri')
        changes = params.get('contentChanges', [])
        self.doc_manager.update_document(uri, changes)
        # 重新发布诊断
        self._publish_diagnostics(uri)
    
    def _publish_diagnostics(self, uri: str):
        """发布诊断信息"""
        diagnostics = self.get_diagnostics(uri)
        notification = lsp_notification('textDocument/publishDiagnostics', {
            'uri': uri,
            'diagnostics': diagnostics
        })
        # 存储待发送的通知
        if not hasattr(self, '_pending_notifications'):
            self._pending_notifications = []
        self._pending_notifications.append(notification)
    
    def get_pending_notifications(self) -> List[Dict]:
        """获取待发送的通知"""
        if not hasattr(self, '_pending_notifications'):
            return []
        notifications = self._pending_notifications
        self._pending_notifications = []
        return notifications
    
    def get_diagnostics(self, uri: str) -> List[Dict]:
        """获取文档诊断信息（语法错误 + 类型错误）"""
        doc = self.doc_manager.get_document(uri)
        if not doc:
            return []

        diagnostics = []

        # 语法分析错误
        try:
            parser = DuanParser()
            ast = parser.parse(doc.text)
        except Exception as e:
            if hasattr(e, 'line') and hasattr(e, 'col'):
                line = max(0, e.line - 1)
                col = max(0, e.col - 1)
                # 尝试获取错误 token 的长度，用于精确高亮
                end_col = col + 1
                if hasattr(e, 'token_value') and e.token_value:
                    end_col = col + len(str(e.token_value))
                diagnostics.append({
                    'severity': 1,
                    'range': {
                        'start': {'line': line, 'character': col},
                        'end': {'line': line, 'character': end_col}
                    },
                    'message': str(e.message) if hasattr(e, 'message') else str(e),
                    'source': '段言'
                })
            else:
                diagnostics.append({
                    'severity': 1,
                    'range': {
                        'start': {'line': 0, 'character': 0},
                        'end': {'line': 0, 'character': 0}
                    },
                    'message': f'错误: {str(e)}',
                    'source': '段言'
                })
            return diagnostics

        # 类型检查诊断
        try:
            from type_inferencer import TypeInferencer
            from type_checker import create_checker_from_source

            inferencer = TypeInferencer()
            inferencer.infer(ast)

            for err in getattr(inferencer, 'errors', []):
                err_line = getattr(err, 'line', 0)
                err_col = getattr(err, 'col', 0)
                diagnostics.append({
                    'severity': 1,
                    'range': {
                        'start': {'line': max(0, err_line - 1), 'character': max(0, err_col - 1)},
                        'end': {'line': max(0, err_line - 1), 'character': max(0, err_col)}
                    },
                    'message': str(err),
                    'source': '段言类型'
                })

            checker = create_checker_from_source(doc.text)
            if checker.config.check_level.value > 0:
                check_results = checker.check(ast, inferencer)
                for r in check_results:
                    severity = 1 if r.is_error() else 2
                    r_line = max(0, getattr(r, 'line', 0) - 1)
                    r_col = max(0, getattr(r, 'col', 0))
                    diagnostics.append({
                        'severity': severity,
                        'range': {
                            'start': {'line': r_line, 'character': r_col},
                            'end': {'line': r_line, 'character': max(r_col, 1)}
                        },
                        'message': getattr(r, 'message', str(r)),
                        'source': '段言类型'
                    })
        except Exception:
            pass

        return diagnostics


def create_language_server():
    """创建 LSP 服务器"""
    return DuanLanguageServer()


# =============================================================================
# Stdio LSP 服务器入口
# =============================================================================

def run_stdio_server():
    """通过 stdio 运行 LSP 服务器"""
    import sys
    
    server = DuanLanguageServer()
    request_id = None
    
    def send_message(message: Dict):
        """发送 LSP 消息"""
        content = json.dumps(message, ensure_ascii=False)
        content_bytes = content.encode('utf-8')
        sys.stdout.write(f'Content-Length: {len(content_bytes)}\r\n\r\n')
        sys.stdout.buffer.write(content_bytes)
        sys.stdout.flush()
    
    def read_message() -> Optional[Dict]:
        """读取 LSP 消息"""
        # 读取 headers
        headers = {}
        while True:
            line = sys.stdin.readline()
            if not line:
                return None
            line = line.strip()
            if not line:
                break
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip().lower()] = value.strip()
        
        # 读取 content
        content_length = int(headers.get('content-length', '0'))
        if content_length <= 0:
            return None
        
        content = sys.stdin.buffer.read(content_length).decode('utf-8')
        return json.loads(content)
    
    while True:
        message = read_message()
        if message is None:
            break
        
        method = message.get('method')
        params = message.get('params', {})
        msg_id = message.get('id')
        
        if method == 'exit':
            break
        
        if method == 'shutdown':
            if msg_id is not None:
                send_message(lsp_response(msg_id, None))
            continue
        
        result = server.handle_request(method, params, msg_id)
        
        if result is not None and msg_id is not None:
            send_message(result)
        
        # 发送待处理的通知
        for notification in server.get_pending_notifications():
            send_message(notification)


if __name__ == '__main__':
    run_stdio_server()

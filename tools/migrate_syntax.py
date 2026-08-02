#!/usr/bin/env python3
"""
段言语法迁移脚本

将旧语法批量迁移到新语法：
1. 定义 x 等于 y  ->  设 x 为 y
2. 段落 名 接收 参数  ->  段落 名(参数)
3. 对象之属性  ->  对象的属性（成员访问符统一）

用法:
    python tools/migrate_syntax.py <文件或目录>
    python tools/migrate_syntax.py --dry-run <文件或目录>  # 预览模式
"""

import sys
import os
import re
from pathlib import Path


def migrate_assignment(content: str) -> tuple:
    """迁移赋值语法：定义 x 等于 y -> 设 x 为 y"""
    changes = []
    
    # 匹配：定义 标识符 等于
    # 注意：不匹配类属性定义（在类块中的 定义 属性名 等于）
    # 类属性定义上下文较复杂，暂不自动迁移
    pattern = re.compile(
        r'^(\s*)定义\s+(\S+)\s+等于\s+',
        re.MULTILINE
    )
    
    def replacer(m):
        indent, name = m.group(1), m.group(2)
        changes.append(f'  赋值: "{indent}定义 {name} 等于 ..." -> "{indent}设 {name} 为 ..."')
        return f'{indent}设 {name} 为 '
    
    new_content = pattern.sub(replacer, content)
    return new_content, changes


def migrate_paragraph_params(content: str) -> tuple:
    """迁移函数参数语法：段落 名 接收 参数 -> 段落 名(参数)"""
    changes = []
    
    # 匹配：段落/段 名 接收 参数列表
    # 参数列表以冒号或换行结束
    # 注意：需要处理多字函数名（如 计算总和）
    pattern = re.compile(
        r'^(\s*)(段落|段)\s+(\S+)\s+接收\s+(.+?)(\s*:\s*)$',
        re.MULTILINE
    )
    
    def replacer(m):
        indent, kw, name, params, colon = m.groups()
        # 清理参数：将空格分隔的参数改为逗号分隔
        # 但如果参数已经有逗号，保持原样
        params = params.strip()
        changes.append(f'  函数参数: "{kw} {name} 接收 {params}:" -> "{kw} {name}({params}):"')
        return f'{indent}{kw} {name}({params}){colon}'
    
    new_content = pattern.sub(replacer, content)
    return new_content, changes


def migrate_member_access(content: str) -> tuple:
    """迁移成员访问符：对象之属性 -> 对象的属性
    
    只迁移真正的成员访问场景：标识符 + 之 + 属性名（标识符）。
    排除以下情况：
    - 推导式中的"之"（后面跟着 列表/集合/字典/映射/筛选）
    - 变量名中包含"之"字（如 平方差之和、倒数之和）
    - 字符串内容中的"之"
    """
    changes = []
    
    comprehension_words = {'列表', '集合', '字典', '映射', '筛选'}
    
    # 匹配模式：标识符（字母/中文/下划线/数字）+ 之 + 属性名
    # 前后必须是标识符字符，且前面不能是引号
    # 之 后面跟的也必须是合法的属性名（标识符）
    pattern = re.compile(
        r'(?<![\w\'"])([\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z_0-9]*?)之([\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z_0-9]*)'
    )
    
    def replace_zhi(m):
        prefix = m.group(1)
        next_word = m.group(2)
        if next_word in comprehension_words:
            return m.group(0)
        # 检查 prefix 是否以"和"等常见变量名后缀结尾
        # 这些是变量名的一部分，不是成员访问
        if prefix.endswith(('和', '差', '积', '商', '数', '值')):
            return m.group(0)
        changes.append(f'  成员访问: "{prefix}之{next_word}" -> "{prefix}的{next_word}"')
        return f'{prefix}的{next_word}'
    
    new_content = pattern.sub(replace_zhi, content)
    return new_content, changes


def migrate_file(filepath: str, dry_run: bool = False) -> list:
    """迁移单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f'  [错误] 无法读取 {filepath}: {e}')
        return []
    
    all_changes = []
    
    # 1. 赋值语法迁移
    content, changes = migrate_assignment(content)
    all_changes.extend(changes)
    
    # 2. 函数参数语法迁移
    content, changes = migrate_paragraph_params(content)
    all_changes.extend(changes)
    
    # 3. 成员访问符迁移
    content, changes = migrate_member_access(content)
    all_changes.extend(changes)
    
    if all_changes and not dry_run:
        # 备份原文件
        backup_path = filepath + '.bak'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 写入新内容
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'  [已迁移] {filepath} ({len(all_changes)} 处变更，备份: {backup_path})')
    elif all_changes and dry_run:
        print(f'  [预览] {filepath} ({len(all_changes)} 处变更)')
    
    for change in all_changes:
        print(change)
    
    return all_changes


def main():
    if len(sys.argv) < 2:
        print('用法: python tools/migrate_syntax.py [--dry-run] <文件或目录>')
        sys.exit(1)
    
    dry_run = '--dry-run' in sys.argv
    paths = [a for a in sys.argv[1:] if not a.startswith('--')]
    
    if not paths:
        print('错误: 请指定文件或目录')
        sys.exit(1)
    
    total_changes = 0
    
    for path_str in paths:
        path = Path(path_str)
        
        if path.is_file() and path.suffix == '.duan':
            print(f'\n处理: {path}')
            total_changes += len(migrate_file(str(path), dry_run))
        elif path.is_dir():
            duan_files = list(path.rglob('*.duan'))
            print(f'\n扫描目录: {path} ({len(duan_files)} 个 .duan 文件)')
            for f in duan_files:
                total_changes += len(migrate_file(str(f), dry_run))
        else:
            print(f'\n跳过: {path} (不是 .duan 文件或目录)')
    
    print(f'\n{"=" * 60}')
    print(f'  总计: {total_changes} 处变更')
    if dry_run:
        print(f'  (预览模式，未实际修改文件)')
    print(f'{"=" * 60}')


if __name__ == '__main__':
    main()

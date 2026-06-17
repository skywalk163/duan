#!/usr/bin/env python3
"""
快速修复ANTLR语法规则的脚本
自动修改DuanLangParser.g4中的语法规则，使其符合统一规范
"""

import re
from pathlib import Path

def fix_parser_grammar():
    """修复DuanLangParser.g4的语法规则"""
    
    parser_file = Path(__file__).parent.parent / 'antlrparser' / 'DuanLangParser.g4'
    
    with open(parser_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 备份原文件
    backup_file = parser_file.with_suffix('.g4.backup')
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] 已备份原文件到: {backup_file}")
    
    # 修复1：段落定义 - 去掉BOOK_L BOOK_R
    old_paragraph = r'''paragraphDef
    : K_SEGMENT \( BOOK_L ID BOOK_R \| ID \) \( K_RECEIVE paramList \)\? \( K_RETURN typeAnnotation \)\?
      COLON
      block
      K_END PERIOD\?
    ;'''
    
    new_paragraph = '''paragraphDef
    : K_SEGMENT ID ( K_RECEIVE paramList )? ( K_RETURN typeAnnotation )?
      COLON
      block
      K_END PERIOD?
    ;'''
    
    content = re.sub(old_paragraph, new_paragraph, content, flags=re.MULTILINE)
    print("[OK] 已修复段落定义语法")
    
    # 修复2：方法定义 - 统一使用K_SEGMENT和K_RECEIVE
    old_method = r'''methodDef
    : \( K_METHOD \| K_SEGMENT \) ID \( LPAREN paramList\? RPAREN \| K_RECEIVE paramList \)\? \( K_RETURN typeAnnotation \)\?
      COLON block K_END PERIOD\?
    ;'''
    
    new_method = '''methodDef
    : K_SEGMENT ID ( K_RECEIVE paramList )? ( K_RETURN typeAnnotation )?
      COLON block K_END PERIOD?
    ;'''
    
    content = re.sub(old_method, new_method, content, flags=re.MULTILINE)
    print("[OK] 已修复方法定义语法")
    
    # 修复3：构造函数 - 使用K_RECEIVE而不是LPAREN
    old_constructor = r'''constructorDef
    : K_CONSTRUCTOR LPAREN paramList\? RPAREN COLON block K_END PERIOD\?
    ;'''
    
    new_constructor = '''constructorDef
    : K_CONSTRUCTOR ( K_RECEIVE paramList )? COLON block K_END PERIOD?
    ;'''
    
    content = re.sub(old_constructor, new_constructor, content, flags=re.MULTILINE)
    print("[OK] 已修复构造函数语法")
    
    # 修复4：属性声明 - 使用K_AS而不是COLON
    old_attribute = r'''attributeDecl
    : K_ATTRIBUTE ID \( COLON typeAnnotation \)\? \( K_EQUAL expr \)\? PERIOD\?
    ;'''
    
    new_attribute = '''attributeDecl
    : K_ATTRIBUTE ID ( K_AS typeAnnotation )? ( K_EQUAL expr )? PERIOD?
    ;'''
    
    content = re.sub(old_attribute, new_attribute, content, flags=re.MULTILINE)
    print("[OK] 已修复属性声明语法")
    
    # 保存修改后的文件
    with open(parser_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] 已保存修改后的文件: {parser_file}")
    
    print("\n下一步：")
    print("1. cd antlrparser")
    print("2. java -jar ../antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor DuanLangLexer.g4")
    print("3. java -jar ../antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor DuanLangParser.g4")
    print("4. python ../compile.py test_unified.duan")

if __name__ == '__main__':
    print("段言编程语言 - ANTLR语法规则修复")
    print("=" * 60)
    fix_parser_grammar()

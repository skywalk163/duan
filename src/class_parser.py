# -*- coding: utf-8 -*-
"""
段言（Duan）编程语言 - 类定义解析器扩展

支持类定义语法：
- 类 学生：...类结束
- 属性 姓名
- 构造(姓名, 年龄)：...
- 方法 定义(参数)：...
- 继承 父类
"""

from typing import List, Optional
from lexer import Lexer
from tokens import Token, TokenType
from keywords import KEYWORDS_CLASS, KEYWORDS_RESERVED
from ast_nodes import (
    ClassDefinition, AttributeDeclaration, MethodDefinition,
    Parameter, ASTNode, Identifier
)


class ClassParser:
    """类定义解析器"""
    
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.tokens = []
        self.pos = 0
    
    def parse_class_definition(self, tokens: List[Token], pos: int) -> tuple:
        """
        解析类定义
        
        语法：
        类 类名 [继承 父类]：
          属性列表
          方法定义
        类结束
        
        返回：(ClassDefinition节点, 新位置)
        """
        self.tokens = tokens
        self.pos = pos
        
        # 消耗 '类' 关键字
        if not self._check_keyword('类'):
            raise SyntaxError(f"期望 '类' 关键字")
        
        line = self.tokens[self.pos].line
        column = self.tokens[self.pos].column
        self.pos = self._next_pos()
        
        # 解析类名
        class_name = self._expect_identifier()
        
        # 解析继承关系（可选）
        base_classes = []
        if self._check_keyword('继承'):
            self.pos = self._next_pos()
            base_classes = [self._expect_identifier()]
        
        # 消耗冒号
        if not self._check_punctuation('：'):
            raise SyntaxError(f"期望 '：' (冒号)")
        self.pos = self._next_pos()
        
        # 解析类体
        attributes = []
        methods = []
        
        while not self._check_keyword('类结束') and not self._at_end():
            # 解析属性声明
            if self._check_keyword('属性'):
                attr = self._parse_attribute()
                attributes.append(attr)
            # 解析方法定义
            elif self._check_keyword('构造'):
                method = self._parse_method(is_constructor=True)
                methods.append(method)
            elif self._check_identifier() and self._peek_next_is_punctuation('（'):
                # 普通方法定义
                method = self._parse_method(is_constructor=False)
                methods.append(method)
            else:
                # 跳过未知内容
                self.pos = self._next_pos()
        
        # 消耗 '类结束' 关键字（如果存在）
        if self._check_keyword('类结束'):
            self.pos = self._next_pos()
        
        return ClassDefinition(
            line=line,
            column=column,
            name=class_name,
            base_classes=base_classes,
            attributes=attributes,
            methods=methods
        ), self.pos
    
    def _parse_attribute(self) -> AttributeDeclaration:
        """解析属性声明"""
        line = self.tokens[self.pos].line
        column = self.tokens[self.pos].column
        
        # 消耗 '属性' 关键字
        self.pos = self._next_pos()
        
        # 解析属性名
        name = self._expect_identifier()
        
        # 解析类型注解（可选）
        type_annotation = None
        if self._check_punctuation('：'):
            self.pos = self._next_pos()
            type_annotation = self._expect_identifier()
        
        # 解析默认值（可选）
        default_value = None
        if self._check_keyword('等于'):
            self.pos = self._next_pos()
            default_value = self._parse_value()
        
        return AttributeDeclaration(
            line=line,
            column=column,
            name=name,
            type_annotation=type_annotation,
            default_value=default_value
        )
    
    def _parse_method(self, is_constructor: bool) -> MethodDefinition:
        """解析方法定义"""
        line = self.tokens[self.pos].line
        column = self.tokens[self.pos].column
        
        # 解析方法名
        if is_constructor:
            # 消耗 '构造' 关键字
            self.pos = self._next_pos()
            name = '构造'
        else:
            name = self._expect_identifier()
        
        # 解析参数列表
        parameters = self._parse_parameters()
        
        # 消耗冒号
        if not self._check_punctuation('：'):
            raise SyntaxError(f"期望 '：' (冒号)")
        self.pos = self._next_pos()
        
        # 解析方法体（简化版，只收集到下一个方法或类结束）
        body = []
        while not self._is_end_of_method() and not self._at_end():
            # 简化：跳过语句
            if self._check_keyword('返回'):
                self.pos = self._next_pos()
                value = self._parse_value()
                body.append(('return', value))
            elif self._check_keyword('定义'):
                self.pos = self._next_pos()
                var_name = self._expect_identifier()
                if self._check_keyword('等于'):
                    self.pos = self._next_pos()
                    var_value = self._parse_value()
                    body.append(('var', var_name, var_value))
            else:
                self.pos = self._next_pos()
        
        return MethodDefinition(
            line=line,
            column=column,
            name=name,
            parameters=parameters,
            body=body,
            is_constructor=is_constructor
        )
    
    def _parse_parameters(self) -> List[Parameter]:
        """解析参数列表"""
        parameters = []
        
        # 消耗左括号
        if not self._check_punctuation('（'):
            return parameters  # 无参数
        
        self.pos = self._next_pos()
        
        # 解析参数
        while not self._check_punctuation('）') and not self._at_end():
            param_name = self._expect_identifier()
            
            # 解析类型注解（可选）
            type_annotation = None
            if self._check_punctuation('：'):
                self.pos = self._next_pos()
                type_annotation = self._expect_identifier()
            
            parameters.append(Parameter(
                line=self.tokens[self.pos-1].line,
                column=self.tokens[self.pos-1].column,
                name=param_name,
                type_annotation=type_annotation
            ))
            
            # 消耗逗号（如果有）
            if self._check_punctuation('，'):
                self.pos = self._next_pos()
        
        # 消耗右括号
        if self._check_punctuation('）'):
            self.pos = self._next_pos()
        
        return parameters
    
    def _parse_value(self) -> ASTNode:
        """解析值（简化版）"""
        line = self.tokens[self.pos].line
        column = self.tokens[self.pos].column
        
        if self._check_number():
            value = self.tokens[self.pos].value
            self.pos = self._next_pos()
            return ASTNode(line=line, column=column)  # 简化
        
        if self._check_string():
            value = self.tokens[self.pos].value
            self.pos = self._next_pos()
            return ASTNode(line=line, column=column)  # 简化
        
        if self._check_identifier():
            name = self.tokens[self.pos].value
            self.pos = self._next_pos()
            return Identifier(line=line, column=column, name=name)
        
        # 默认：跳过
        self.pos = self._next_pos()
        return ASTNode(line=line, column=column)
    
    # =========================================================================
    # 辅助方法
    # =========================================================================
    
    def _check_keyword(self, keyword: str) -> bool:
        """检查当前是否为指定关键字"""
        if self._at_end():
            return False
        token = self.tokens[self.pos]
        return token.type == TokenType.KEYWORD and token.value == keyword
    
    def _check_identifier(self) -> bool:
        """检查当前是否为标识符"""
        if self._at_end():
            return False
        return self.tokens[self.pos].type == TokenType.IDENTIFIER
    
    def _check_number(self) -> bool:
        """检查当前是否为数字"""
        if self._at_end():
            return False
        return self.tokens[self.pos].type == TokenType.NUMBER
    
    def _check_string(self) -> bool:
        """检查当前是否为字符串"""
        if self._at_end():
            return False
        return self.tokens[self.pos].type == TokenType.STRING
    
    def _check_punctuation(self, punct: str) -> bool:
        """检查当前是否为指定标点"""
        if self._at_end():
            return False
        token = self.tokens[self.pos]
        return token.type == TokenType.PUNCTUATION and token.value == punct
    
    def _peek_next_is_punctuation(self, punct: str) -> bool:
        """检查下一个是否为指定标点"""
        if self.pos + 1 >= len(self.tokens):
            return False
        token = self.tokens[self.pos + 1]
        return token.type == TokenType.PUNCTUATION and token.value == punct
    
    def _expect_identifier(self) -> str:
        """期望并消耗标识符"""
        if not self._check_identifier():
            raise SyntaxError(f"期望标识符，实际得到 {self.tokens[self.pos]}")
        name = self.tokens[self.pos].value
        self.pos = self._next_pos()
        return name
    
    def _is_end_of_method(self) -> bool:
        """检查是否到达方法结束"""
        return (self._check_keyword('属性') or 
                self._check_keyword('构造') or 
                self._check_keyword('类结束') or
                (self._check_identifier() and self._peek_next_is_punctuation('（')))
    
    def _at_end(self) -> bool:
        """检查是否到达token流末尾"""
        return self.pos >= len(self.tokens)
    
    def _next_pos(self) -> int:
        """返回下一个位置"""
        return self.pos + 1

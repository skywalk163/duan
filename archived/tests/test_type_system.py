#!/usr/bin/env python3
"""
段言类型推断系统 - 综合测试套件

测试覆盖：
1. 基本类型推断（数字、字符串、布尔、空值）
2. 变量类型追踪
3. 二元运算类型推断（加法/连接操作）
4. 嵌套表达式类型推断
5. 函数调用类型推断
6. 类实例化类型推断
7. 复杂场景测试
"""

import sys
import os

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'antlrparser'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from antlr4 import InputStream, CommonTokenStream
from DuanLangLexer import DuanLangLexer
from DuanLangParser import DuanLangParser
from duan_visitor import DuanLangASTBuilder
from code_generator_unified import UnifiedCodeGenerator


class TestResult:
    """测试结果"""
    def __init__(self, name: str, passed: bool, message: str = ""):
        self.name = name
        self.passed = passed
        self.message = message
    
    def __str__(self):
        status = "✓ 通过" if self.passed else "✗ 失败"
        result = f"{status}: {self.name}"
        if self.message:
            result += f"\n  {self.message}"
        return result


class TypeInferenceTestSuite:
    """类型推断测试套件"""
    
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
    
    def add_result(self, result: TestResult):
        """添加测试结果"""
        self.results.append(result)
        if result.passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def run_test(self, name: str, code: str, expected_output: str = None):
        """运行单个测试"""
        try:
            # 解析代码
            input_stream = InputStream(code)
            lexer = DuanLangLexer(input_stream)
            token_stream = CommonTokenStream(lexer)
            parser = DuanLangParser(token_stream)
            tree = parser.program()
            
            # 转换为AST
            visitor = DuanLangASTBuilder()
            ast = visitor.visit(tree)
            
            # 生成Python代码
            gen = UnifiedCodeGenerator()
            py_code = gen.generate(ast)
            
            # 执行生成的代码
            output = self._execute_code(py_code)
            
            # 验证结果
            if expected_output is not None:
                if output == expected_output:
                    self.add_result(TestResult(name, True))
                else:
                    self.add_result(TestResult(
                        name, False,
                        f"期望输出: {expected_output}\n实际输出: {output}"
                    ))
            else:
                # 只验证代码生成成功
                self.add_result(TestResult(name, True))
                
        except Exception as e:
            self.add_result(TestResult(name, False, str(e)))
    
    def _execute_code(self, code: str) -> str:
        """执行Python代码并捕获输出"""
        import io
        from contextlib import redirect_stdout
        
        output = io.StringIO()
        try:
            with redirect_stdout(output):
                exec(code, {})
        except Exception as e:
            return f"Error: {e}"
        
        return output.getvalue().strip()
    
    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "=" * 60)
        print("测试摘要")
        print("=" * 60)
        print(f"总计: {self.passed + self.failed}")
        print(f"通过: {self.passed}")
        print(f"失败: {self.failed}")
        print(f"成功率: {(self.passed / (self.passed + self.failed) * 100):.1f}%" if self.passed + self.failed > 0 else "N/A")
        print("=" * 60)
        
        if self.failed > 0:
            print("\n失败的测试:")
            for result in self.results:
                if not result.passed:
                    print(result)
    
    def run_all(self):
        """运行所有测试"""
        print("=" * 60)
        print("段言类型推断系统 - 综合测试套件")
        print("=" * 60)
        
        # 测试1: 纯数字加法
        self.run_test(
            "纯数字加法",
            "设 甲 为 3 加 5。\n打印(甲)。",
            "8"
        )
        
        # 测试2: 纯字符串连接
        self.run_test(
            "纯字符串连接",
            "设 甲 为 \"你好\" 加 \"世界\"。\n打印(甲)。",
            "你好世界"
        )
        
        # 测试3: 字符串与数字混合（字符串在前）
        self.run_test(
            "字符串与数字混合（字符串在前）",
            "设 数字 为 42。\n打印(\"答案是：\" 加 数字)。",
            "答案是：42"
        )
        
        # 测试4: 字符串与数字混合（数字在前）
        self.run_test(
            "字符串与数字混合（数字在前）",
            "设 数字 为 42。\n打印(数字 加 \"是答案\")。",
            "42是答案"
        )
        
        # 测试5: 多个字符串连接
        self.run_test(
            "多个字符串连接",
            "设 姓名 为 \"张三\"。\n设 年龄 为 25。\n打印(\"姓名：\" 加 姓名 加 \"，年龄：\" 加 年龄)。",
            "姓名：张三，年龄：25"
        )
        
        # 测试6: 表达式结果与字符串连接
        self.run_test(
            "表达式结果与字符串连接",
            "设 计算 为 5 乘 8。\n打印(\"5 × 8 = \" 加 计算)。",
            "5 × 8 = 40"
        )
        
        # 测试7: 嵌套表达式（纯数字）
        self.run_test(
            "嵌套表达式（纯数字）",
            "设 结果 为 (1 加 2) 乘 (3 加 4)。\n打印(结果)。",
            "21"
        )
        
        # 测试8: 嵌套表达式（字符串连接）
        self.run_test(
            "嵌套表达式（字符串连接）",
            "设 结果 为 (\"你好\" 加 \"，\") 加 \"世界\"。\n打印(结果)。",
            "你好，世界"
        )
        
        # 测试9: 英文加号
        self.run_test(
            "英文加号（数字加法）",
            "设 甲 为 10 加 20。\n打印(甲)。",
            "30"
        )
        
        # 测试10: 英文加号（字符串连接）
        self.run_test(
            "英文加号（字符串连接）",
            "设 甲 为 \"Hello\" 加 \" \" 加 \"World\"。\n打印(甲)。",
            "Hello World"
        )
        
        # 测试11: 数字减法
        self.run_test(
            "数字减法",
            "设 甲 为 10 减 3。\n打印(甲)。",
            "7"
        )
        
        # 测试12: 数字乘法
        self.run_test(
            "数字乘法",
            "设 甲 为 6 乘 7。\n打印(甲)。",
            "42"
        )
        
        # 测试13: 数字除法
        self.run_test(
            "数字除法",
            "设 甲 为 20 除 4。\n打印(甲)。",
            "5.0"
        )
        
        # 测试14: 比较运算
        self.run_test(
            "比较运算",
            "设 甲 为 10 大于 5。\n打印(甲)。",
            "True"
        )
        
        # 测试15: 布尔运算
        self.run_test(
            "布尔运算",
            "设 甲 为 1 等于 1。\n打印(甲)。",
            "True"
        )
        
        # 测试16: 三元表达式（使用条件语句）
        self.run_test(
            "三元表达式（使用条件语句）",
            "设 甲 为 1。\n如果 甲 大于 0:\n    设 乙 为 \"正数\"。\n否则:\n    设 乙 为 \"负数\"。\n结束。\n打印(乙)。",
            "正数"
        )
        
        # 测试17: 复杂混合表达式
        self.run_test(
            "复杂混合表达式",
            "设 数字 为 123。\n设 文本 为 \"数字是：\" 加 数字。\n打印(文本)。",
            "数字是：123"
        )
        
        # 测试18: 列表元素与字符串连接
        self.run_test(
            "列表长度与字符串连接",
            "设 列表 为 [1, 2, 3]。\n设 长度 为 长(列表)。\n打印(\"列表长度：\" 加 长度)。",
            "列表长度：3"
        )
        
        # 测试19: 变量重新赋值
        self.run_test(
            "变量重新赋值（类型变化）",
            "设 甲 为 10。\n设 甲 为 \"字符串\"。\n打印(\"甲是：\" 加 甲)。",
            "甲是：字符串"
        )
        
        # 测试20: 段落（函数）中的类型推断
        self.run_test(
            "段落中的类型推断",
            "段落 加法 接收 甲, 乙:\n    返回 甲 加 乙。\n结束。\n打印(加法(3, 5))。",
            "8"
        )
        
        # 测试21: 条件语句中的类型推断
        self.run_test(
            "条件语句中的类型推断",
            "设 甲 为 10。\n如果 甲 大于 5:\n    设 乙 为 \"大\"。\n否则:\n    设 乙 为 \"小\"。\n结束。\n打印(乙)。",
            "大"
        )
        
        # 测试22: 循环语句中的类型推断
        self.run_test(
            "循环语句中的类型推断",
            "设 计数 为 0。\n当 计数 小于 3:\n    设 计数 为 计数 加 1。\n结束。\n打印(\"计数：\" 加 计数)。",
            "计数：3"
        )
        
        # 测试23: 空值处理
        self.run_test(
            "空值与字符串连接",
            "设 甲 为 空。\n打印(\"甲是：\" 加 甲)。",
            "甲是：None"
        )
        
        # 测试24: 布尔值与字符串连接
        self.run_test(
            "布尔值与字符串连接",
            "设 甲 为 真。\n打印(\"甲是：\" 加 甲)。",
            "甲是：True"
        )
        
        # 测试25: 浮点数与字符串连接
        self.run_test(
            "浮点数与字符串连接",
            "设 甲 为 3.14。\n打印(\"圆周率：\" 加 甲)。",
            "圆周率：3.14"
        )
        
        self.print_summary()
        
        return self.failed == 0


def main():
    """主函数"""
    suite = TypeInferenceTestSuite()
    success = suite.run_all()
    
    if success:
        print("\n所有测试通过！")
        sys.exit(0)
    else:
        print("\n部分测试失败，请检查上述失败项。")
        sys.exit(1)


if __name__ == '__main__':
    main()
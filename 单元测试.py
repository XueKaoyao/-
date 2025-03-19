import unittest
from io import StringIO
from unittest.mock import patch, mock_open
import random
import fractions
import sys

# 假设程序的功能已经保存在四则运算脚本中，导入需要测试的函数
from 四则运算 import generate_fraction, generate_expression, evaluate_expression, generate_questions_and_answers, \
    write_to_files, grade_answers


class TestArithmeticOperations(unittest.TestCase):

    # 测试 generate_fraction 函数，确保生成的是真分数
    def test_generate_fraction(self):
        fraction = generate_fraction(10, 10)
        numerator, denominator = map(int, fraction.split('/'))
        self.assertTrue(1 <= numerator < denominator <= 10)

    # 测试 generate_expression 函数，确保表达式按预期生成
    def test_generate_expression(self):
        expr = generate_expression(10, 3)  # 生成最多3个运算符的表达式
        self.assertTrue(isinstance(expr, str))  # 确保返回类型是字符串
        self.assertTrue(any(op in expr for op in ['+', '-', '*', '/']))  # 包含四则运算符
        self.assertTrue('=' in expr)  # 包含等号

    # 测试 evaluate_expression 函数，确保计算结果正确
    def test_evaluate_expression(self):
        # 测试加法
        result = evaluate_expression("2 + 3")
        self.assertEqual(result, "5")

        # 测试减法
        result = evaluate_expression("5 - 3")
        self.assertEqual(result, "2")

        # 测试乘法
        result = evaluate_expression("2 * 3")
        self.assertEqual(result, "6")

        # 测试除法
        result = evaluate_expression("6 / 2")
        self.assertEqual(result, "3")

        # 测试真分数运算
        result = evaluate_expression("1/3 + 2/3")
        self.assertEqual(result, "1")

        # 测试除法的真分数
        result = evaluate_expression("1/6 + 1/8")
        self.assertEqual(result, "7/24")

    # 测试 generate_questions_and_answers 函数，确保生成题目和答案
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_questions_and_answers(self, mock_file):
        # 生成3道题目，数值范围为10
        questions, answers = generate_questions_and_answers(3, 10)

        # 验证题目数量
        self.assertEqual(len(questions), 3)
        self.assertEqual(len(answers), 3)

        # 验证题目格式
        for question in questions:
            self.assertTrue('=' in question)  # 确保每道题目包含等号
        for answer in answers:
            self.assertTrue(answer)  # 确保每个答案不为空

        # 验证写入文件
        mock_file.assert_called_with('Exercises.txt', 'w')
        mock_file().write.assert_called()

    # 测试 grade_answers 函数，确保能够正确批改答案并生成成绩
    @patch('builtins.open', new_callable=mock_open)
    def test_grade_answers(self, mock_file):
        # 模拟题目文件内容
        exercises = [
            "2 + 3 = ",
            "4 - 1 = ",
            "1/3 + 2/3 = "
        ]
        # 模拟答案文件内容
        answers = [
            "5",
            "3",
            "1"
        ]

        mock_file.return_value.read.side_effect = ["\n".join(exercises), "\n".join(answers)]

        # 执行批改
        grade_answers('Exercises.txt', 'Answers.txt')

        # 验证 Grade.txt 文件是否正确生成
        mock_file.assert_called_with("Grade.txt", 'w')
        mock_file().write.assert_called_with("Correct: 3 (1, 2, 3)\nWrong: 0 ()\n")

    # 测试 main 函数，确保程序正确调用
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.argv', new=['program', '-n', '3', '-r', '10'])
    def test_main_with_args(self, mock_file):
        # 模拟主函数执行
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            sys.argv = ['program', '-n', '3', '-r', '10']
            from 四则运算 import main  # 引入并调用main函数
            main()

            # 验证文件写入
            mock_file.assert_called_with('Exercises.txt', 'w')
            mock_file().write.assert_called()

    # 测试 main 函数，确保没有参数时报错
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_without_args(self, mock_stdout):
        sys.argv = ['program']
        from 四则运算 import main  # 引入并调用main函数
        main()
        output = mock_stdout.getvalue().strip()
        self.assertIn("请在命令行输入", output)  # 检查提示信息是否出现


if __name__ == "__main__":
    unittest.main()

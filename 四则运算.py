import random
import fractions
import sys
import cProfile

def generate_fraction(numerator_limit, denominator_limit):
    # 生成真分数，保证分母不为1
    while True:
        numerator = random.randint(1, numerator_limit)
        denominator = random.randint(2, denominator_limit)
        if numerator < denominator:  # 确保是一个真分数
            return f"{numerator}/{denominator}"

def generate_expression(range_limit, num_operations):
    # 生成四则运算表达式
    operators = ['+', '-', '*', '/']
    expression = str(random.randint(0, range_limit - 1))  # 起始为一个自然数

    for _ in range(num_operations):
        operator = random.choice(operators)
        if operator == '/':
            # 生成除法表达式时，需要确保其结果是一个真分数
            numerator = random.randint(1, range_limit - 1)
            denominator = random.randint(2, range_limit - 1)
            expression += f" {operator} {numerator}/{denominator}"
        else:
            expression += f" {operator} {random.randint(0, range_limit - 1)}"

    return expression

def evaluate_expression(expr):
    # 计算表达式的结果
    try:
        result = eval(expr.replace("/", "//"))
        if isinstance(result, int):
            return str(result)
        else:
            # 确保除法结果是一个真分数
            fraction = fractions.Fraction(result).limit_denominator()
            if fraction.denominator != 1:
                return f"{fraction.numerator}/{fraction.denominator}"
            else:
                return str(fraction.numerator)
    except ZeroDivisionError:
        return "Error"  # 除0错误

def generate_questions_and_answers(num_questions, range_limit):
    questions = []
    answers = []

    for _ in range(num_questions):
        num_operations = random.randint(1, 3)
        expr = generate_expression(range_limit, num_operations)
        answer = evaluate_expression(expr)
        questions.append(f"{expr} =")
        answers.append(answer)

    return questions, answers

def write_to_files(questions, answers):
    # 将问题和答案写入文件
    with open("Exercises.txt", "w") as f_questions, open("Answers.txt", "w") as f_answers:
        for question in questions:
            f_questions.write(question + "\n")
        for answer in answers:
            f_answers.write(answer + "\n")

def grade_answers(exercise_file, answer_file):
    # 根据给定的题目文件和答案文件检查正确答案
    with open(exercise_file, "r") as f_questions, open(answer_file, "r") as f_answers:
        questions = f_questions.readlines()
        answers = f_answers.readlines()

    correct = []
    wrong = []

    for i, (question, answer) in enumerate(zip(questions, answers)):
        question = question.strip().replace(" =", "")
        correct_answer = evaluate_expression(question)
        if correct_answer == answer.strip():
            correct.append(i + 1)
        else:
            wrong.append(i + 1)

    with open("Grade.txt", "w") as f_grade:
        f_grade.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
        f_grade.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")

def main():
    if len(sys.argv) < 3:
        print("请在命令行输入: python 四则运算.py -n [生成题目的个数] -r [题目中数值（自然数、真分数和真分数分母）的范围]")
        return

    num_questions = 10
    range_limit = 10
    exercise_file = ""
    answer_file = ""

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-n':
            num_questions = int(sys.argv[i + 1])
        elif sys.argv[i] == '-r':
            range_limit = int(sys.argv[i + 1])
        elif sys.argv[i] == '-e':
            exercise_file = sys.argv[i + 1]
        elif sys.argv[i] == '-a':
            answer_file = sys.argv[i + 1]
    if exercise_file and answer_file:
        grade_answers(exercise_file, answer_file)
    else:
        questions, answers = generate_questions_and_answers(num_questions, range_limit)
        write_to_files(questions, answers)



if __name__ == "__main__":
    main()
# 性能分析
cProfile.run('main()')
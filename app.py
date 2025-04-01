from flask import Flask, request, render_template
import re
from sympy import symbols, Eq, solve, diff, integrate, pi

app = Flask(__name__)

# Dữ liệu khái niệm
math_concepts = {
    "hàm số": "Hàm số là một quy tắc mà với mỗi giá trị của biến độc lập (x), ta gán một giá trị duy nhất của biến phụ thuộc (y).",
    "phương trình": "Phương trình là một đẳng thức chứa biến số, ví dụ x + 2 = 5.",
    "đạo hàm": "Đạo hàm của một hàm số cho biết tốc độ thay đổi của hàm tại một điểm, thường ký hiệu là f'(x).",
    "tích phân": "Tích phân là phép toán ngược của đạo hàm, dùng để tính diện tích, thể tích, v.v."
}

def preprocess_equation(equation):
    return equation.replace("x^2", "x**2")

def solve_linear_equation(equation_str):
# giải 2*x + 3 = 7 
    try:
        x = symbols('x')
        left, right = equation_str.replace("giải", "").strip().split('=')
        eq = Eq(eval(left), eval(right))
        solution = solve(eq, x)
        return f"Nghiệm của phương trình là: {solution}"
    except:
        return "Mình không giải được phương trình này, bạn kiểm tra lại nhé!"

def solve_quadratic_equation(equation_str):
# giải x^2 - 5*x + 6 = 0
    try:
        equation_str = preprocess_equation(equation_str)
        x = symbols('x')
        left, right = equation_str.replace("giải", "").strip().split('=')
        eq = Eq(eval(left), eval(right))
        solutions = solve(eq, x)
        return f"Nghiệm của phương trình bậc hai là: {solutions}"
    except:
        return "Mình không giải được phương trình này, bạn kiểm tra lại nhé!"

def calculate_derivative(expression):
# tính đạo hàm x**2 + 3*x
    try:
        x = symbols('x')
        expr = eval(expression.replace("tính đạo hàm", "").strip())
        derivative = diff(expr, x)
        return f"Đạo hàm của {expr} là: {derivative}"
    except:
        return "Mình không tính được đạo hàm này, bạn kiểm tra lại nhé!"

def calculate_integral(expression):
# tính tích phân 2*x + 1
    try:
        x = symbols('x')
        expr = eval(expression.replace("tính tích phân", "").strip())
        integral = integrate(expr, x)
        return f"Tích phân của {expr} là: {integral} + C"
    except:
        return "Mình không tính được tích phân này, bạn kiểm tra lại nhé!"

def calculate_circle_area(radius_str):
# diện tích hình tròn bán kính 3
    try:
        radius = float(radius_str.replace("diện tích hình tròn bán kính", "").strip())
        area = pi * radius**2
        return f"Diện tích hình tròn với bán kính {radius} là: {area.evalf()}"
    except:
        return "Mình không tính được diện tích, bạn kiểm tra lại nhé!"

def get_response(user_input):
    user_input = user_input.lower()
    concept_keywords = ["là gì", "nghĩa là", "định nghĩa"]
    for concept, explanation in math_concepts.items():
        if concept in user_input and any(keyword in user_input for keyword in concept_keywords):
            return explanation
        if concept in user_input and "?" in user_input:
            return explanation

    if "giải" in user_input:
        if "x**2" in user_input or "x^2" in user_input:
            return solve_quadratic_equation(user_input)
        else:
            return solve_linear_equation(user_input)

    if "tính đạo hàm" in user_input:
        return calculate_derivative(user_input)

    if "tính tích phân" in user_input:
        return calculate_integral(user_input)

    if "diện tích hình tròn" in user_input:
        return calculate_circle_area(user_input)

    return "Mình chưa hiểu câu hỏi, bạn có thể hỏi rõ hơn không?"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']
    response = get_response(user_input)
    return response

if __name__ == '__main__':
    app.run(debug=True)
import ast
import sys
import os
from openai import OpenAI
from radon.complexity import cc_visit
from radon.visitors import ComplexityVisitor
from tenacity import retry, wait_random_exponential, stop_after_attempt

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_code(code):
    # Parse the code into an AST
    tree = ast.parse(code)

    # Analyze the complexity using radon
    complexity = cc_visit(code)

    # Extract relevant information from the complexity results
    complexity_info = []
    for item in complexity:
        complexity_info.append({
            'name': item.name,
            'lineno': item.lineno,
            'col_offset': item.col_offset,
            'end_lineno': item.endline,  # Corrected attribute name
            'end_col_offset': item.end_col_offset if hasattr(item, 'end_col_offset') else None,  # Ensure attribute exists
            'complexity': item.complexity,
            'classname': getattr(item, 'classname', None)  # Use getattr to safely access classname
        })

    return {
        'complexity': complexity_info,
        'functions': [func.name for func in complexity]
    }

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_code_review_comments(code):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a code review assistant."},
            {"role": "user", "content": f"Review the following Python code and provide comments:\n\n{code}"}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def format_analysis_result(result):
    formatted_result = "Analysis Result:\n"
    for item in result['complexity']:
        formatted_result += (
            f"Function/Class: {item['name']}\n"
            f"  Line Number: {item['lineno']}\n"
            f"  Column Offset: {item['col_offset']}\n"
            f"  End Line Number: {item['end_lineno']}\n"
            f"  End Column Offset: {item['end_col_offset']}\n"
            f"  Complexity: {item['complexity']}\n"
            f"  Class Name: {item['classname']}\n\n"
        )
    formatted_result += "Functions:\n"
    for func in result['functions']:
        formatted_result += f"  - {func}\n"
    return formatted_result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_python_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
        code = file.read()

    analysis_result = analyze_code(code)
    review_comments = generate_code_review_comments(code)

    formatted_analysis_result = format_analysis_result(analysis_result)

    print(formatted_analysis_result)
    print("\nCode Review Comments:\n", review_comments)

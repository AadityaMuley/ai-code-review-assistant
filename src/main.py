import ast
import sys
from radon.complexity import cc_visit
from radon.visitors import ComplexityVisitor

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
            'classname': item.classname
        })
    
    return {
        'complexity': complexity_info,
        'functions': [func.name for func in complexity]
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_python_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
        code = file.read()

    analysis_result = analyze_code(code)
    print(analysis_result)

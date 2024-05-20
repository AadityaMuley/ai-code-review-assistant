import unittest
from textwrap import dedent
from src.main import analyze_code


class TestCodeAnalysis(unittest.TestCase):

    def test_analyze_code(self):
        code = dedent("""
        def addition():
            a = 1
            b = 2
            return a + b

        def factorial(n):
            if n == 0:
                return 1
            else:
                return n * factorial(n-1)
        """)
        expected_result = {
            'complexity': [
                {
                    'name': 'addition', 'lineno': 2, 'col_offset': 0, 'end_lineno': 5, 'end_col_offset': None,
                    'complexity': 1, 'classname': None
                },
                {
                    'name': 'factorial', 'lineno': 7, 'col_offset': 0, 'end_lineno': 11, 'end_col_offset': None,
                    'complexity': 2, 'classname': None
                }
            ],
            'functions': ['addition', 'factorial']
        }
        result = analyze_code(code)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()

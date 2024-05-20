import unittest
from textwrap import dedent
from unittest.mock import patch, MagicMock
from src.main import analyze_code, generate_code_review_comments


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

    @patch('src.main.get_openai_client')
    def test_generate_code_review_comments(self, mock_get_openai_client):
        mock_client = MagicMock()
        mock_get_openai_client.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices[0].message.content.strip.return_value = (
            "Review: The code looks good."
        )

        code = dedent("""
        def addition():
            a = 1
            b = 2
            return a + b
        """)
        result = generate_code_review_comments(code)
        self.assertEqual(result, "Review: The code looks good.")


if __name__ == "__main__":
    unittest.main()

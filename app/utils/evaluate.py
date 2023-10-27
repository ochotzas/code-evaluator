import difflib
import sys
from io import StringIO


def execute_code(code, expected_output):
    exec_result = {}
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        exec(code, globals(), exec_result)
        actual_output = sys.stdout.getvalue()

        sys.stdout = old_stdout

        if actual_output == expected_output:
            return True, 'Output matches the expected output', None, None
        else:
            diff = difflib.ndiff(actual_output.splitlines(keepends=True), expected_output.splitlines(keepends=True))
            diff_str = ''.join([x for x in diff if x != '\n'])
            return False, 'Output does not match the expected output', diff_str, actual_output

    except Exception as e:
        return False, str(e), None, None

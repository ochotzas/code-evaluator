import difflib
import sys
from io import StringIO

from flask import request, jsonify, render_template

from app import app


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/evaluate', methods=['POST'])
def evaluate_code():
    data = request.get_json()
    code = data.get('code')
    expected_output = data.get('expected_output')

    try:
        exec_result = {}  # Define exec_result as a dictionary
        # Redirect stdout to capture the output
        old_stdout = sys.stdout
        sys.stdout = StringIO()  # Create a StringIO object to capture the output

        exec(code, globals(), exec_result)
        actual_output = sys.stdout.getvalue()  # Get the captured output

        sys.stdout = old_stdout  # Restore the original stdout

        # Check if the actual output matches the expected output
        if actual_output == expected_output:
            return jsonify({'success': True, 'message': 'Output matches the expected output.'})
        else:
            # Create a visual diff between actual and expected output and show if any there are whitespace differences
            diff = difflib.ndiff(actual_output.splitlines(keepends=True), expected_output.splitlines(keepends=True))
            diff_str = '\n'.join([x for x in diff if x != '\n'])

            return jsonify({'success': False, 'message': 'Output does not match the expected output.',
                            'diff': diff_str, 'expected_output': expected_output, 'actual_output': actual_output})
    except Exception as e:
        return jsonify(
            {'success': False, 'message': 'Error occurred while executing the code.', 'error_message': str(e)})

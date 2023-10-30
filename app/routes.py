from flask import request, jsonify, render_template

from app import app
from .common.enums.routes import Routes
from .utils import database
from .utils.evaluate import execute_code


@app.route(Routes.INDEX.value, methods=['GET'])
def index():
    assigment_key = request.args.get('assignment')

    assigment = database.get_assignment(assigment_key)

    return render_template('index.html', expected_output=assigment.expected_code,
                           assigment_description=assigment.description, assigment_timestamp=assigment.timestamp,
                           assigment_key=assigment_key)


@app.route(Routes.EVALUATE.value, methods=['POST'])
def evaluate_code():
    data = request.get_json()
    code = data.get('code')
    expected_output = data.get('expected_output')

    success, message, diff, actual_output = execute_code(code, expected_output)

    if success:
        return jsonify({'success': True, 'message': message})
    else:
        return jsonify({'success': False, 'message': message,
                        'diff': diff, 'expected_output': expected_output, 'actual_output': actual_output})


@app.route(Routes.POST_ASSIGNMENT.value, methods=['POST', 'GET'])
def post_assigment():
    if request.method == 'GET':
        return render_template('assigment.html')

    data = request.get_json()

    expected_output = data.get('expected_output')
    description = data.get('description')

    key = database.create_assignment(expected_output, description)

    if key is not None:
        return jsonify({'success': True, 'message': 'Assignment created successfully.', 'key': key})
    else:
        return jsonify({'success': False, 'message': 'Error occurred while creating the assignment.'})


@app.route(Routes.GET_ALL_ASSIGNMENTS.value, methods=['GET'])
def get_all_assignments():
    return jsonify({'success': True, 'assignments': database.get_all_assignments()})

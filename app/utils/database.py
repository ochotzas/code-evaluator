from flask import json

from ..common.enums.assignment import AssignmentDetails
from ..models import assignment
from ..utils import authenticate as auth

# Create an instance of the authentication class
access = auth.Authentication()


def create_assignment(expected_code, description):
    """
    Create an assignment in the database
    :return: The key of the created assignment or None if it failed
    """
    db = access.firestore.client()
    assignments_ref = db.collection('assignments')

    new_assignment = assignment.Assignment(expected_code, description, access.firestore.SERVER_TIMESTAMP).to_dict()

    return assignments_ref.add(new_assignment)[1].id


def get_assignment(assignment_key):
    """
    Get an assignment from a database by key if it exists, otherwise return an empty assignment object
    :param assignment_key: String key of assignment
    :return: Object assignment or empty assignment object
    """
    if not assignment_key:
        return assignment.Assignment(None, None, None)

    db = access.firestore.client()
    assignment_ref = db.collection(AssignmentDetails.COLLECTION.value).document(assignment_key)
    assignment_data = assignment_ref.get().to_dict()

    if assignment_data:
        return assignment.Assignment(assignment_data.get(AssignmentDetails.EXPECTED_CODE.value),
                                     assignment_data.get(AssignmentDetails.DESCRIPTION.value),
                                     assignment_data.get(AssignmentDetails.TIMESTAMP.value))

    return assignment.Assignment(None, None, None)


def get_all_assignments():
    """
    Get all assignments from database
    :return: A JSON list of all assignments
    """
    db = access.firestore.client()
    assignments_ref = db.collection('assignments')
    assignments = assignments_ref.stream()

    assignments_list = []
    for a in assignments:
        assignment_obj = assignment.Assignment(
            a.get(AssignmentDetails.EXPECTED_CODE.value),
            a.get(AssignmentDetails.DESCRIPTION.value),
            a.get(AssignmentDetails.TIMESTAMP.value),
            a.id)

        assignments_list.append(assignment_obj.to_dict())

    return json.dumps(assignments_list)

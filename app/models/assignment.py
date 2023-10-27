import json
from ..common.enums.assignment import AssignmentDetails


class Assignment:
    """
    Represents an assignment model.
    """

    def __init__(self, expected_code: str, description: str, timestamp: int, key: str = None):
        self.expected_code = expected_code
        self.description = description
        self.timestamp = timestamp
        self.key = key

    def to_dict(self):
        """
        Converts the object to a dictionary.
        :return: The dictionary representation of the object.
        """
        return {
            AssignmentDetails.EXPECTED_CODE.value: self.expected_code,
            AssignmentDetails.DESCRIPTION.value: self.description,
            AssignmentDetails.TIMESTAMP.value: self.timestamp,
            **({AssignmentDetails.KEY.value: self.key} if self.key is not None else {})
        }

    def __repr__(self):
        """
        Converts the object dictionary model to a JSON string.
        :return: The JSON representation of the object.
        """
        return json.dumps(self.to_dict())

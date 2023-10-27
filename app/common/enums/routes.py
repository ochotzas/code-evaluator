from enum import Enum


class Routes(Enum):
    INDEX = '/'
    EVALUATE = '/evaluate'
    POST_ASSIGNMENT = '/post-assignment'
    GET_ALL_ASSIGNMENTS = '/get-all-assignments'

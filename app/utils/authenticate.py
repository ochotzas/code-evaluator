import json
import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore


class Authentication:
    """
    Authentication class for Firebase
    """

    def __init__(self):
        """
        Initialize Firebase app
        """
        load_dotenv()
        self._firebase_credentials = credentials.Certificate(json.loads(os.environ.get("GOOGLE_CREDENTIALS_JSON")))
        self._app = firebase_admin.initialize_app(self._firebase_credentials)

    @property
    def firestore(self):
        """
        Get firestore instance
        :return:
        """
        return firebase_admin.firestore

    @property
    def app(self):
        """
        Get firebase app
        :return: The firebase app
        """
        return self._app

#!/usr/bin/python3
"""
Module for User
"""

from app.models.base_model import BaseModel


class User(BaseModel):

    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Create the instance of user

        Args:
            first_name (string): first name of user
            last_name (string): last name of user
            email (string): email of user
            is_admin (bool, optional): if user is admin. Defaults to False.
        """
        super().__init__()  # Call parent to generate UUID & timestamps
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []  # list to store places user owns

        # Password for the moment is not implemented (following the HBNB tasks)
        # self.password = None

#!/usr/bin/python3
"""
BaseModel class that defines all common attributes/methods for other classes
"""

import uuid
from datetime import datetime


class BaseModel:
    def __init__(self):
        """
        Intialize a new instance with UUID & timestamps for creation and update
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Update the updated_at timestamp whenever the object is modified
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update the attributes of the object based on the provided dictionary
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

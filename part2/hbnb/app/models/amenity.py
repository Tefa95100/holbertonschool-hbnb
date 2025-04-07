#!/usr/bin/python3
"""
Module for amenity
"""

from app.models.base_model import BaseModel


class Amenity(BaseModel):

    def __init__(self, name):
        """
        Create instance of Amenity

        Args:
            name (string): Name of the amenity
        """
        super().__init__()  # Call parent to generate UUID & timestamps
        self.name = name

#!/usr/bin/python3
"""
Module for Review
"""

from app.models.base_model import BaseModel


class Review(BaseModel):

    def __init__(self, text, rating, place_id, user_id):
        """
        Create instance of review

        Args:
            text (string): Comments in the review
            rating (int): 0 to 5 star rating
            place (Place): the place to which this review refers
            user (User): tue user who writes the review
        """
        super().__init__()  # Call parent to generate UUID & timestamps
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

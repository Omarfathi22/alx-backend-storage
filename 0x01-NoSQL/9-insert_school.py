#!/usr/bin/env python3
'''Module for MongoDB operations related to task 9.
'''


def insert_school(mongo_collection, **kwargs):
    '''Inserts a new document into the specified MongoDB collection.

    Args:
        mongo_collection: The MongoDB collection where the document will be inserted.
        **kwargs: The fields and values for the new document.

    Returns:
        The unique identifier (_id) of the inserted document.
    '''
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id

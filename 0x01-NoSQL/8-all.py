#!/usr/bin/env python3
'''Module for MongoDB operations related to task 8.
'''


def list_all(mongo_collection):
    '''Lists all documents in a given MongoDB collection.

    Args:
        mongo_collection: The MongoDB collection from which to list documents.

    Returns:
        A list of all documents in the collection.
    '''
    return [doc for doc in mongo_collection.find()]

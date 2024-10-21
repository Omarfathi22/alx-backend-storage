#!/usr/bin/env python3
'''Module for updating topics in a MongoDB collection.
'''

def update_topics(mongo_collection, name, topics):
    '''Update the 'topics' field of all documents in the collection that match the given name.

    Parameters:
    mongo_collection (Collection): The MongoDB collection to update.
    name (str): The name used to find the documents to update.
    topics (list): The new list of topics to set in the matching documents.
    '''
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )

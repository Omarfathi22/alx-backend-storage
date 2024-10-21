#!/usr/bin/env python3
'''Module for MongoDB operations related to task 11.
'''


def schools_by_topic(mongo_collection, topic):
    '''Retrieves a list of schools that have a specific topic.

    Args:
        mongo_collection: The MongoDB collection containing school documents.
        topic (str): The topic to filter schools by.

    Returns:
        A list of documents representing schools that include the specified topic.
    '''
    topic_filter = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [doc for doc in mongo_collection.find(topic_filter)]

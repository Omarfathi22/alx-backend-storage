#!/usr/bin/env python3
'''Module for retrieving and sorting students by average score from a MongoDB collection.
'''


def top_students(mongo_collection):
    '''Retrieves all students from a collection, sorted by their average score.

    Args:
        mongo_collection: The MongoDB collection containing student documents.

    Returns:
        A cursor containing student documents sorted by average score in descending order.
    '''
    students = mongo_collection.aggregate(
        [
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'averageScore': {
                        '$avg': {
                            '$avg': '$topics.score',  # Calculate the average score of each student
                        },
                    },
                    'topics': 1,
                },
            },
            {
                '$sort': {'averageScore': -1},  # Sort by average score in descending order
            },
        ]
    )
    return students

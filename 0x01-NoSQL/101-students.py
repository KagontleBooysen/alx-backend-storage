#!/usr/bin/env python3
''' module for task 12 '''


def top_students(mongo_collection):
    ''' function that lists top students in a collection '''
    return mongo_collection.aggregate([
        {
            "$project":
                {
                    "name": "$name",
                    "averageScore": {"$avg": "$topics.score"}
                }
        },
        {"$sort": {"averageScore": -1}}
    ])

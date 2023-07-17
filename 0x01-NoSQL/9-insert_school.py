#!/usr/bin/env python3
''' module for task 9 '''


def insert_school(mongo_collection, **kwargs):
    ''' function that inserts a new document in a collection '''
    return mongo_collection.insert_one(kwargs).inserted_id

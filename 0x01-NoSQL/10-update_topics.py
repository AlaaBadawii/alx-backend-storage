#!/usr/bin/env python3
"""
changes all topics
"""

def update_topics(mongo_collection, name, topics):
    """
    changes all topics of a school document based on the name
    """
    mongo_collection.update(
        {'name': name}, 
        {'$set': {topics: topics}}
    )

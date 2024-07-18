#!/usr/bin/env python3
"""
"""

from pymongo import MongoClient

def print_nginx_request_logs(nginux_collection):
    """"""
    print('{} logs'.format(nginux_collection.count_documents({})))
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req_count = len(list(nginux_collection.find({'method': method})))
        print(f'\tmethod {method}: {req_count}')
    status_checks_count = len(list(
        nginux_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(status_checks_count))


def run():
    '''Provides some stats about Nginx logs stored in MongoDB.
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(client.logs.nginx)


if __name__ == '__main__':
    run()

    
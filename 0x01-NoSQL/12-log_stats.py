#!/usr/bin/env python3
''' module for task 12 '''
from pymongo import MongoClient


def main():
    ''' script that provides some stats about Nginx logs '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    lst = client.logs.nginx

    print("{} logs\nMethods:".format(lst.estimated_document_count()))

    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        print("\tmethod {}: {}".format(method,
              lst.count_documents({'method': method})))

    print("{} status check".format(lst.count_documents(
        {'method': 'GET', 'path': "/status"})))


if __name__ == "__main__":
    main()

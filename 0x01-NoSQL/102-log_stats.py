#!/usr/bin/env python3
'''Module for printing statistics about Nginx request logs from a MongoDB collection.
'''
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    '''Prints statistics about Nginx request logs.

    Args:
        nginx_collection: The MongoDB collection containing Nginx log documents.
    '''
    total_logs = nginx_collection.count_documents({})
    print('{} logs'.format(total_logs))  
    print('Methods:')
    
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req_count = len(list(nginx_collection.find({'method': method})))  
        print('\tmethod {}: {}'.format(method, req_count))
    

    status_checks_count = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(status_checks_count))


def print_top_ips(server_collection):
    '''Prints statistics about the top 10 HTTP IPs based on request counts.

    Args:
        server_collection: The MongoDB collection containing server request logs.
    '''
    print('IPs:')
    request_logs = server_collection.aggregate(
        [
            {
                '$group': {
                    '_id': "$ip", 
                    'totalRequests': {'$sum': 1}  
                }
            },
            {
                '$sort': {'totalRequests': -1}  
            },
            {
                '$limit': 10  
            },
        ]
    )
    
    for request_log in request_logs:
        ip = request_log['_id']
        ip_requests_count = request_log['totalRequests']
        print('\t{}: {}'.format(ip, ip_requests_count))  


def run():
    '''Runs the functions to print stats about Nginx logs stored in MongoDB.
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(client.logs.nginx)  
    print_top_ips(client.logs.nginx)  


if __name__ == '__main__':
    run()  

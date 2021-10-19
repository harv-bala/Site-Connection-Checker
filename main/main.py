import time as t
import argparse
import json
from pathlib import Path
from db.db_helper import DBHelper
from status.status_checker import StatusChecker

def validate_url(url):
    statChecker = StatusChecker(url)
    statChecker.check_status()

def add_to_database(url):
    validate_url(url)
    webDB = DBHelper()
    webDB.create_record(url)

def remove_from_database(url):
    webDB = DBHelper()
    webDB.delete_record(url)

def get_interval():
    filepath = str(Path('settings.json'))
    with open(filepath, 'r') as f:
        data = json.load(f)
    interval = data['settings'][0]['interval']
    return int(interval)

def set_interval(interval):
    filepath = str(Path('settings.json'))
    with open(filepath, 'r') as f:
        data = json.load(f)

    data['settings'][0]['interval'] = str(interval)

    with open(filepath, 'w') as f:
        json.dump(data, f)

def print_results():
    webDB = DBHelper()
    results = webDB.read_all_records()
    for result in results:
        if result[2] == 1:
            print(f'{result[1]:<34} [OK]')
        elif result[2] == 0:
            print(f'{result[1]:<34} [ERROR]')

def print_sites():
    webDB = DBHelper()
    results = webDB.read_all_records()
    print('Current stored sites: \n')
    for result in results:
        print(result[1])

def print_sites_verbose():
    webDB = DBHelper()
    results = webDB.read_all_records()
    print(f'Here are the sites you currently have stored. There are {len(results)} sites: \n')
    for i in range(len(results)):
        print(f'Site {i + 1}: {results[i][1]}')

def main():
    webDB = DBHelper()
    interval = get_interval()
    print_results()

    try:
        while True:
            t.sleep(interval)
            records = webDB.read_all_records()
            for record in records:
                statChecker = StatusChecker(record[1])
                statChecker.check_status()
                currentStatus = statChecker.get_status()
                if currentStatus != record[2]:
                    webDB.update_record(record[1], currentStatus)
                    print('STATUS UPDATED FOR ONE OR MORE WEBSITES')
            print_results()
    except KeyboardInterrupt:
        print('PROGRAM STOPPED')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Site Connection Checker')
    subparser = parser.add_subparsers(dest='command')
    database = subparser.add_parser('database', help='Perform database operations')
    interval = subparser.add_parser('interval', help='Change the check time interval')
    listSites = subparser.add_parser('list', help='List all websites stored in the database')
    start = subparser.add_parser('start', help='Start the program')

    db_group = database.add_mutually_exclusive_group()
    db_group.add_argument('-a', '--add', metavar='', help='Add to DB')
    db_group.add_argument('-r', '--remove', metavar='', help='Remove from DB')

    list_group = listSites.add_mutually_exclusive_group()
    list_group.add_argument('-v', '--verbose', help='Output a more verbose list of websites', action='store_true')

    interval.add_argument('-c', '--change', metavar='', type=int, help='Change the check time interval', required=True)

    args = parser.parse_args()

    if args.command == 'start':
        main()
    elif args.command == 'database':
        if args.add:
            add_to_database(args.add)
        elif args.remove:
            remove_from_database(args.remove)
    elif args.command == 'interval':
        set_interval(args.change)
        print('Changed interval time to', args.change, 'seconds')
    elif args.command == 'list':
        if args.verbose:
            print_sites_verbose()
        else:
            print_sites()
    else:
        print('Enter a valid command. Use -h or --help for help.')
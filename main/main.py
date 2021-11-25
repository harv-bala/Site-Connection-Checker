import time as t
import argparse
import json
from pathlib import Path
from db.db_helper import DBHelper
from status.status_checker import StatusChecker


def validate_url(url: str):
    '''check url is in the correct format'''
    stat_checker = StatusChecker(url)
    stat_checker.check_status()


def add_to_database(url: str):
    '''add a website to the database'''
    validate_url(url)
    web_db = DBHelper()
    web_db.create_record(url)


def remove_from_database(url: str):
    '''remove a website from the database'''
    web_db = DBHelper()
    web_db.delete_record(url)


def get_interval() -> int:
    '''return the time interval stored in the settings file'''
    filepath = str(Path('settings.json'))
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    time_interval = data['settings'][0]['interval']
    return int(time_interval)


def set_interval(time_interval: int):
    '''set (overwrite) the time interval stored in the settings file'''
    filepath = str(Path('settings.json'))
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    data['settings'][0]['interval'] = str(time_interval)

    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file)


def print_results():
    '''print formatted website statuses'''
    web_db = DBHelper()
    results = web_db.read_all_records()
    if results:
        for result in results:
            if result[2] == 1:
                print(f'{result[1]:<34} [OK]')
            elif result[2] == 0:
                print(f'{result[1]:<34} [ERROR]')


def print_sites():
    '''print list of all stored websites'''
    web_db = DBHelper()
    results = web_db.read_all_records()
    print('Current stored sites: \n')
    if results:
        for result in results:
            print(result[1])


def print_sites_verbose():
    '''print a formatted, verbose list of stored websites'''
    web_db = DBHelper()
    results = web_db.read_all_records()
    if results:
        print(
            'Here are the sites you currently have stored. '
            f'There are {len(results)} sites: \n')
        for i, j in enumerate(results):
            print(f'Site {i + 1}: {j[1]}')
    else:
        pass


def main():
    '''continuously check status of stored websites unless interrupted'''
    web_db = DBHelper()
    time_interval = get_interval()
    print('PROGRAM STARTED')

    try:
        while True:
            t.sleep(time_interval)
            records = web_db.read_all_records()
            if records:
                for record in records:
                    stat_checker = StatusChecker(record[1])
                    stat_checker.check_status()
                    current_status = stat_checker.get_status()
                    if current_status != record[2]:
                        web_db.update_record(record[1], current_status)
                        print('STATUS UPDATED FOR ONE OR MORE WEBSITES')
                print_results()
    except KeyboardInterrupt:
        print('PROGRAM STOPPED')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Site Connection Checker')
    subparser = parser.add_subparsers(dest='command')
    database = subparser.add_parser(
                                    'database',
                                    help='Perform database operations')
    interval = subparser.add_parser(
                                    'interval',
                                    help='Change the check time interval')
    listSites = subparser.add_parser(
                                    'list',
                                    help='List all websites in the database')
    start = subparser.add_parser('start', help='Start the program')

    db_group = database.add_mutually_exclusive_group()
    db_group.add_argument('-a', '--add', metavar='', help='Add to DB')
    db_group.add_argument('-r', '--remove', metavar='', help='Remove from DB')

    list_group = listSites.add_mutually_exclusive_group()
    list_group.add_argument(
                            '-v',
                            '--verbose',
                            help='Output a more verbose list of websites',
                            action='store_true')

    interval.add_argument(
                        '-c',
                        '--change',
                        metavar='',
                        type=int,
                        help='Change the check time interval',
                        required=True)

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

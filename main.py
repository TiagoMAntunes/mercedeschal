import json
import urllib.request
import re
import sys
import time
from bs4 import BeautifulSoup

FLAGPATTERN = re.compile('--[a-zA-Z]+=[\w,]+')

class Service:
    def __init__(self, name, url, tag, match, online):
        self.name = name
        self.url = url
        self.tag = tag
        self.match = match
        self.online = online
        self.records = []

    def isOnline(self):
        """Makes a request to the service url and tries to match, analyzing the html and deciding if the service is online"""
        # connect to server and fetch html
        with urllib.request.urlopen(self.url) as url:
            # find the correct html tag
            soup = BeautifulSoup(url.read(), features='html.parser')
            # validate if content is online with no problems
            status = self.online in str(soup.find(self.tag, self.match))
            self.records.append(
                {"time": time.time(), "status": "up" if status else "down"})
            return status

    def __repr__(self):
        return ",".join([self.name, self.url, self.tag, str(self.match), self.online])


def getFlags(args, validFlags):
    """ Receives a list of strings and the flags to analyze.\nReturns a dictionary with the information organized """
    flagList = list(filter(lambda x: re.match(FLAGPATTERN, x), args))
    flags = {el: [] for el in validFlags}
    for flag in flagList:
        # checks if valid flag is the one used
        for f in validFlags:
            if f in flag:
                # only selects the important part of the flag
                flags[f].extend(flag[flag.find('=')+1:].split(','))
                break
    return flags


def poll(services, args):
    """ Evaluates if services the specified services are online """
    # finds flags and gets their information
    flags = getFlags(args, ['only', 'exclude'])

    # possible functions to be taken
    def fn1(x): return True
    def fn2(x): return x in flags["only"]
    def fn3(x): return x not in flags['exclude']

    fn = fn1
    if len(flags["only"]) > 0:
        fn = fn2
    elif len(flags['exclude']) > 0:
        fn = fn3

    for service in services:
        if (fn(service.name.lower())):
            print('[' + service.name + '] ' + time.asctime(time.localtime(time.time())
                                                           ) + " - " + "up" if service.isOnline() else "down")


def fetch(services, args):
    """ Calls poll function within a time interval """
    flags = getFlags(args, ['refresh'])
    if len(flags['refresh']) > 0:
        try:
            sleeptime = int(flags['refresh'][0])
        except ValueError:
            print("Refresh flag must be integer")
            raise KeyError
    else:
        sleeptime = 5

    while True:
        poll(services, args)
        time.sleep(sleeptime)


def history(services, args):
    """ Gets data from storage and displays it to the user """
    flags = getFlags(args, ['only'])

    def f1(x): return True
    def f2(x): return x in flags['only']
    fn = f1
    if len(flags['only']) > 0:
        fn = f2
    for service in services:
        if fn(service.name.lower()):
            for data in service.records:
                print('[' + service.name + "] - " + "Time: " +
                      time.asctime(time.localtime(data["time"])) + ", status: " + data["status"])


def backup(services, args):
    """ Saves data to storage with a specified format """
    flags = getFlags(args, ['format'])

    if len(args) - len(flags['format']) < 1:
        print('You need to specify the path where to save to')
        return

    def f1(x, filepath): json.dump({'records': x}, filepath)  # json

    def f2(x, filepath):
        for data in x:
            filepath.write(data['name']+'\n')
            filepath.write(",".join(str(x) for x in data['data']) + '\n')

    def f3(x, filepath):
        for data in x:
            filepath.write(data['name'] + ':' + ",".join(str(y)
                                                         for y in data['data']) + '\n')

    fn = f1
    if len(flags['format']) > 0:
        if 'txt' in flags['format']:
            fn = f3
        elif 'csv' in flags['format']:
            fn = f2

    # find path to write to
    for key in args:
        if not re.match(FLAGPATTERN, key):
            path = key
            break

    try:
        # writes to file data
        with open(path, 'w+') as f:
            data = []
            # gets each service and its records
            for service in services:
                data.append({"name": service.name, "data": service.records})

            fn(data, f)
    except IOError:
        print('Path is invalid')


def restore(services, args):
    """ Reads from storage (only in JSON) """
    flags = getFlags(args, ['merge'])
    if len(args) - len(flags['merge']) < 1:
        print('You need to specify the path where to save to')
        return
    if len(flags['merge']) > 0 and 'true' in flags['merge']:
        merge = True
    else:
        merge = False

    # find path to write to
    for key in args:
        if not re.match(FLAGPATTERN, key):
            path = key
            break

    try:
        with open(path) as f:
            data = json.load(f)['records']
            for el in data:
                for s in services:
                    if s.name == el['name'] and all(map(lambda x: x['time'] != el['data'][0]['time'], s.records)):
                        s.records = el['data'] if not merge else s.records + el['data']
                        break
    except IOError:
        print('Path is invalid')
    except ValueError:
        print('Invalid file')


def displayServices(services, args):
    """ Gets the information from all services """
    for service in services:
        print(service)


def help(*_):
    options = [
        ("poll", "Retrieves the status from all configured services"),
        ("fetch", "Retrieves the status from all configured services"),
        ("services", "Lists all known services"),
        ("backup", "Backups the current internal state to a file"),
        ('restore', "Imports the internal state from another run or app"),
        ('history', "Outputs all the data from the local storage"),
        ('help', "This screen")
    ]
    print('Commands:')
    for option in options:
        print('    ' + option[0] + ' - ' + option[1])


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Usage: python3 main.py <configuration file>")
        sys.exit(0)

    # get services from config file
    with open(sys.argv[1]) as config:
        data = json.load(config)

    services = []

    # create virtual services
    for serviceData in data['services']:
        services.append(Service(**serviceData))

    # switch case alternative
    options = {
        "poll": poll,
        "fetch": fetch,
        "history": history,
        "backup": backup,
        'restore': restore,
        'services': displayServices,
        'help': help
    }

    while True:
        print('> ', end='')
        line = input().lower().split()
        if len(line) == 0 or line[0] in ['exit']:
            break
        try:
            options[line[0]](services, line[1:])
        except KeyError as e:
            print(sys.exc_info())
            print('Invalid command')

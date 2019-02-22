import json
import urllib.request
import re
import sys
import time
from bs4 import BeautifulSoup


class Service:
    def __init__(self, name, url, tag, match, online):
        self.name = name
        self.url = url
        self.tag = tag
        self.match = match
        self.online = online
        self.records = []

    def isOnline(self):
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


def poll(services, args):
    for service in services:
        print('[' + service.name + '] ' + time.asctime(time.localtime(time.time())
                                                       ) + " - " + "up" if service.isOnline() else "down")


def fetch(services, args):
    while True:
        poll(services, args)
        time.sleep(5)


def history(services, args):
    for service in services:
        for data in service.records:
            print('[' + service.name + "] - " + "Time: " +
                  time.asctime(time.localtime(data["time"])) + ", status: " + data["status"])


def backup(services, args):
    if len(args) < 1:
        print('You need to specify the path where to save to')
        return
    try:
        # writes to file data
        with open(args[0], 'w+') as f:
            data = []
            # gets each service and its records
            for service in services:
                data.append({"name": service.name, "data": service.records})
            # dump data as json format
            json.dump({"records": data}, f)
    except IOError:
        print('Path is invalid')


def restore(services, args):
    if len(args) < 1:
        print('You need to specify the path where to save to')
        return
    try:
        with open(args[0]) as f:
            data = json.load(f)['records']
            for el in data:
                for s in services:
                    if s.name == el['name']:
                        s.records = el['data']
                        break
    except IOError:
        print('Path is invalid')
    except ValueError:
        print('Invalid file')

def displayServices(services, args):
    for service in services:
        print(service)

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
        'services':displayServices
    }

    while True:
        line = input().split()
        if len(line) == 0 or line[0] in ['exit', '']:
            break
        try:
            options[line[0]](services, line[1:])
        except KeyError:
            print('Invalid command')

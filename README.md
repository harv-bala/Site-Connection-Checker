# Site Connection Checker

Site Connection Checker (SCC) is a command line tool which allows you to continuously check the status of any website(s).

### Why Might I Use Site Connection Checker?

It is not uncommon to visit a website only to find that, for whatever reason, it is out of action. At this point, you can either waste time constantly refreshing the page in the hopes that it will go back online, or you can leave the site for some arbitrary and likely excessive amount of time and hope that when you try again, the site is working.

Neither of these options are particularly ideal, which is why SCC exists. By automatically checking the status of any website(s) you request, at timed intervals you set, SCC can alert you as soon as a website is back online and connection is established.

### Prerequisites

SCC requires the requests library for Python. You can install it with Python's package manager, pip.

#### Unix / macOS
```shell
python -m pip install requests
```
#### Windows
```shell
py -m pip install requests
```

### Usage
There are multiple commands and options to setup and run the Site Connection Checker.

#### Start the program
```shell
python main.py start
```

#### Add a website to check
```shell
python main.py database -a [URL]
```

#### Remove a website
```shell
python main.py database -r [URL]
```

#### Change the time interval between checks
```shell
python main.py interval -c [value]
```

#### Help
You can always run the help command to get information about how to use the program and its commands.

For general help:
```shell
python main.py -h
```
For command-specific help:
```shell
python main.py [command] -h
```

### Features

- Automatically run status checks on any website(s)
- Customisable status check time intervals
- Create your own list of websites to be checked
- Get alerts when websites on your list go back online

# License

This project is licensed under the MIT license.
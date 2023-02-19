![Logo](https://i.imgur.com/qXfSr0u.png)

Jasmin is a utility that displays a list of Linux commands available on a given machine. 

Connecting via SSH, Jasmin tests potentially useful commands to exit a restricted shell and perform actions that were normally restricted.

## Demonstration

[![asciicast](https://asciinema.org/a/0K7bmescf283rWU2pxr5KMWy4.svg)](https://asciinema.org/a/0K7bmescf283rWU2pxr5KMWy4)

## Requirements

```
python -m pip install paramiko rich
```

## Installing

```
python -m pip install jasmin-fuzzer
```

## Help page

```
$ jasmin --help
usage: jasmin [-h] --user username --host hostname [--privatekey] [-p PORT] [-v]

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  --user username       username
  --host hostname       ip address or domain name

optional arguments:
  --privatekey          connection established with your private key
  -p PORT, --port PORT  ssh to use port (default=22)
  -v, --verb            give each command tested (default=False)
```
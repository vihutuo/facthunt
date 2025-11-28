import datetime
import sys

# ANSI color codes
COL = {
    "RESET": "\033[0m",
    "GRAY": "\033[90m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "CYAN": "\033[36m",
}

def _ts():
    return datetime.datetime.now().strftime("%H:%M:%S")

def _log(color, label, msg):
    text = f"{COL['GRAY']}[{_ts()}]{COL['RESET']} {color}{label}{COL['RESET']} {msg}"
    print(text, flush=True, file=sys.stdout)   # flush for Fly.io

# PUBLIC API -------------------------------------------------------

def info(msg):
    _log(COL["CYAN"],  "[INFO]", msg)

def ok(msg):
    _log(COL["GREEN"], "[ OK ]", msg)

def warn(msg):
    _log(COL["YELLOW"], "[WARN]", msg)

def error(msg):
    _log(COL["RED"],   "[ERR ]", msg)
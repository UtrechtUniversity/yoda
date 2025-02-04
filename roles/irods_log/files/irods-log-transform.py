#!/usr/bin/python3
#
# This script is used by rsyslogd to transform iRODS
# JSON log messages into a more human-readable format.

import datetime
import json
import os
import sys

LOG_DIR = "/var/lib/irods-log"


def get_log_file() -> str:
    filename = datetime.datetime.now().strftime("rodsLog-%Y-%m-%d")
    return os.path.join(LOG_DIR, filename)


def write_message(message: str) -> None:
    with open(get_log_file(), "a") as logfile:
        logfile.write(message)
        logfile.flush()


def process_log() -> None:
    for line in sys.stdin:
        output_message = get_output_message(line)
        write_message(output_message)


def get_output_message(line: str) -> str:
    start_json_message = line.index("{") if "{" in line else 0
    try:
        json_data = json.loads(line[start_json_message:])
    except json.decoder.JSONDecodeError:
        # If it's not JSON, it's probably an error message such as a Python exception
        # Just write it as-is, for readability.
        return line

    datestamp = json_data.get("server_timestamp", "n.d.")
    pid = json_data.get("server_pid", "N/A")
    category = json_data.get("log_category", "N/A")
    client_user = json_data.get("request_client_user", "N/A")
    proxy_user = json_data.get("request_proxy_user", "N/A")
    zone = json_data.get("server_zone", "N/A")

    if client_user == "N/A":
        user_string = "no_user"
    else:
        user_string = f"{client_user}#{zone}" if proxy_user == client_user else f"{client_user}:{proxy_user}#{zone}"

    level = json_data.get("log_level", "N/A")
    message = json_data.get("log_message", "No message")

    if category == "rule_engine" and level == "info" and message.startswith("writeString:"):
        # Abbreviate writeString messages for better readability
        message = message.replace("writeString:", "", 1)

    return f"{datestamp} pid:{pid} {category}:{level} {{{user_string}}} {message}\n"


if __name__ == "__main__":
    process_log()

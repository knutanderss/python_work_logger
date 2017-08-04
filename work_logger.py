#!/usr/bin/python

import sys
import os.path
import time

LOGGER_FILE_COLUMNS = ['Date', 'Time', 'Session length', 'Total length']

def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

def column_string():
    return ''.join(intersperse(LOGGER_FILE_COLUMNS, ';'))

def file_exist(file_name):
    return os.path.isfile(file_name)

def create_log_file(file_name):
    log_file = open(file_name, 'w')
    log_file.write(column_string() + '\n')
    time_now = time.strftime("%H:%M:%S")
    date_now = time.strftime("%d/%m/%Y")
    log_file.write('{};{};0;0 \n'.format(date_now, time_now))

# returns numbers of seconds since start of project
def get_total_seconds(file_name):
    if not file_exist(file_name):
        create_log_file(file_name)
        return 0.0
    else:
        with open(file_name) as log_file:
            last_record = log_file.readlines()[-1]
            fields = last_record.split(';')
            return float(fields[3])

def save_new_record(file_name, session_time, total_time):
    log_file = open(file_name, 'a')
    time_now = time.strftime("%H:%M:%S")
    date_now = time.strftime("%d/%m/%Y")
    log_file.write('{};{};{};{} \n'.format(date_now, time_now, session_time, total_time))

def main():
    logger_file_name = sys.argv[1]
    total_seconds = get_total_seconds(logger_file_name)
    time_start = time.time()

    while(True):
        user_input = raw_input()
        if (user_input == "done"):

            session_seconds = time.time() - time_start
            new_total_seconds = total_seconds + session_seconds

            session_time = time.strftime("%H:%M:%S", time.gmtime(session_seconds))
            new_total_time = time.strftime("%H:%M:%S", time.gmtime(new_total_seconds))

            save_new_record(logger_file_name, session_seconds, new_total_seconds)
            print("This session lasted {}. Total time is now {}".format(session_time, new_total_time))
            return
        else:
            print("Unkown command. Write 'done' when finished")

main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-2-6 上午11:06

import re
import os
import argparse

parten = re.compile(r'RESPONSE:\s+.*TIME:\s+\d+')
parten_for_split = re.compile(r'\s+')


def analyze(log):
    with open(log, 'r') as log_file:
        for line in log_file:
            search_result = parten.search(line)
            if search_result:
                result_list = parten_for_split.split(line)[0:2]
                result_list.append(search_result.group())
                yield ' '.join(result_list)


def write_analyze_reuslt(new_log, analyze_result):
    with open(new_log, 'w') as new_log_file:
        for item in analyze_result:
            new_log_file.write("%s\n" % item)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="the dicretory og log files")
    args = parser.parse_args()
    if args.directory and os.path.isdir(args.directory):
        result_directory = os.path.join(args.directory, 'result')
        if not os.path.isdir(result_directory):
            os.mkdir(result_directory)
        print "Analyzing...\nRustlt will store in %s" % result_directory
        for log in os.listdir(args.directory):
            log_path = os.path.join(args.directory, log)
            if os.path.isfile(log_path):
                analyze_result_path = os.path.join(result_directory, log + '_result')
                print "Begin to analyze %s" % log_path
                write_analyze_reuslt(analyze_result_path, analyze(log_path))
        print "Completed"
    else:
        print("Pleace input correct directory!")

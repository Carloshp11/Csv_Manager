# -*- coding: utf-8 -*-

import os
# This code has been automatically taylored by the tool Csv manager_ for an specific file. Correct execution requires python interpreter 3.X


def get_files():
    if os.path.isfile('C:/Users/Carlos/Programming/Python/Csv_Manager/Csv_test.csv'):
        input_handler = open('C:/Users/Carlos/Programming/Python/Csv_Manager/Csv_test.csv', 'r', encoding="utf-8")
        output_handler = open(input_handler.name[:-4] + '_transformed.csv', 'w')
        manage_file(input_handler, output_handler)
    elif os.path.isdir('C:/Users/Carlos/Programming/Python/Csv_Manager/Csv_test.csv'):
        for csv in os.listdir('C:/Users/Carlos/Programming/Python/Csv_Manager/Csv_test.csv'):
            if csv[-4:] != '.csv' or csv[-16:] == '_transformed.csv':
                continue
            input_handler = open(csv, 'r', encoding="utf-8")
            output_handler = open(input_handler.name[:-4] + '_transformed.csv', 'w')
            manage_file(input_handler, output_handler)


def manage_file(input_handler, output_handler):
    number = 0
    delimiter = ','
    for line in input_handler:
        number += 1
        if number == 1:
            output_handler.write('NumeroFeo;NumeroGuapo' + '\n')
        if number <= 1:
            continue
        line = line.rstrip('\n').split(delimiter)
        processed_line = delete_columns(line)
        if processed_line is not None:
            output_handler.write(','.join(processed_line) + '\n')


def delete_columns(line):
    for delete_this_one in [1]:
        line.pop(delete_this_one)
    return filter_lines(line)


def filter_lines(line):
    if 5 <= int(line[1]) <= 100:
        return line


get_files()

import os

project_folder = os.getcwd()
newfile = open(os.path.join(project_folder, 'Filter output.csv'), 'w')
for csv in os.listdir(project_folder):
    if csv[-4:] != '.csv' or csv == 'Filter output.csv':
        continue
    handler = open(csv, 'r', encoding="utf-8")
    # noinspection PyRedeclaration
    number = 0
    for line in handler:
        number += 1
        if number <= 1:
            continue
        print(line.rstrip('\n'))
        delimiter = ','
        line = line.rstrip('\n').split(delimiter)
        if int(line[2]) >= 5:
            print('Writting', ','.join(line))
            newfile.write(','.join(line) + '\n')

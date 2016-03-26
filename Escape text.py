import os

project_folder = os.getcwd()
newfile = open(os.path.join(project_folder, 'Escaped text.txt'), 'w')
for csv in os.listdir(project_folder):
    if csv != 'Escape this text.txt':
        continue
    handler = open(csv, 'r', encoding="utf-8")
    # noinspection PyRedeclaration
    # for line in handler:
    # print(handler.read())
    document = handler.read()
    print(document, '\n', '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    document = document.replace('\'\\n\'', '\'\\\\n\'').replace('\'', '\\\'')
    print(document)
    newfile.write(document)
    # newfile.write(','.join(line) + '\n')

import os


def headers(args):
    print('Headers ', args)
    Compiled.manage_file_setter('Headers', P.new_delimiter.join(args))
    return None


# noinspection PyUnresolvedReferences,PyUnboundLocalVariable
def filter_lines(filter_to_apply):
    global __next_callback__
    Compiled.script_c[0]['filter_lines'] = 'def filter_lines(line):\n' + \
                                           '    if ' + filter_to_apply[0].lstrip('[').rstrip(']') + ':\n' + \
                                           '        return [callback]\n' + \
                                           '\n'
    Compiled.script_id_setter('filter_lines')
    print('Filter ', filter_to_apply[0])
    Compiled.callback_switcher[__next_callback__]('callback', 'filter_lines(line)')
    __next_callback__ = 'filter_lines'
    return None


def delete_columns(columns_to_delete):
    global __next_callback__
    for column in columns_to_delete:  # convert into integers
        if int(column) > P.min_number_of_columns - 1:
            error = 'You are trying to delete column [' + column + '], but at least one of the files has no more' + \
                    ' than ' + str(P.min_number_of_columns) + ' columns\n' + \
                    '              Remember: column index starts at 0'
            raise RuntimeError(error)

        columns_to_delete[columns_to_delete.index(column)] = int(columns_to_delete[columns_to_delete.index(column)])
    Compiled.script_c[0]['delete_columns'] = 'def delete_columns(line):\n' + \
                                             '    for delete_this_one in [list_to_delete]:\n' + \
                                             '        line.pop(delete_this_one)\n' + \
                                             '    return [callback]\n' \
                                             '\n'
    Compiled.delete_columns_setter('list_to_delete', str(sorted(columns_to_delete, key=int, reverse=True)))
    Compiled.script_id_setter('delete_columns')
    print('DeleteColumns ', columns_to_delete)
    Compiled.callback_switcher[__next_callback__]('callback', 'delete_columns(line)')
    __next_callback__ = 'delete_columns'
    return None


def transpose(args):
    # TODO Implementar Transpose
    print('Transpose ', args)
    return None


def new_delimiter(args):
    # Sintaxis := NewDelimiter [;]
    print('NewDelimiter ', args)
    P.new_delimiter = args[0].lstrip('[').rstrip(']')
    if P.new_delimiter == '':
        P.new_delimiter = ' '
    return None


class CompiledFile:
    def __init__(self):
        self.callback_switcher = {
            'manage_file': self.manage_file_setter,
            'headers': self.headers_setter,
            'filter_lines': self.filter_lines_setter,
            'transpose': self.transpose_setter,
            'delete_columns': self.delete_columns_setter
        }
        self.script_container_id = {
            0: 'get_files',
            1: 'manage_file'
        }
        self.script_container_text = {
            'get_files': '# -*- coding: utf-8 -*-\n' + \
                         '\n' \
                         'import os' \
                         '\n' \
                         '# This code has been automatically taylored by the tool Csv manager_' \
                         ' for an specific file. Correct execution requires python interpreter 3.X\n' \
                         '\n' \
                         '\n' \
                         'def get_files():\n' \
                         '    if os.path.isfile(\'INPUT_FILE_PATH_GOES_HERE\'):\n' \
                         '        input_handler = open(\'INPUT_FILE_PATH_GOES_HERE\', \'r\', encoding=\"utf-8\")\n' \
                         '        output_handler = open(input_handler.name[:-4] + \'_transformed.csv\', \'w\')\n' \
                         '        manage_file(input_handler, output_handler)\n' \
                         '    elif os.path.isdir(\'INPUT_FILE_PATH_GOES_HERE\'):\n' \
                         '        for csv in os.listdir(\'INPUT_FILE_PATH_GOES_HERE\'):\n' \
                         '            if csv[-4:] != \'.csv\' or csv[-16:] == \'_transformed.csv\':\n' \
                         '                continue\n' \
                         '            input_handler = open(csv, \'r\', encoding=\"utf-8\")\n' \
                         '            output_handler = open(input_handler.name[:-4] + \'_transformed.csv\', \'w\')\n' \
                         '            manage_file(input_handler, output_handler)\n' \
                         '\n',

            'manage_file': 'def manage_file(input_handler, output_handler):\n' + \
                           '    number = 0\n' \
                           '    delimiter = \'[delimiter]\'\n' \
                           '    for line in input_handler:\n' \
                           '        number += 1\n' \
                           '        if number == 1:\n' \
                           '            output_handler.write(line + \'\\n\')\n' \
                           '        if number <= [ignore]:\n' \
                           '            continue\n' \
                           '        line = line.rstrip(\'\\n\').split(delimiter)\n' \
                           '        output_handler.write(\',\'.join([callback]) + \'\\n\')' \
                           '\n' \
                           '\n',
            'filter_lines': '',
            'transpose': '',
            'delete_columns': '',
            'main_content': 'get_files()\n'
        }

        self.script_c = [self.script_container_text, self.script_container_id]
        self.script_i = [0, 1]

    def script_id_setter(self, which_one):
        self.script_c[1][max(self.script_i) + 1] = which_one
        self.script_i.append(max(self.script_i) + 1)

    def get_files_setter(self, what_thing, path):
        if what_thing == 'input':
            self.script_c[0]['get_files'] = self.script_c[0]['get_files'].replace(
                'INPUT_FILE_PATH_GOES_HERE', path)
        # elif what_thing == 'output':
        #     self.get_files.replace('OUTPUT_FILE_PATH_GOES_HERE', path)
        else:
            error = 'CompiledFile.get_files_setter execution error'
            raise RuntimeError(error)
        return None

    def manage_file_setter(self, what_thing, value):
        if what_thing == 'delimiter':
            self.script_c[0]['manage_file'] = self.script_c[0]['manage_file'].replace('[delimiter]',
                                                                                      value)
        elif what_thing == 'ignore lines':
            self.script_c[0]['manage_file'] = self.script_c[0]['manage_file'].replace('[ignore]',
                                                                                      str(value))
        elif what_thing == 'callback':
            self.script_c[0]['manage_file'] = self.script_c[0]['manage_file'].replace('[callback]',
                                                                                      value)
        elif what_thing == 'Headers':
            if value == 'none':
                self.script_c[0]['manage_file'] = self.script_c[0]['manage_file'].replace(
                        '        if number == 1:\n'
                        '            output_handler.write(line + \'\\n\')\n', '')
            else:
                self.script_c[0]['manage_file'] = self.script_c[0]['manage_file'].replace(
                        '        if number == 1:\n'
                        '            output_handler.write(line + \'\\n\')\n',
                        '        if number == 1:\n'
                        '            output_handler.write(\'' + value + '\' + \'\\n\')\n')

        else:
            error = 'CompiledFile.manage_file_setter execution error'
            raise RuntimeError(error)
        return None

    def headers_setter(self, what_thing, value):
        if what_thing == 'callback':
            self.script_c[0]['headers'] = self.script_c[0]['headers'].replace('[callback]', value)
        else:
            error = 'CompiledFile.headers_setter execution error'
            raise RuntimeError(error)
        return None

    def delete_columns_setter(self, what_thing, value):
        if what_thing == 'callback':
            self.script_c[0]['delete_columns'] = self.script_c[0]['delete_columns'].replace('[callback]', value)
        elif what_thing == 'list_to_delete':
            self.script_c[0]['delete_columns'] = self.script_c[0]['delete_columns'].replace('[list_to_delete]', value)
        else:
            error = 'CompiledFile.delete_columns_setter execution error'
            raise RuntimeError(error)
        return None

    def transpose_setter(self, what_thing, value):
        print('transpose_setter')

    def filter_lines_setter(self, what_thing, value):
        if what_thing == 'callback':
            self.script_c[0]['filter_lines'] = self.script_c[0]['filter_lines'].replace('[callback]', value)
        else:
            error = 'CompiledFile.filter_lines_setter execution error'
            raise RuntimeError(error)
        return None


class Parserclass:
    def __init__(self, statement_):
        self.statements = statement_.split(' ')
        while True:  # eliminates double spaces
            try:
                void = self.statements.pop(self.statements.index(''))
            except ValueError:
                break

        self.name = self.statements[0]
        if self.name == 'dir':
            self.input_path = os.path.dirname(__file__)
        else:
            self.input_path = os.path.dirname(__file__) + '/' + self.name

        self.output_path = os.path.dirname(__file__) + '/' + self.name.split('.')[0] + '_transformed.csv'
        self.execution_path = os.path.dirname(__file__) + '/' + self.name.split('.')[0] + '_execution.py'
        self.file_delimiter = statement[statement.find('[') + 1:statement.find(']')]
        self.new_delimiter = ','
        self.min_number_of_columns = 50


class TaskIdentifier:
    Keywords = ['Headers', 'Transpose', 'Filter', 'NewDelimiter', 'DeleteColumns']
    number_of_argument = {
        'Filter': (1, 1),
        'Headers': (1, 50),
        'Transpose': (1, 50),
        'NewDelimiter': (1, 1),
        'DeleteColumns': (1, 50),
    }
    task_switcher = {
        'Filter': filter_lines,
        'Headers': headers,
        'Transpose': transpose,
        'NewDelimiter': new_delimiter,
        'DeleteColumns': delete_columns
    }

    def __init__(self):
        self.task_indexes = []
        self.tasks = []
        self.ignore_x_lines = 1
        self.task_init_position = 2

        self.parse_statement_main_arguments()
        self.parse_functions_and_arguments()
        self.catch_new_delimiter()

    def parse_statement_main_arguments(self):
        if P.statements[2].lower() == 'ignore':
            try:
                self.ignore_x_lines = int(P.statements[3])
            except ValueError:
                error = 'Statement parsing error detected: found \'Ignore\' clause. Sintax: [Ignore x lines]'
                raise RuntimeError(error)
            if P.statements[4].lower() != 'lines':
                error = 'Statement parsing error detected: found \'Ignore\' clause. Sintax: [Ignore x lines]'
                raise RuntimeError(error)
            self.task_init_position = 5

        Compiled.manage_file_setter('ignore lines', self.ignore_x_lines)
        return

    def parse_functions_and_arguments(self):
        for word in P.statements[self.task_init_position:]:  # Identify Tasks in the statement and index their positions
            if word in self.Keywords:
                self.task_indexes.append(P.statements.index(word))

        for task in self.task_indexes:
            try:
                if task + 1 == self.task_indexes[self.task_indexes.index(task) + 1]:  # Function without arguments
                    new_task = [P.statements[task], []]
                else:  # Function with arguments
                    new_task = [P.statements[task], self.detect_complex_arguments(
                            P.statements[task + 1:self.task_indexes[self.task_indexes.index(task) + 1]])]
            except IndexError:
                if task == len(P.statements):  # If 'Task' is the last word in the statement
                    new_task = [P.statements[task], '']
                else:
                    new_task = [P.statements[task], self.detect_complex_arguments(P.statements[task + 1:])]
            self.tasks.append(new_task)

    def catch_new_delimiter(self):
        for task_looper in self.tasks:
            if task_looper[0] == 'NewDelimiter':
                self.tasks.insert(0, self.tasks.pop(self.tasks.index(task_looper)))
                break
        return None

    @staticmethod
    def detect_complex_arguments(args):
        processed_args = []
        complex_arg = ''
        for arg in args:
            if arg[-1] == ']':
                complex_arg = (complex_arg + ' ' + arg).lstrip(' ')
                processed_args.append(complex_arg)
                complex_arg = ''
            elif arg[0] == '[' or complex_arg != '':
                complex_arg = (complex_arg + ' ' + arg).lstrip(' ')
            else:
                processed_args.append(arg)
        return processed_args

    def execute(self, task):
        min_ = 0
        max_ = 1
        what_function = task[0]
        args = task[1]
        how_many_arguments = len(task[1])
        if how_many_arguments < self.number_of_argument[what_function][min_] or \
                        how_many_arguments > self.number_of_argument[what_function][max_]:
            error = 'Function ' + what_function + ' has been declared with the incorrect number of arguments \n\t\t\t  ' \
                                                  'Number of arguments declared: ' + str(
                how_many_arguments) + '\n\t\t\t  ' \
                                      'Valid number of arguments: ' + str(
                    self.number_of_argument[what_function][min_]) + ' to ' \
                                                                    '' + str(
                    self.number_of_argument[what_function][max_])
            raise RuntimeError(error)
        return self.task_switcher[what_function](args)


def input_check():
    if not os.path.isfile(P.input_path) and not os.path.isdir(P.input_path):
        error = P.name + ' does not exists in this folder.Script must be executed on the same folder of the _' \
                         'file you want to convert'
        raise RuntimeError(error)
    # noinspection PyBroadException
    if os.path.isfile(P.input_path):
        delimiter_check(open(P.input_path, 'r', encoding='utf-8'))
    else:
        for csv in os.listdir(P.input_path):
            if csv[-4:] != '.csv' or csv[-16:] == '_transformed.csv' or csv[-14:] == '_execution.csv':
                continue
            delimiter_check(open(csv, 'r', encoding='utf-8'))

    Compiled.get_files_setter('input', P.input_path)
    Compiled.manage_file_setter('delimiter', P.file_delimiter)
    return None


def delimiter_check(input_handler):
    try:
        firstline = input_handler.readline()
    except:
        error = 'Failed attempt to read file ' + input_handler.name + '. Sure the format is correct?'
        raise RuntimeError(error)
    number_of_columns = len(firstline.split(P.file_delimiter))
    if number_of_columns == 1 and P.file_delimiter != 'single':
        error = 'Either ' + input_handler.name + ' is not delimited by \"' + P.file_delimiter + '\" or you pointed ' \
                                                                                                'to a single row csv. To point a single row csv, set \"single\" as the delimiter'
        raise RuntimeError(error)
    P.min_number_of_columns = min(number_of_columns, P.min_number_of_columns)
    return None


def output_check():
    if os.path.isfile(P.output_path):
        error = P.name.split('.')[0] + '_transformed.csv' + ' already exists. Delete or rename it before executing'
        raise RuntimeError(error)
    return None


def write_execution_file():
    output_handler = open(P.execution_path, 'w', encoding='utf-8')

    Compiled.script_id_setter('main_content')
    # execution_file = '\n'.join((Compiled.get_files, Compiled.manage_file))
    execution_file = Compiled.script_c[0][Compiled.script_c[1][0]]
    for script in sorted(Compiled.script_i)[1:]:
        execution_file = '\n'.join((execution_file, Compiled.script_c[0][Compiled.script_c[1][script]]))

    output_handler.write(execution_file)
    return None


statement = 'Csv_test.csv  [,] Headers NumeroFeo NumeroGuapo NewDelimiter [;] DeleteColumns 1 Filter [int(line[1]) >= 5 and int(line[1]) <=100]'
# TODO Sistema de -H --help y [FunctionName]
# statement_sintax = 'Filename|dir [delimiter|single] [Ignore x lines] [OperationName option1 option2 option3...]' \
#                    '[OperationName option1 option2 option3...] ...'
statement_sintax = 'Filename|dir [delimiter|single] [Ignore x lines] [OperationName option1 option2 option3...]' \
                   '[OperationName option1 option2 option3...] ...'

print('<<<<<<<<<<Statement sintax>>>>>>>>>>', '\n' + statement_sintax, '\n')
print('Statement received:', '\n' + statement, '\n', '\nResolves into', '\n')

Compiled = CompiledFile()
P = Parserclass(statement)
output_check()
input_check()
T = TaskIdentifier()
print(T.tasks)

message = '\nCsv manager will apply '
for task in T.tasks:
    message = message + task[0] + ' -> '
message = message.rstrip(' -> ')
print(message)

__next_callback__ = 'manage_file'
for next_task in T.tasks:
    T.execute(next_task)
Compiled.callback_switcher[__next_callback__]('callback', 'line')
__next_callback__ = 'Pipeline reached its end'

write_execution_file()
print('You reached the end')

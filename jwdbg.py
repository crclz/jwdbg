import os
import sys
import yaml
import subprocess
import io
import argparse

if sys.version_info[0] < 3 or sys.version_info[1] < 7:
    print('Require python 3.7+')
    exit(-1)

parser = argparse.ArgumentParser(description="jwdbg arguments")
parser.add_argument('-cmd', required=True,
                    help="command to run the target program")
parser.add_argument('-case', required=True,
                    help="testcase file, e.g. case1.yml")
parser.add_argument('-inputdata', action='store_true')

args = parser.parse_args()

case_file = args.case

with open(case_file, 'r', encoding="utf-8") as f:
    testcase = yaml.load(f, Loader=yaml.SafeLoader)

print(f"test name: {testcase['name']}")

if testcase.__contains__('warn'):
    print("**** warn **************")
    print(testcase['warn'])
    print("************************")

# get input and output lines from test data
# make sure each item of these 2 lists does not end with \n, \r\n (by calling strip())
input_lines = []
output_lines = []

# 1 command may has more than 1 line of output
# belong_to[output_line_index]==its input line index
belong_to = dict()

for item in testcase['data']:

    current_output = None

    if isinstance(item, str):
        # input with no output
        current_input_line = str(item).strip()
    elif isinstance(item, list):
        # input with output
        if len(item) != 2:
            raise Exception(f"Test data wrong format. {str(item)}")
        current_input_line = str(item[0]).strip()
        current_output = str(item[1]).strip()
    else:
        raise Exception(f"Test data wrong format. {str(item)}")

    input_lines.append(current_input_line)

    if current_output != None:
        for line in current_output.splitlines(keepends=False):
            line = line.strip()
            output_lines.append(line)
            belong_to[len(output_lines)-1] = len(input_lines)-1

# all input
if args.inputdata:
    print("All input data:")
    print("============================")
    print('\n'.join(input_lines))
    print("============================")
    exit(0)

# run program and get output

cmd = args.cmd
input_data = "\n".join(input_lines).encode("utf-8")
output_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE).communicate(input_data, timeout=5)[0]
actual_lines = output_data.decode().splitlines(keepends=False)

# compare actual output lines and expected lines

smaller_len = min(len(actual_lines), len(output_lines))
ok = True

i = 0
while i < smaller_len:
    if output_lines[i] != actual_lines[i]:
        ok = False
        print("test failure")
        print("================")
        print(f"expected: {output_lines[i]}")
        print(f"actual:   {actual_lines[i]}")
        print("================")
        break
    i += 1

if not ok:
    print('The last command of the following lines caused the error.')
    print('Please copy these lines for debugging:')
    x = belong_to[i]
    i = 0
    while i <= x:
        print(input_lines[i])
        i += 1
    exit(2)

if len(actual_lines) != len(output_lines):
    print("test failed")
    print("last command output line count mismatch")

    if len(actual_lines) > len(output_lines):
        print("actual lines are more than expected. extra lines:")
        print("================")
        for l in actual_lines[smaller_len:]:
            print(l)
        print("================")
    else:
        print("actual lines are less than expected. expect more lines:")
        print("================")
        for l in output_lines[smaller_len:]:
            print(l)
        print("================")
    
    # print all input lines
    print()
    print('Please copy these lines for debugging:')
    for line in input_lines:
        print(line)


    exit(3)

print("test passed")
exit(0)

import os
import sys
import yaml
import subprocess
import io
import argparse
import difflib
from colorama import Fore, Style

RESET_ALL = Style.RESET_ALL

if sys.version_info[0] < 3 or sys.version_info[1] < 7:
    print('Require python 3.7+')
    print()
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

print()

print(f"test name: {Fore.CYAN}{testcase['name']}{RESET_ALL}")
print()

if testcase.__contains__('warn'):
    print(f"{Fore.LIGHTYELLOW_EX}warn:")
    print(f"{testcase['warn']}{RESET_ALL}")
    print()

# get input and output contents from test data
# make sure each item of these 2 lists does not end with \n, \r\n (by calling strip())
input_lines = []
output_contents = []

# 一个输入行对应一个输出内容。
# 无输出 - None
# 一行输出 - 普通字符串
# 多行输出 - 以‘\n’分隔的字符串


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
        current_output = str(item[1]).replace('\r\n', '\n').strip()
    else:
        raise Exception(f"Test data wrong format. {str(item)}")

    input_lines.append(current_input_line)
    output_contents.append(current_output)

# all input
if args.inputdata:
    print("All input data:")
    print("============================")
    print('\n'.join(input_lines))
    print("============================")
    print()
    exit(0)

# run program and get output

# TODO: set env JWDBG=debugging
os.environ['JWDBG'] = "debugging"
cmd = args.cmd
input_data = "\n".join(input_lines).encode("utf-8")
output_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE).communicate(input_data, timeout=5)[0]
actual_lines = output_data.decode().splitlines(keepends=False)


# integration check
echo_lines = [x for x in actual_lines if x.startswith("[Echo]")]

if len(echo_lines) != len(input_lines):
    print(f"{Fore.RED}Echo lines ([Echo]) integration check failure.")
    print(f"Please view ndbg.py document.{RESET_ALL}")
    print()
    exit(-10)

for i in range(len(echo_lines)):
    if echo_lines[i] != ("[Echo]"+input_lines[i]):
        print("echo lines integration check failure")
        print()
        exit(-10)


# actual output lines ===> actual output contents

actual_contents = []

is_start = True
buf = None

for line in actual_lines:
    if line.startswith('[Echo]'):
        if not is_start:
            # flush buf; reset buf
            actual_contents.append(None if buf == None else buf.rstrip())
            buf = None
    else:
        buf = (buf or "") + line + '\n'
    is_start = False
    pass

# flush buf
actual_contents.append(None if buf == None else buf.rstrip())


assert len(actual_contents) == len(input_lines)
assert len(actual_contents) == len(output_contents)


# compare actual_contents and output_contents

for i in range(len(actual_contents)):
    actual = actual_contents[i]
    expected = output_contents[i]

    if(expected != actual):
        print(f"{Fore.RED}Test failed.{Style.RESET_ALL}")
        print()
        print(f"{Fore.GREEN}================ expected ================{RESET_ALL}")
        print(expected)
        print(f"{Fore.YELLOW}================ actual   ================{RESET_ALL}")
        print(actual)
        print("==========================================")
        print()
        print()
        print(
            f"{Fore.CYAN}================ diff (difflib, 如果上面看不清楚，可以看这里) ============={RESET_ALL}")

        if expected!=None:
            k = difflib.Differ().compare(expected.splitlines(
                keepends=False), actual.splitlines(keepends=False))

            diff_info = '\n'.join(k)

            print(diff_info)
            print("=============================================")
            print()
            # d = difflib.HtmlDiff()
            # file = d.make_file(expected.splitlines(
            #     keepends=False), actual.splitlines(keepends=False))
            # table = d.make_table(expected.splitlines(
            #     keepends=False), actual.splitlines(keepends=False))
            # with open("1.diff.html","w") as f:
            #     f.write(file)

        # print input lines for debugging
        print(f'{Fore.YELLOW}The last command of the following lines caused the error.')
        print(f'Please copy these lines for debugging:{RESET_ALL}')

        for x in range(i+1):
            print(input_lines[x])
        print("==============================================")
        print()

        exit(-1)

print(f"{Fore.LIGHTGREEN_EX}Test passed!{RESET_ALL}")
print()
exit(0)

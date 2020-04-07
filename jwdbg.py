import os
import yaml
import subprocess
import io

case_file = './case1.yml'

with open(case_file, 'r', encoding="utf-8") as f:
    testcase = yaml.load(f, Loader=yaml.SafeLoader)


def get_input_output(data, until):
    input_str = ""
    output_str = ""

    i = 0
    for item in data:
        if not i < until:
            break

        output_line = None

        if isinstance(item, str):
            # input with no output
            line = str(item)
        elif isinstance(item, list):
            # input with output
            if len(item) != 2:
                raise Exception(f"Test data wrong format. {str(item)}")
            line = str(item[0])
            output_line = str(item[1])
        else:
            raise Exception(f"Test data wrong format. {str(item)}")

        if not line.endswith("\n"):
            line += "\n"
        input_str += line

        if output_line != None:
            if not output_line.endswith("\n"):
                output_line += "\n"
            output_str += output_line

        i += 1

    return input_str, output_str


def get_program_output(cmd, input_str):
    input_data = input_str.encode()
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stdin=subprocess.PIPE).communicate(input_data)[0]

    return output.decode()


input_str, expected_output = get_input_output(testcase['data'], 99999)

os.chdir("E:/personal/学习/大二下/面向对象/jw_idea/target/classes")

actual_output = get_program_output("java Test", input_str)

actual_lines = actual_output.splitlines(keepends=False)
expected_lines = expected_output.splitlines(keepends=False)

smaller_len = min(len(actual_lines), len(expected_lines))

# compare actual lines and expected lines

ok = True
cursor = 0
tc_cursor = 0
for item in testcase['data']:
    if not cursor < smaller_len:
        break

    if isinstance(item, list):
        # input with output
        actual = actual_lines[cursor]

        for actual_line in actual.splitlines(keepends=False):
            expected = expected_lines[cursor]

            if expected != actual_line:
                ok = False
                print("line mismatch.")
                print(f">>> expected:\t{expected}")
                print(f">>> actual:\t{actual_line}")
                break
            cursor += 1

        if not ok:
            break

    tc_cursor += 1

if not ok:
    print("test failed")
    print("The last command of the following lines caused the error. Please copy to debug your code.")
    print()
    input_lines = input_str.splitlines(keepends=False)
    for l in input_lines[:tc_cursor+1]:
        print(l)
    exit(2)

if len(actual_lines) != len(expected_lines):
    print("test failed")
    print("last command output line count mismatch")
    print("========")
    print("expected:")
    for l in expected_lines[cursor:]:
        print(l)

    print("========")
    print("The last command(which has output) of the following lines caused the error. Please copy to debug your code.")
    input_lines = input_str.splitlines(keepends=False)
    for l in input_lines:
        print(l)
    exit(3)

print('test passed!')
exit(0)

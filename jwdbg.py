import os
import yaml
import subprocess
import io

case_file = './case1.yml'

with open(case_file, 'r', encoding="utf-8") as f:
    testcase = yaml.load(f, Loader=yaml.SafeLoader)

print(f"test name: {testcase['name']}")

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


# run program and get output

os.chdir("E:/personal/学习/大二下/面向对象/jw_idea/target/classes")
cmd = "java Test"
input_data = "\n".join(input_lines).encode("utf-8")
output_data = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE).communicate(input_data)[0]
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
        print(f"expected:\t{output_lines[i]}")
        print(f"actual:\t\t{actual_lines[i]}")
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
    exit(3)

print("test passed")
exit(0)

import argparse
import os
import sys
import subprocess
import shutil

zip_path = "./to_submit.zip"
last_temp = "./lastcheck_temp"

parser = argparse.ArgumentParser(description="jw lastcheck arguments")
parser.add_argument('-case', required=True,
                    help="testcase file, e.g. case1.yml")

args = parser.parse_args()

test_case = args.case

# zip file exist
if not os.path.exists(zip_path):
    print("zip file not exist")
    exit(-1)

# remove last_temp if exist
if os.path.exists(last_temp):
    shutil.rmtree(last_temp)

# unzip
subprocess.call(['python', '-m', 'zipfile', '-e', zip_path, last_temp])

# compile

# 防止git-bash javac命令行输出中文乱码
# os.environ['JAVA_TOOL_OPTIONS'] = "-Dfile.encoding=UTF8"

os.chdir(last_temp)

# optional: -encoding UTF-8 GBK
ret = subprocess.call(
    "javac -cp ./src ./src/*.java -Xlint:unchecked -encoding UTF-8")

if ret != 0:
    print("compile failure")
    exit(-2)

print("compile success")

# del os.environ['JAVA_TOOL_OPTIONS']  # unset


# do test
os.chdir('..')

subprocess.call(['python', 'jwdbg.py', '-case', test_case,
                 '-cmd', f"java -cp ./{last_temp}/src   Test"])

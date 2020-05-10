# !/bin/bash
echo ""
zip_path="./to_submit.zip"
last_temp="./lastcheck_temp"
test_case=$1

JAVA_TOOL_OPTIONS="-Dfile.encoding=UTF-8" # 防止git-bash javac命令行输出中文乱码

[[ -e $last_temp ]] && rm -r $last_temp # remove last_temp if exist

unset JAVA_TOOL_OPTIONS

[[ -f $zip_path ]] || { echo "Zip file not exist: $zip_path"; exit -1; }

python -m zipfile -e $zip_path $last_temp

cd $last_temp

javac -cp ./src ./src/*.java -Xlint:unchecked -encoding UTF-8 || { echo "compile failure"; exit -1 ; } # optional: -encoding UTF-8 GBK
echo "compile success"
echo ""

cd ..

python jwdbg.py -case $test_case -cmd "java -cp ./$last_temp/src   Test"
# coding = utf-8

import os
import re
import sys

output_location = "./"
for root, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        if re.match("^.*\\.java$", file) is not None:
            print(os.path.join(root, file))
            in_file = open(os.path.join(root, file), "r")
            out_file = open(os.path.join(output_location, file), "w")
            for code in in_file:
                if re.match("^package[.\n]*", code):
                    continue
                if re.match("^import[.\n]*", code) and not re.match("^import java[.\n]*", code):
                    continue
                out_file.write(code)
            out_file.close()

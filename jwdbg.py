import yaml

case_file = './case1.yml'

with open(case_file) as f:
    testcase = yaml.load(f, Loader=yaml.SafeLoader)


def gen_input(data):
    input_str = ""

    for item in data:
        if isinstance(item, str):
            # input with no output
            line = str(item)
        elif isinstance(item, list):
            # input with output
            if len(item) != 2:
                raise Exception(f"Test data wrong format. {str(item)}")
            line = str(item[0])
        else:
            raise Exception(f"Test data wrong format. {str(item)}")

        if not line.endswith("\n"):
            line += "\n"

        input_str += line

    return input_str


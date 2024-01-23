import json
import yaml
import sys
import os

def add_to_file(file_path: str, line: str) -> None:
    with open(file_path, "a") as f:
        f.write(f"{line}\n")

def parse_mindmap_dict(mindmap_dict: dict, max_recursion_limit: int=5, level: int=1) -> None:
    global output_file_path
    if max_recursion_limit == 0:
        return
    for key, value in mindmap_dict.items():
        if key == "i--": #? image code
            for image_name, image_data in value.items():
                add_to_file(output_file_path, f"{'#'*(level)} ![alt text]({image_data[0]}) {image_name}")
            continue


        add_to_file(output_file_path, f"{'#'*level} {key}") #* Adds #s equal to the current level + 1 as well as the name of the branch
        if type(value) == dict:
            parse_mindmap_dict(value, max_recursion_limit-1, level+1)
        elif type(value) == list:
            if max_recursion_limit-1 == 0: #* Stops code if it would pass the recursion limit
                continue
            for element in value:
                add_to_file(output_file_path, f"{'#'*(level+1)} {element}")



def read_json(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return json.loads(f.read())

def read_yaml(file_path: str) -> dict:
    with open(file_path, "r") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)
            return {}

output_file_path = ""
def convert_file(input_file_path: str, output_file_path_a: str="output.md"): #? _a is argument
    global output_file_path
    output_file_path = output_file_path_a

    # match input_file_path.split(".")[-1]
    mindmap_dict = {}
    if not os.path.exists(input_file_path):
        raise Exception (f"\n  Invalid file_path\n  {input_file_path} does not exist")
    if input_file_path.split(".")[-1] == ".json":
        mindmap_dict = read_json(input_file_path) 
    else:
        mindmap_dict = read_yaml(input_file_path)
    open(output_file_path, "w")
    parse_mindmap_dict(mindmap_dict)



if __name__ == "__main__":
    error = False
    try:
        convert_file(sys.argv[1], sys.argv[2])
    except IndexError:
        error = True
    if error:
        raise Exception (f"\n  Invalid arguments.\n  Expected [<input_file_path>, <output_file_path>] but recieved {sys.argv[1:]}")
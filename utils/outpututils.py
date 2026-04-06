import numpy as np
import hashlib
import shutil

def create_submission_txt(filename, value, precision=6):
    np.set_printoptions(suppress=True, precision=precision)
    
    with open(filename, "w") as f:
        if type(value) == float or type(value) == int: 
            print(value, file=f)
        elif type(value) == list:
            print(*value, file=f)
        elif type(value) == np.ndarray:  
            print(*value.flatten(), file=f)

def copy_submission_txt(in_path, out_path):
    shutil.copy(in_path, out_path)

def hash_submission_txt(in_path, out_path):
    with open(in_path, "rb") as input, open(out_path, "w") as output:
        print(hashlib.file_digest(input, "sha256").hexdigest(), file=output)

import numpy as np

def create_submission_txt(filename, value, precision=6):
    np.set_printoptions(suppress=True, precision=precision)
    
    with open(filename, "w") as f:
        if type(value) == float or type(value) == int: 
            print(value, file=f)
        elif type(value) == list:
            print(*value, file=f)
        elif type(value) == np.ndarray:  
            print(*value.flatten(), file=f)

from pathlib import Path

from utils.outpututils import hash_submission_txt

for path in Path('output').rglob("*"):
    if path.is_file():
        hash_submission_txt(path, "test/" + path.parts[1] + "/" + path.parts[2])
        
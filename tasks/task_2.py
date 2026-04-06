from pathlib import Path

from utils.projectutils import LMO_mission
from utils.outpututils import create_submission_txt

t_LMO = 300
HN = LMO_mission.get_HN(t_LMO)

Path("output/task_2").mkdir(parents=True, exist_ok=True)
create_submission_txt("output/task_2/HN.txt", HN)

from pathlib import Path

from utils.projectutils import LMO_mission
from utils.outpututils import create_submission_txt

RsN = LMO_mission.get_RsN()
N_omega_RsN = LMO_mission.get_N_omega_RsN()

Path("output/task_3").mkdir(parents=True, exist_ok=True)
create_submission_txt("output/task_3/RsN.txt", RsN)
create_submission_txt("output/task_3/N_omega_RsN.txt", N_omega_RsN)

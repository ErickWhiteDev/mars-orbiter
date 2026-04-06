from pathlib import Path

from utils.projectutils import LMO_mission
from utils.outpututils import create_submission_txt

t_LMO = 330 # [s]
RnN = LMO_mission.get_RnN(t_LMO)
N_omega_RnN = LMO_mission.get_N_omega_RnN(t_LMO)

Path("output/task_4").mkdir(parents=True, exist_ok=True)
create_submission_txt("output/task_4/RnN.txt", RnN)
create_submission_txt("output/task_4/N_omega_RnN.txt", N_omega_RnN)

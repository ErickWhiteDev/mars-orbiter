from pathlib import Path

from utils.projectutils import LMO_mission, GMO_mission
from utils.outpututils import create_submission_txt

t_LMO = 330 # [s]
RcN = LMO_mission.get_RcN(t_LMO, GMO_mission)
N_omega_RcN = LMO_mission.get_N_omega_RcN(t_LMO, GMO_mission)

Path("output/task_5").mkdir(parents=True, exist_ok=True)
create_submission_txt("output/task_5/RcN.txt", RcN)
create_submission_txt("output/task_5/N_omega_RcN.txt", N_omega_RcN)

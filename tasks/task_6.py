from pathlib import Path

from utils.projectutils import LMO_mission, LMO_attitude, GMO_mission
from utils.outpututils import create_submission_txt

t_LMO = 0 #[s]
RsN = LMO_mission.get_RsN()
N_omega_RsN = LMO_mission.get_N_omega_RsN()
RnN = LMO_mission.get_RnN(t_LMO)
N_omega_RnN = LMO_mission.get_N_omega_RnN(t_LMO)
RcN = LMO_mission.get_RcN(t_LMO, GMO_mission)
N_omega_RcN = LMO_mission.get_N_omega_RcN(t_LMO, GMO_mission)

B_omega_BRs, sigma_BRs = LMO_attitude.get_tracking_error(RsN, N_omega_RsN)
B_omega_BRn, sigma_BRn = LMO_attitude.get_tracking_error(RnN, N_omega_RnN)
B_omega_BRc, sigma_BRc = LMO_attitude.get_tracking_error(RcN, N_omega_RcN)

Path("output/task_6").mkdir(parents=True, exist_ok=True)
create_submission_txt("output/task_6/B_omega_BRs.txt", B_omega_BRs)
create_submission_txt("output/task_6/sigma_BRs.txt", sigma_BRs)
create_submission_txt("output/task_6/B_omega_BRn.txt", B_omega_BRn)
create_submission_txt("output/task_6/sigma_BRn.txt", sigma_BRn)
create_submission_txt("output/task_6/B_omega_BRc.txt", B_omega_BRc)
create_submission_txt("output/task_6/sigma_BRc.txt", sigma_BRc)

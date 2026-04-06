from pathlib import Path
import numpy as np

from utils.projectutils import LMO_orbit, GMO_orbit
from utils.orbit import angles2state
from utils.outpututils import create_submission_txt

t_LMO = 450 # [s]
theta_LMO = LMO_orbit.find_true_anomaly(t_LMO) # [rad]
I_r_LMO, I_v_LMO = angles2state(np.linalg.norm(LMO_orbit.rvec), LMO_orbit.Omega, LMO_orbit.i, theta_LMO, LMO_orbit.planet.mu)

t_GMO = 1150 # [s]
theta_GMO = GMO_orbit.find_true_anomaly(t_GMO) # [rad]
I_r_GMO, I_v_GMO = angles2state(np.linalg.norm(GMO_orbit.rvec), GMO_orbit.Omega, GMO_orbit.i, theta_GMO, GMO_orbit.planet.mu)

Path("output/task_1").mkdir(parents=True, exist_ok=True)
create_submission_txt("output/task_1/r_LMO.txt", I_r_LMO)
create_submission_txt("output/task_1/v_LMO.txt", I_v_LMO)
create_submission_txt("output/task_1/r_GMO.txt", I_r_GMO)
create_submission_txt("output/task_1/v_GMO.txt", I_v_GMO)

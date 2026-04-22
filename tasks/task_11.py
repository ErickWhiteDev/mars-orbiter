from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt

from utils.projectutils import LMO_mission, GMO_mission
from utils.outpututils import create_submission_txt

h = 1 # [s]

P = 1 / 6
K = 1 / 180

t_LMO = 6500 # [s]
max_comms_angle = np.deg2rad(35) # [deg]

t_LMO, yapp_LMO, u_LMO = LMO_mission.RK4_mission(0, t_LMO, h, GMO_mission, max_comms_angle, P, K)

mrp_LMO = yapp_LMO[:, 6:9]
omega_LMO = yapp_LMO[:, 9:12]

fig_state, ax_state = plt.subplots(3, 1, sharex=True)

ax_state[0].plot(t_LMO, mrp_LMO, linewidth=3)
ax_state[0].set_ylabel('MRP')
ax_state[0].legend([f'$\\sigma_1$', f'$\\sigma_2$', f'$\\sigma_3$'])
ax_state[0].grid()

ax_state[1].plot(t_LMO, omega_LMO, linewidth=3)
ax_state[1].set_ylabel('Angular Velocity [rad / s]')
ax_state[1].legend([f'$\\omega_1$', f'$\\omega_2$', f'$\\omega_3$'])
ax_state[1].grid()

ax_state[2].plot(t_LMO, u_LMO, linewidth=3)
ax_state[2].set_xlabel('Time [s]')
ax_state[2].set_ylabel('Control Torque [N * m]')
ax_state[2].legend([f'$\\tau_1$', f'$\\tau_2$', f'$\\tau_3$'])
ax_state[2].grid()

fig_state.suptitle('LMO Attitude Propagation')
fig_state.tight_layout()

Path("output/task_11").mkdir(parents=True, exist_ok=True)
create_submission_txt("output/task_11/mrp_300.txt", mrp_LMO[np.where(t_LMO == 300)[0][0]])
create_submission_txt("output/task_11/mrp_2100.txt", mrp_LMO[np.where(t_LMO == 2100)[0][0]])
create_submission_txt("output/task_11/mrp_3400.txt", mrp_LMO[np.where(t_LMO == 3400)[0][0]])
create_submission_txt("output/task_11/mrp_4400.txt", mrp_LMO[np.where(t_LMO == 4400)[0][0]])
create_submission_txt("output/task_11/mrp_5600.txt", mrp_LMO[np.where(t_LMO == 5600)[0][0]])

plt.show()

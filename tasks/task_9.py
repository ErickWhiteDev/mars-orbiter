from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt

from utils.attitude import RK4_mrp, mrp2dcm, dcm2mrp
from utils.projectutils import LMO_attitude, LMO_spacecraft, LMO_mission
from utils.outpututils import create_submission_txt

h = 1 # [s]

P = 1 / 6
K = 1 / 180
mrp_BRn = lambda mrp, t: dcm2mrp(mrp2dcm(mrp) @ LMO_mission.get_RnN(t).T)
omega_BRn = lambda t, mrp, omega: omega - mrp2dcm(mrp) @ LMO_mission.get_N_omega_RnN(t)

def u(t, attitude, omega, **__):
    mrp = mrp_BRn(attitude, t)
    omega = omega_BRn(t, attitude, omega)
    return -K * mrp - P * omega

t_LMO = 400 # [s]

X0 = LMO_attitude.get_state('MRP')
mrp_0 = X0[0:3]
omega_0 = X0[3:6]

t_LMO, yapp_LMO, u_LMO = RK4_mrp(0, t_LMO, h, np.hstack((mrp_0, omega_0)), LMO_spacecraft.I, control_law=u)

mrp_LMO = yapp_LMO[:, 0:3]
mrp_error_LMO = np.linalg.norm(np.array([mrp_BRn(mrp_LMO[i], t_LMO[i]) for i in range(len(t_LMO))]), axis=1)
omega_LMO = yapp_LMO[:, 3:6]

fig_state, ax_state = plt.subplots(3, 1, sharex=True, figsize=(10, 8))

ax_state[0].plot(t_LMO, mrp_LMO, linewidth=3)
ax_state[0].set_ylabel('MRP', fontsize=14)
ax_state[0].legend([f'$\\sigma_1$', f'$\\sigma_2$', f'$\\sigma_3$'], fontsize=12)
ax_state[0].grid()

ax_state[1].plot(t_LMO, omega_LMO, linewidth=3)
ax_state[1].set_ylabel('Angular Velocity [rad / s]', fontsize=14)
ax_state[1].legend([f'$\\omega_1$', f'$\\omega_2$', f'$\\omega_3$'], fontsize=12)
ax_state[1].grid()

ax_state[2].plot(t_LMO, u_LMO, linewidth=3)
ax_state[2].set_xlabel('Time [s]', fontsize=14)
ax_state[2].set_ylabel('Control Torque [N * m]', fontsize=14)
ax_state[2].legend([f'$\\tau_1$', f'$\\tau_2$', f'$\\tau_3$'], fontsize=12)
ax_state[2].grid()

fig_state.suptitle('LMO State and Control Propagation', fontsize=16)
fig_state.tight_layout()

fig_error, ax_error = plt.subplots(figsize=(10, 8))
ax_error.plot(t_LMO, mrp_error_LMO, linewidth=3)

ax_error.set_xlabel('Time [s]', fontsize=14)
ax_error.set_ylabel('MRP Error', fontsize=14)
ax_error.set_title('LMO MRP Error', fontsize=16)
ax_error.grid()

Path("output/task_9").mkdir(parents=True, exist_ok=True)
create_submission_txt("output/task_9/mrp_15.txt", mrp_LMO[np.where(t_LMO == 15)[0][0]])
create_submission_txt("output/task_9/mrp_100.txt", mrp_LMO[np.where(t_LMO == 100)[0][0]])
create_submission_txt("output/task_9/mrp_200.txt", mrp_LMO[np.where(t_LMO == 200)[0][0]])
create_submission_txt("output/task_9/mrp_400.txt", mrp_LMO[np.where(t_LMO == 400)[0][0]])

plt.show()

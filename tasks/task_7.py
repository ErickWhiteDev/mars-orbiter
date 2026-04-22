from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt

from utils.attitude import RK4_mrp, mrp2dcm
from utils.projectutils import LMO_attitude, LMO_spacecraft
from utils.outpututils import create_submission_txt

h = 1 # [s]

t_zero_LMO = 500 # [s]
t_zero_LMO, yapp_zero_LMO, u_zero_LMO = RK4_mrp(0, t_zero_LMO, h, LMO_attitude.get_state('MRP'), LMO_spacecraft.I)

mrp_zero_LMO = yapp_zero_LMO[:, 0:3]
omega_zero_LMO = yapp_zero_LMO[:, 3:6]

fig_zero_state, ax_zero_state = plt.subplots(3, 1, sharex=True)

ax_zero_state[0].plot(t_zero_LMO, mrp_zero_LMO, linewidth=3)
ax_zero_state[0].set_ylabel('MRP')
ax_zero_state[0].legend([f'$\\sigma_1$', f'$\\sigma_2$', f'$\\sigma_3$'])
ax_zero_state[0].grid()

ax_zero_state[1].plot(t_zero_LMO, omega_zero_LMO, linewidth=3)
ax_zero_state[1].set_ylabel('Angular Velocity [rad / s]')
ax_zero_state[1].legend([f'$\\omega_1$', f'$\\omega_2$', f'$\\omega_3$'])
ax_zero_state[1].grid()

ax_zero_state[2].plot(t_zero_LMO, u_zero_LMO, linewidth=3)
ax_zero_state[2].set_xlabel('Time [s]')
ax_zero_state[2].set_ylabel('Control Torque [N * m]')
ax_zero_state[2].legend([f'$\\tau_1$', f'$\\tau_2$', f'$\\tau_3$'])
ax_zero_state[2].grid()

fig_zero_state.suptitle('LMO Attitude Propagation')
fig_zero_state.tight_layout()

t_const_LMO = 100 # [s]
u_const = lambda t, attitude, omega, **kwargs: np.array([0.01, -0.01, 0.02])
t_const_LMO, yapp_const_LMO, u_const_LMO = RK4_mrp(0, t_const_LMO, h, LMO_attitude.get_state('MRP'), LMO_spacecraft.I, control_law=u_const)

mrp_const_LMO = yapp_const_LMO[:, 0:3]
omega_const_LMO = yapp_const_LMO[:, 3:6]
fig_const_state, ax_const_state = plt.subplots(3, 1, sharex=True)

ax_const_state[0].plot(t_const_LMO, mrp_const_LMO, linewidth=3)
ax_const_state[0].set_ylabel('MRP')
ax_const_state[0].legend([f'$\\sigma_1$', f'$\\sigma_2$', f'$\\sigma_3$'])
ax_const_state[0].grid()

ax_const_state[1].plot(t_const_LMO, omega_const_LMO, linewidth=3)
ax_const_state[1].set_ylabel('Angular Velocity [rad / s]')
ax_const_state[1].legend([f'$\\omega_1$', f'$\\omega_2$', f'$\\omega_3$'])
ax_const_state[1].grid()

ax_const_state[2].plot(t_const_LMO, u_const_LMO, linewidth=3)
ax_const_state[2].set_xlabel('Time [s]')
ax_const_state[2].set_ylabel('Control Torque [N * m]')
ax_const_state[2].legend([f'$\\tau_1$', f'$\\tau_2$', f'$\\tau_3$'])
ax_const_state[2].grid()

fig_const_state.suptitle('LMO Attitude Propagation with Constant Control')
fig_const_state.tight_layout()

Path("output/task_7").mkdir(parents=True, exist_ok=True)
create_submission_txt("output/task_7/B_H.txt", LMO_spacecraft.I @ omega_zero_LMO[-1])
create_submission_txt("output/task_7/T.txt", 0.5 * omega_zero_LMO[-1].T @ LMO_spacecraft.I @ omega_zero_LMO[-1])
create_submission_txt("output/task_7/zero_mrp.txt", mrp_zero_LMO[-1])
create_submission_txt("output/task_7/N_H.txt", mrp2dcm(mrp_zero_LMO[-1]).T @ (LMO_spacecraft.I @ omega_zero_LMO[-1]))
create_submission_txt("output/task_7/const_mrp.txt", mrp_const_LMO[-1])

plt.show()

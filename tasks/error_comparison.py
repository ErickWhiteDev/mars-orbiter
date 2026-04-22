import numpy as np
from matplotlib import pyplot as plt

from utils.attitude import RK4_mrp, mrp2dcm, dcm2mrp
from utils.projectutils import LMO_attitude, LMO_spacecraft, LMO_mission, GMO_mission

h = 1 # [s]

P = 1 / 6
K = 1 / 180
mrp_BRs = lambda mrp: dcm2mrp(mrp2dcm(mrp) @ LMO_mission.get_RsN().T)
omega_BRs = lambda mrp, omega: omega - mrp2dcm(mrp) @ LMO_mission.get_N_omega_RsN()
mrp_BRn = lambda mrp, t: dcm2mrp(mrp2dcm(mrp) @ LMO_mission.get_RnN(t).T)
omega_BRn = lambda t, mrp, omega: omega - mrp2dcm(mrp) @ LMO_mission.get_N_omega_RnN(t)
mrp_BRc = lambda mrp, t: dcm2mrp(mrp2dcm(mrp) @ LMO_mission.get_RcN(t, GMO_mission).T)
omega_BRc = lambda t, mrp, omega: omega - mrp2dcm(mrp) @ LMO_mission.get_N_omega_RcN(t, GMO_mission)

def u_BRs(_, attitude, omega, **__):
    mrp = mrp_BRs(attitude)
    omega = omega_BRs(attitude, omega)
    return -K * mrp - P * omega

def u_BRn(t, attitude, omega, **__):
    mrp = mrp_BRn(attitude, t)
    omega = omega_BRn(t, attitude, omega)
    return -K * mrp - P * omega

def u_BRc(t, attitude, omega, **__):
    mrp = mrp_BRc(attitude, t)
    omega = omega_BRc(t, attitude, omega)
    return -K * mrp - P * omega

t_LMO = 400 # [s]

X0 = LMO_attitude.get_state('MRP')
mrp_0 = X0[0:3]
omega_0 = X0[3:6]

t_BRs, yapp_BRs, u_BRs = RK4_mrp(0, t_LMO, h, np.hstack((mrp_0, omega_0)), LMO_spacecraft.I, control_law=u_BRs)
t_BRn, yapp_BRn, u_BRn = RK4_mrp(0, t_LMO, h, np.hstack((mrp_0, omega_0)), LMO_spacecraft.I, control_law=u_BRn)
t_BRc, yapp_BRc, u_BRc = RK4_mrp(0, t_LMO, h, np.hstack((mrp_0, omega_0)), LMO_spacecraft.I, control_law=u_BRc)

mrp_BRs_arr = yapp_BRs[:, 0:3]
mrp_error_BRs = np.linalg.norm(np.array([mrp_BRs(mrp) for mrp in mrp_BRs_arr]), axis=1)

mrp_BRn_arr = yapp_BRn[:, 0:3]
mrp_error_BRn = np.linalg.norm(np.array([mrp_BRn(mrp_BRn_arr[i], t_BRn[i]) for i in range(len(t_BRn))]), axis=1)

mrp_BRc_arr = yapp_BRc[:, 0:3]
mrp_error_BRc = np.linalg.norm(np.array([mrp_BRc(mrp_BRc_arr[i], t_BRc[i]) for i in range(len(t_BRc))]), axis=1)

fig_error_comp, ax_error_comp = plt.subplots(figsize=(10, 8))
ax_error_comp.plot(t_BRs, mrp_error_BRs, label=f'$R_s$', linewidth=3)
ax_error_comp.plot(t_BRn, mrp_error_BRn, label=f'$R_n$', linewidth=3)
ax_error_comp.plot(t_BRc, mrp_error_BRc, label=f'$R_c$', linewidth=3)

ax_error_comp.set_xlabel('Time [s]', fontsize=14)
ax_error_comp.set_ylabel('MRP Error', fontsize=14)
ax_error_comp.set_title('LMO MRP Error Comparison', fontsize=16)
ax_error_comp.legend(fontsize=12)
ax_error_comp.grid()

plt.show()

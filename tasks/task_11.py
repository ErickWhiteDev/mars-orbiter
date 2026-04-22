from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

from utils.orbit import kep2cart_vector
from utils.projectutils import LMO_mission, GMO_mission, Mars
from utils.outpututils import create_submission_txt

h = 1 # [s]

P = 1 / 6
K = 1 / 180

t_LMO = 6500 # [s]
max_comms_angle = np.deg2rad(35) # [deg]

t_LMO, yapp_LMO, u_LMO, mode_LMO, mrp_error_LMO = LMO_mission.RK4_mission(0, t_LMO, h, GMO_mission, max_comms_angle, P, K)

mrp_LMO = yapp_LMO[:, 6:9]
omega_LMO = yapp_LMO[:, 9:12]

kep_states_LMO = yapp_LMO[:, 0:6]
cart_states_LMO = np.array([kep2cart_vector(kep_state, GMO_mission.planet.mu) for kep_state in kep_states_LMO])
r_LMO = cart_states_LMO[:, 0:3]

kep_states_GMO = yapp_LMO[:, 12:18]
cart_states_GMO = np.array([kep2cart_vector(kep_state, GMO_mission.planet.mu) for kep_state in kep_states_GMO])
r_GMO = cart_states_GMO[:, 0:3]

fill_scale = 1.2

fig_state, ax_state = plt.subplots(3, 1, sharex=True, figsize=(10, 8))

ax_state[0].plot(t_LMO, mrp_LMO, linewidth=3, label=[f'$\\sigma_1$', f'$\\sigma_2$', f'$\\sigma_3$'])
ax_state[0].fill_between(t_LMO, fill_scale * np.min(mrp_LMO), fill_scale * np.max(mrp_LMO), where=mode_LMO == 1, color='yellow', alpha=0.3, label=f'$u_{{R_s}}$')
ax_state[0].fill_between(t_LMO, fill_scale * np.min(mrp_LMO), fill_scale * np.max(mrp_LMO), where=mode_LMO == 2, color='green', alpha=0.3, label=f'$u_{{R_c}}$')
ax_state[0].fill_between(t_LMO, fill_scale * np.min(mrp_LMO), fill_scale * np.max(mrp_LMO), where=mode_LMO == 3, color='red', alpha=0.3, label=f'$u_{{R_n}}$')
ax_state[0].set_ylabel('MRP', fontsize=14)
ax_state[0].legend(fontsize=12, loc='upper right')
ax_state[0].grid()

ax_state[1].plot(t_LMO, omega_LMO, linewidth=3, label=[f'$\\omega_1$', f'$\\omega_2$', f'$\\omega_3$'])
ax_state[1].fill_between(t_LMO, fill_scale * np.min(omega_LMO), fill_scale * np.max(omega_LMO), where=mode_LMO == 1, color='yellow', alpha=0.3, label=f'$u_{{R_s}}$')
ax_state[1].fill_between(t_LMO, fill_scale * np.min(omega_LMO), fill_scale * np.max(omega_LMO), where=mode_LMO == 2, color='green', alpha=0.3, label=f'$u_{{R_c}}$')
ax_state[1].fill_between(t_LMO, fill_scale * np.min(omega_LMO), fill_scale * np.max(omega_LMO), where=mode_LMO == 3, color='red', alpha=0.3, label=f'$u_{{R_n}}$')
ax_state[1].set_ylabel('Angular Velocity [rad / s]', fontsize=14)
ax_state[1].legend(fontsize=12, loc='upper right')
ax_state[1].grid()

ax_state[2].plot(t_LMO, u_LMO, linewidth=3, label=[f'$\\tau_1$', f'$\\tau_2$', f'$\\tau_3$'])
ax_state[2].fill_between(t_LMO, fill_scale * np.min(u_LMO), fill_scale * np.max(u_LMO), where=mode_LMO == 1, color='yellow', alpha=0.3, label=f'$u_{{R_s}}$')
ax_state[2].fill_between(t_LMO, fill_scale * np.min(u_LMO), fill_scale * np.max(u_LMO), where=mode_LMO == 2, color='green', alpha=0.3, label=f'$u_{{R_c}}$')
ax_state[2].fill_between(t_LMO, fill_scale * np.min(u_LMO), fill_scale * np.max(u_LMO), where=mode_LMO == 3, color='red', alpha=0.3, label=f'$u_{{R_n}}$')
ax_state[2].set_xlabel('Time [s]', fontsize=14)
ax_state[2].set_ylabel('Control Torque [N * m]', fontsize=14)
ax_state[2].legend(fontsize=12, loc='upper right')
ax_state[2].grid()

fig_state.suptitle('LMO State and Control Propagation', fontsize=16)
fig_state.tight_layout()

fig_3D = plt.figure(figsize=(10, 8), constrained_layout=True)
ax_3D = fig_3D.add_subplot(111, projection="3d")

u = np.linspace(0, 2 * np.pi, 50)
v = np.linspace(0, np.pi, 50)
x_sphere = Mars.R * np.outer(np.cos(u), np.sin(v))
y_sphere = Mars.R * np.outer(np.sin(u), np.sin(v))
z_sphere = Mars.R * np.outer(np.ones(np.size(u)), np.cos(v))

mode_colors = np.where(mode_LMO == 1, "yellow",
               np.where(mode_LMO == 2, "green",
               np.where(mode_LMO == 3, "red", "yellow")))

norm = np.sqrt(x_sphere**2 + y_sphere**2 + z_sphere**2)
nx = x_sphere / norm
ny = y_sphere / norm
nz = z_sphere / norm

L = np.array([0.0, 1.0, 0.0])

intensity = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0.0, 1.0)

ambient = 0.25
I = ambient + (1.0 - ambient) * intensity

base_rgb = np.array([0x99, 0x3D, 0x00], dtype=float) / 255.0

facecolors = np.zeros(x_sphere.shape + (4,))
facecolors[..., 0] = base_rgb[0] * I
facecolors[..., 1] = base_rgb[1] * I
facecolors[..., 2] = base_rgb[2] * I
facecolors[..., 3] = 1.0

ax_3D.scatter(
    r_LMO[:, 0], r_LMO[:, 1], r_LMO[:, 2],
    c=mode_colors,
    s=8,
    depthshade=False
)

ax_3D.plot(
    r_GMO[:, 0], r_GMO[:, 1], r_GMO[:, 2],
    color="green",
    linewidth=4
)

ax_3D.plot_surface(
    x_sphere, y_sphere, z_sphere,
    facecolors=facecolors,
    shade=False,
    linewidth=0,
    antialiased=True
)

ax_3D.set_xlabel("x [km]", fontsize=14)
ax_3D.set_ylabel("y [km]", fontsize=14)
ax_3D.set_zlabel("")
ax_3D.set_zticks([])
ax_3D.set_zticklabels([])
ax_3D.set_title("LMO 3D Trajectory Colored by Control Mode", fontsize=16, y=0.85)

legend_elements = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor="yellow", markersize=8, label=f"$u_{{R_s}}$"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor="green", markersize=8, label=f"$u_{{R_c}}$"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor="red", markersize=8, label=f"$u_{{R_n}}$"),
]
ax_3D.legend(handles=legend_elements, bbox_to_anchor=(1, 0.5), loc='center left', fontsize=12)
ax_3D.set_aspect("equal")
ax_3D.grid(True)
ax_3D.view_init(elev=90, azim=0)

fig_error, ax_error = plt.subplots(figsize=(10, 8))
ax_error.plot(t_LMO[1:], mrp_error_LMO[1:], linewidth=3, c='tab:blue')
ax_error.fill_between(t_LMO, fill_scale * np.min(mrp_error_LMO), fill_scale * np.max(mrp_error_LMO), where=mode_LMO == 1, color='yellow', alpha=0.3, label=f'$u_{{R_s}}$')
ax_error.fill_between(t_LMO, fill_scale * np.min(mrp_error_LMO), fill_scale * np.max(mrp_error_LMO), where=mode_LMO == 2, color='green', alpha=0.3, label=f'$u_{{R_c}}$')
ax_error.fill_between(t_LMO, fill_scale * np.min(mrp_error_LMO), fill_scale * np.max(mrp_error_LMO), where=mode_LMO == 3, color='red', alpha=0.3, label=f'$u_{{R_n}}$')

ax_error.set_xlabel('Time [s]', fontsize=14)
ax_error.set_ylabel('MRP Error', fontsize=14)
ax_error.set_title('LMO MRP Error Over Time', fontsize=16)
ax_error.grid()

Path("output/task_11").mkdir(parents=True, exist_ok=True)
create_submission_txt("output/task_11/mrp_300.txt", mrp_LMO[np.where(t_LMO == 300)[0][0]])
create_submission_txt("output/task_11/mrp_2100.txt", mrp_LMO[np.where(t_LMO == 2100)[0][0]])
create_submission_txt("output/task_11/mrp_3400.txt", mrp_LMO[np.where(t_LMO == 3400)[0][0]])
create_submission_txt("output/task_11/mrp_4400.txt", mrp_LMO[np.where(t_LMO == 4400)[0][0]])
create_submission_txt("output/task_11/mrp_5600.txt", mrp_LMO[np.where(t_LMO == 5600)[0][0]])

plt.show()

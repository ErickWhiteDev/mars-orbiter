import numpy as np
from scipy.spatial.transform import Rotation as R

class Attitude():
    def __init__(self, type, omega, attitude):
        self.omega = omega

        match type:
            case 'MRP':
                self.rot = R.from_mrp(attitude).inv()

        self.mrp = self.rot.inv().as_mrp()
        self.dcm = self.rot.as_matrix()

    def get_tracking_error(self, RN, N_omega_RN, return_shadow_set=True):
        B_omega_RN = self.rot.apply(N_omega_RN)
        RN_rot = R.from_matrix(RN)

        B_omega_BR = self.omega - B_omega_RN
        BR_rot = self.rot * RN_rot.inv()
        BR_mrp = BR_rot.inv().as_mrp()

        if (np.linalg.norm(BR_mrp) >= 1) and return_shadow_set:
            BR_mrp = get_mrp_shadow_set(BR_mrp)

        return B_omega_BR, BR_mrp

def axes2dcm(ax1, v1, ax2, v2):
    axes = [1, 2, 3]
    used_axes = [ax1, ax2]
    ax3 = [ax for ax in axes if ax not in used_axes][0]

    ax1idx = axes.index(ax1)
    ax2idx = axes.index(ax2)
    ax3idx = axes.index(ax3)

    shift = 2 - ax3idx

    v3 = np.cross(v1, v2) if (ax1idx + shift) % 2 < (ax2idx + shift) % 2 else np.cross(v2, v1)

    dcm = np.empty((3, 3))
    dcm[ax1idx, :] = v1
    dcm[ax2idx, :] = v2
    dcm[ax3idx, :] = v3

    return dcm

def eul2dcm(theta_1, theta_2, theta_3, order, degrees=False):
    chars = ['X', 'Y', 'Z']
    order = ''.join([chars[int(num) - 1] for num in list(order)])
    
    return R.from_euler(order, [theta_1, theta_2, theta_3], degrees=degrees).inv().as_matrix()

def dcm2eul(dcm, order, degrees=False):
    chars = ['X', 'Y', 'Z']
    order = ''.join([chars[int(num) - 1] for num in list(order)])

    return R.from_matrix(dcm).inv().as_euler(order, degrees=degrees)

def quat2dcm(quat):
    return R.from_quat(quat, scalar_first=True).inv().as_matrix()

def dcm2quat(dcm):
    return R.from_matrix(dcm).inv().as_quat(scalar_first=True)

def get_mrp_shadow_set(mrp):
    return -mrp / np.dot(mrp, mrp)

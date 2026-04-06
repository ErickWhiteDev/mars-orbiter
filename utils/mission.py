import numpy as np

from utils.orbit import angles2state
from utils.attitude import eul2dcm, axes2dcm
from utils.mathutils import tilde2vec, matrix_derivative

class Mission():
    def __init__(self, name, planet, orbit, attitude):
        self.name = name
        self.planet = planet
        self.orbit = orbit
        self.attitude = attitude

    def get_HN(self, t):
        n = np.sqrt(self.planet.mu / self.orbit.a ** 3)
        theta = self.orbit.theta + n * t # [rad]

        HN = eul2dcm(self.orbit.Omega, self.orbit.i, theta, '313')

        return HN
    
    def get_RsN(self):
        return axes2dcm(1, np.array([-1, 0, 0]), 3, np.array([0, 1, 0]))
    
    def get_N_omega_RsN(self):
        return np.zeros(3)
    
    def get_RnN(self, t):
        RnH = axes2dcm(1, np.array([-1, 0, 0]), 2, np.array([0, 1, 0]))
        HN = self.get_HN(t)

        return RnH @ HN
    
    def get_N_omega_RnN(self, t):
        n = np.sqrt(self.planet.mu / self.orbit.a ** 3)

        H_omega_RnN = np.array([0, 0, n])

        return self.get_HN(t).T @ H_omega_RnN
    
    def get_RcN(self, t, companion):
        theta_self = self.orbit.find_true_anomaly(t)
        r_self, _ = angles2state(np.linalg.norm(self.orbit.rvec), self.orbit.Omega, self.orbit.i, theta_self, self.planet.mu)

        theta_companion = companion.orbit.find_true_anomaly(t)
        r_companion, _ = angles2state(np.linalg.norm(companion.orbit.rvec), companion.orbit.Omega, companion.orbit.i, theta_companion, companion.planet.mu)

        Delta_r = r_companion - r_self
        r2_dir = np.cross(Delta_r, np.array([0, 0, 1]))
        
        r1 = -Delta_r / np.linalg.norm(Delta_r)
        r2 = r2_dir / np.linalg.norm(r2_dir)

        return axes2dcm(1, r1, 2, r2)
    
    def get_N_omega_RcN(self, t, companion, derivative_order=8):
        RcN = self.get_RcN(t, companion)

        dRcNdt = matrix_derivative(self.get_RcN, t, (3, 3), args=(companion), order=derivative_order)

        Rc_omega_RcN_tilde = -dRcNdt @ RcN.T
        Rc_omega_RcN = tilde2vec(Rc_omega_RcN_tilde)

        return RcN.T @ Rc_omega_RcN
        

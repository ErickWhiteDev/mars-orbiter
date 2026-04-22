import numpy as np

from utils.orbit import angles2state
from utils.attitude import eul2dcm, axes2dcm, get_short_mrp, mrp2dcm, dcm2mrp, eom
from utils.mathutils import vec2tilde, tilde2vec, matrix_derivative, RK4_step

class Mission():
    def __init__(self, name, planet, orbit, attitude, spacecraft=None):
        self.name = name
        self.planet = planet
        self.orbit = orbit
        self.attitude = attitude
        self.spacecraft = spacecraft

    def get_HN(self, t):
        n = np.sqrt(self.planet.mu / self.orbit.a ** 3)
        theta = self.orbit.theta + n * t # [rad]

        HN = eul2dcm(self.orbit.Omega, self.orbit.i, theta, '313')

        return HN
    
    def get_RsN(self):
        return axes2dcm(1, np.array([-1, 0, 0]), 3, np.array([0, 1, 0]))
    
    def get_BRs(self):
        return self.attitude.dcm @ self.get_RsN().T
    
    def get_N_omega_RsN(self):
        return np.zeros(3)
    
    def get_B_omega_BRs(self):
        return self.attitude.omega - self.attitude.dcm @ self.get_N_omega_RsN()
    
    def u_Rs(self, _, P, K, **__):
        mrp = dcm2mrp(self.get_BRs())
        omega = self.get_B_omega_BRs()
        return -K * mrp - P * omega
    
    def get_RnN(self, t):
        RnH = axes2dcm(1, np.array([-1, 0, 0]), 2, np.array([0, 1, 0]))
        HN = self.get_HN(t)

        return RnH @ HN
    
    def get_BRn(self, t):
        return self.attitude.dcm @ self.get_RnN(t).T
    
    def get_N_omega_RnN(self, t):
        n = np.sqrt(self.planet.mu / self.orbit.a ** 3)

        H_omega_RnN = np.array([0, 0, n])

        return self.get_HN(t).T @ H_omega_RnN
    
    def get_B_omega_BRn(self, t):
        return self.attitude.omega - self.attitude.dcm @ self.get_N_omega_RnN(t)
    
    def u_Rn(self, t, P, K, **__):
        mrp = dcm2mrp(self.get_BRn(t))
        omega = self.get_B_omega_BRn(t)
        return -K * mrp - P * omega
    
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
    
    def get_BRc(self, t, companion):
        return self.attitude.dcm @ self.get_RcN(t, companion).T
    
    def get_N_omega_RcN(self, t, companion, derivative_order=8):
        RcN = self.get_RcN(t, companion)

        dRcNdt = matrix_derivative(self.get_RcN, t, (3, 3), args=(companion), order=derivative_order)

        Rc_omega_RcN_tilde = -dRcNdt @ RcN.T
        Rc_omega_RcN = tilde2vec(Rc_omega_RcN_tilde)

        return RcN.T @ Rc_omega_RcN
    
    def get_B_omega_BRc(self, t, companion):
        return self.attitude.omega - self.attitude.dcm @ self.get_N_omega_RcN(t, companion)

    def u_Rc(self, t, P, K, **kwargs):
        mrp = dcm2mrp(self.get_BRc(t, kwargs['companion']))
        omega = self.get_B_omega_BRc(t, kwargs['companion'])
        return -K * mrp - P * omega
        
    def RK4_mission(self, a, b, h, companion, max_comms_angle, P, K, **kwargs):
        kwargs['type'] = 'MRP'
        kwargs['mission'] = self
        kwargs['companion'] = companion

        X0 = np.hstack((self.orbit.get_kep_state_vector(), self.attitude.mrp, self.attitude.omega, companion.orbit.get_kep_state_vector()))
        u0 = np.zeros(3)
        N = int((b - a) / h)

        X = np.zeros((N + 1, X0.size))
        t = np.zeros(N + 1)
        u = np.zeros((N + 1, u0.size))
        mrp_error = np.zeros((N + 1, 3))
        mode = np.zeros(N + 1)

        X[0, :] = X0
        t[0] = a
        u[0, :] = u0
        mode[0] = 0

        for j in range(1, N + 1):
            cart_state = self.orbit.get_cart_state_vector()
            
            if cart_state[1] > 0:
                control_law = self.u_Rs
                mrp_error[j] = np.linalg.norm(dcm2mrp(self.get_BRs()))
                mode[j] = 1
            else:
                rvec = cart_state[0:3]
                companion_cart_state = companion.orbit.get_cart_state_vector()
                companion_rvec = companion_cart_state[0:3]
                comms_angle = np.arccos(np.dot(rvec, companion_rvec) / (np.linalg.norm(rvec) * np.linalg.norm(companion_rvec)))
                if comms_angle < max_comms_angle:
                    control_law = self.u_Rc
                    mrp_error[j] = np.linalg.norm(dcm2mrp(self.get_BRc(0, companion)))
                    mode[j] = 2
                else:
                    control_law = self.u_Rn
                    mrp_error[j] = np.linalg.norm(dcm2mrp(self.get_BRn(0)))

                    mode[j] = 3

            uj = control_law(0, P, K, **kwargs)
            u[j] = uj
            kwargs['u'] = uj

            tj, yapp_j = RK4_step(t[j - 1], h, X[j - 1, :], eom, **kwargs)
            t[j] = tj

            X[j, 0:6] = yapp_j[0:6]
            X[j, 6:9] = get_short_mrp(yapp_j[6:9])
            X[j, 9:18] = yapp_j[9:18]

            self.orbit.update_from_kep_state(X[j, 0:6])
            self.attitude.update_state('MRP', X[j, 6:12])
            companion.orbit.update_from_kep_state(X[j, 12:18])

        return t, X, u, mode, mrp_error

def eom(t, X, mission, companion, u, type):
    orbit_state = X[0:6]
    attitude = X[6:9]
    omega = X[9:12]
    companion_orbit_state = X[12:18]

    orbit_state_dot = np.zeros(6)
    orbit_state_dot[5] = np.sqrt(mission.planet.mu / orbit_state[0] ** 3) # Only valid for circular orbits

    companion_orbit_state_dot = np.zeros(6)
    companion_orbit_state_dot[5] = np.sqrt(companion.planet.mu / companion_orbit_state[0] ** 3) # Only valid for circular orbits

    if type == 'MRP':
        mrp = attitude
        mrp_dot = 0.25 * ((1 - np.dot(mrp, mrp)) * np.eye(3) + 2 * vec2tilde(mrp) + 2 * np.outer(mrp, mrp)) @ omega

    omega_dot = np.linalg.inv(mission.spacecraft.I) @ (u - np.cross(omega, mission.spacecraft.I @ omega))

    return np.hstack((orbit_state_dot, mrp_dot, omega_dot, companion_orbit_state_dot))

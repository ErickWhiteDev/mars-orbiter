import numpy as np
from scipy.optimize import fsolve

from utils.attitude import eul2dcm

class Orbit:
    def __init__(self, planet, type, state):
        self.planet = planet
        if type == 'kep':
            self.a = state.get('a')
            self.e = state.get('e')
            self.i = state.get('i')
            self.Omega = state.get('Omega')
            self.omega = state.get('omega')
            self.theta = state.get('theta')

            cart_state = kep2cart(self.get_kep_state(), self.planet.mu)
            self.rvec = np.array([cart_state.get('x'), cart_state.get('y'), cart_state.get('z')])
            self.vvec = np.array([cart_state.get('vx'), cart_state.get('vy'), cart_state.get('vz')])
        elif type == 'cart':
            self.rvec = np.array([state.get('x'), state.get('y'), state.get('z')])
            self.vvec = np.array([state.get('vx'), state.get('vy'), state.get('vz')])

            kep_state = cart2kep(self.get_cart_state(), self.planet.mu)
            self.a = kep_state.get('a')
            self.e = kep_state.get('e')
            self.i = kep_state.get('i')
            self.Omega = kep_state.get('Omega')
            self.omega = kep_state.get('omega')
            self.theta = kep_state.get('theta')

    def get_kep_state(self):
        return {
            'a': self.a,
            'e': self.e,
            'i': self.i,
            'Omega': self.Omega,
            'omega': self.omega,
            'theta': self.theta
        }

    def get_cart_state(self):
        return {
            'x': self.rvec[0],
            'y': self.rvec[1],
            'z': self.rvec[2],
            'vx': self.vvec[0],
            'vy': self.vvec[1],
            'vz': self.vvec[2]
        }
    
    def find_true_anomaly(self, t, eps=1E-5):
        e = self.e
        a = self.a
        theta_0 = self.theta      
        mu = self.planet.mu

        if np.abs(1 - e) < eps:
            cart_state = kep2cart(self)
            rvec = np.array([cart_state['x'], cart_state['y'], cart_state['z']])
            vvec = np.array([cart_state['vx'], cart_state['vy'], cart_state['vz']])

            hvec = np.cross(rvec, vvec)
            h = np.linalg.norm(hvec)

            p = h ** 2 / mu

            tp = -0.5 * np.sqrt(p ** 3 / mu) * np.tan(theta_0 / 2) * (1 + np.tan(theta_0 / 2) ** 2 / 3)

            M = mu ** 2 / h ** 3 * (t - tp)
            theta = np.mod(2 * np.atan2(np.pow((3 * M + np.sqrt((3 * M) ** 2 + 1)), 1 / 3) - np.pow((3 * M + np.sqrt((3 * M) ** 2 + 1)), -1 / 3), 1), 2 * np.pi)
        elif e < 1:
            E0 = np.mod(2 * np.atan2(np.sqrt((1 - e) / (1 + e)) * np.tan(theta_0 / 2), 1), 2 * np.pi)
            tp = -np.sqrt(a ** 3 / mu) * (E0 - e * np.sin(E0))

            M = np.sqrt(mu / a ** 3) * (t - tp)
            kepler = lambda E: E - e * np.sin(E) - M

            E = fsolve(kepler, M)

            theta = np.mod(2 * np.atan2(np.sqrt((1 + e) / (1 - e)) * np.tan(E / 2), 1), 2 * np.pi)
        else:
            F0 = np.mod(2 * np.atanh(np.sqrt((e - 1) / (e + 1)) * np.tan(theta_0 / 2)), 2 * np.pi)
            tp = -np.sqrt(np.abs(a) ** 3 / mu) * (F0 - e * np.sinh(F0))

            M = np.sqrt(mu / np.abs(a) ** 3) * (t - tp)
            kepler = lambda H: e * np.sinh(H) - H - M

            H = fsolve(kepler, M)

            theta = np.mod(2 * np.atan2(np.sqrt((e + 1) / (e - 1)) * np.tanh(H / 2), 1), 2 * np.pi)

        return theta[0]

def cart2kep(state, mu, eps=1E-5):
    rvec = np.array([state[0], state[1], state[2]])
    r = np.linalg.norm(rvec)
    vvec = np.array([state[3], state[4], state[5]])

    zhat = np.array([0, 0, 1])

    hvec = np.cross(rvec, vvec)
    h = np.linalg.norm(hvec)
    hhat = hvec / h

    if abs(h) < eps:
        raise ValueError("Cannot calculate orbital elements for rectilinear trajectory")
    
    evec = 1 / mu * np.cross(vvec, hvec) - rvec / r
    e = np.linalg.norm(evec)

    p = h ** 2 / mu
    a = np.inf if np.abs(1 - e) < eps else p / (1 - e ** 2)

    i = np.acos(hhat[2])

    nvec = np.cross(zhat, hvec)
    n = np.linalg.norm(nvec)

    if (np.abs(e) < eps) and ((np.abs(i) < eps) or (np.abs(np.pi - i) < eps)):
        Omega = 0
        omega = 0
        theta = np.acos(rvec[0] / r) if rvec[1] >= 0 else 2 * np.pi - np.acos(rvec[0] / r)
    elif np.abs(e) < eps:
        nhat = nvec / n
        nhat_perp = np.cross(hhat, nhat)

        Omega = np.atan2(nhat[1], nhat[0])
        omega = 0
        theta = np.acos(np.dot(evec, rvec) / (e * r)) if np.dot(rvec, vvec) >= 0 else 2 * np.pi - np.acos(np.dot(nvec, rvec) / (n * r))
    elif (np.abs(i) < eps) or (np.abs(np.pi - i) < eps):
        ehat = evec / e
        ehat_perp = np.cross(hhat, ehat)
        
        Omega = 0
        omega = np.acos(evec[0] / e) if evec[1] >= 0 else 2 * np.pi - np.acos(evec[0] / e)
        theta = np.atan2(np.dot(rvec, ehat_perp), np.dot(rvec, ehat))
    else:
        nhat = nvec / n
        nhat_perp = np.cross(hhat, nhat)

        ehat = evec / e
        ehat_perp = np.cross(hhat, ehat)

        Omega = np.atan2(nhat[1], nhat[0])
        omega = np.atan2(np.dot(evec, nhat_perp), np.dot(evec, nhat))
        theta = np.atan2(np.dot(rvec, ehat_perp), np.dot(rvec, ehat))

    return {
        'a': a,
        'e': e,
        'i': i,
        'Omega': Omega,
        'omega': omega,
        'theta': theta,
    }

def kep2cart(state, mu):
    a = state['a']
    e = state['e']
    i = state['i']
    Omega = state['Omega']
    omega = state['omega']
    theta = state['theta']

    p = a * (1 - e ** 2)
    r = p / (1 + e * np.cos(theta))

    node_vec = np.array([np.cos(Omega), np.sin(Omega), 0])
    node_vec_perp = np.array([-np.cos(i) * np.sin(Omega), np.cos(i) * np.cos(Omega), np.sin(i)])

    ehat = np.cos(omega) * node_vec + np.sin(omega) * node_vec_perp
    ehat_perp = -np.sin(omega) * node_vec + np.cos(omega) * node_vec_perp

    rhat = np.cos(theta) * ehat + np.sin(theta) * ehat_perp
    rhat_perp = -np.sin(theta) * ehat + np.cos(theta) * ehat_perp
    rvec = r * rhat

    sin_gamma = e * np.sin(theta) / np.sqrt(1 + 2 * e * np.cos(theta) + e ** 2)
    cos_gamma = (1 + e * np.cos(theta)) / np.sqrt(1 + 2 * e * np.cos(theta) + e ** 2)

    v = np.sqrt(mu / p  * (1 + 2 * e * np.cos(theta) + e ** 2))
    vvec = v * (sin_gamma * rhat + cos_gamma * rhat_perp)

    return {
        'x': rvec[0],
        'y': rvec[1],
        'z': rvec[2],
        'vx': vvec[0],
        'vy': vvec[1],
        'vz': vvec[2]
        }

def angles2state(r, Omega, i, theta, mu):
    v = np.sqrt(mu / r) # [km / s]

    rvec_O = np.array([r, 0, 0])
    vvec_O = np.array([0, v, 0])

    ON = eul2dcm(Omega, i, theta, '313')

    rvec_I = ON.T @ rvec_O
    vvec_I = ON.T @ vvec_O

    return rvec_I, vvec_I

import numpy as np

from utils.planet import Planet
from utils.orbit import Orbit
from utils.attitude import Attitude
from utils.spacecraft import Spacecraft
from utils.mission import Mission

Mars = Planet('Mars', 3396.19, 42828.3)

LMO_orbit = Orbit(Mars, 'kep', {'a': 3796.19, 'e': 0, 'i': np.deg2rad(30), 'Omega': np.deg2rad(20), 'omega': 0, 'theta': np.deg2rad(60)})
LMO_attitude = Attitude('MRP', np.deg2rad(np.array([1, 1.75, -2.2])), np.array([0.3, -0.4, 0.5]))
LMO_spacecraft = Spacecraft('LMO', np.diag([10, 5, 7.5]))
LMO_mission = Mission('LMO', Mars, LMO_orbit, LMO_attitude, LMO_spacecraft)

GMO_orbit = Orbit(Mars, 'kep', {'a': 20424.2, 'e': 0, 'i': 0, 'Omega': 0, 'omega': 0, 'theta': np.deg2rad(250)})
GMO_attitude = Attitude('MRP', np.deg2rad(np.array([1, 1.75, -2.2])), np.array([0.3, -0.4, 0.5])) # Filler value to instantiate Mission class
GMO_mission = Mission('GMO', Mars, GMO_orbit, GMO_attitude)

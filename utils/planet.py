class Planet:
    def __init__(self, name, R, mu):
        self.name = name
        self.R = R
        self.mu = mu

    def get_planet_data(self):        
        return {
            'name': self.name,
            'R': self.R, # [km]
            'mu': self.mu # [km^3 / s^2]
        }

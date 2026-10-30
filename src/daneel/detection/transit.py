import importlib
import numpy as np
import matplotlib.pyplot as plt

batman = importlib.import_module("batman")

# Old code that previously worked, has been superseded but may be helpful in the future
if False:
    # Create dictionary of planetary parameters, from NEA
    paramsdic = {
        "pl_name": "K2-18b",
        "t0": 0.,
        "per": 32.9,
        "rp_e": 2.37,
        "rp": 0.05, # 0.05 times st_rad
        "a_au": 0.1429,
        "a": 75,   # 75 times st_rad
        "inc": 90.,     # take to be 90, not listed in NEA default entry
        "ecc": 0.2,
        "w": 0.,    # take to be 0, -5 deg in NEA
        "limb_dark": "quadratic",
        "u": [0.244, 0.286],
        "st_rad": 0.411     # host star radius, in solar radii
    }


# Function to convert pl_rad to function of planetary radius
def radius_convert(pl_rade, st_rad, rade_per_radsol=109):  # Default conversion factor 109 Earth rad per Solar rad
    return (pl_rade / rade_per_radsol) / st_rad

# Similar function to convert pl_a to units of host star radius
def semimajor_convert(pl_a, st_rad, radsol_per_au=215.032):  # Default conversion factor 215 Solar rad per 1 AU
    return (pl_a * radsol_per_au) / st_rad


class Transit:
    """
    Transit model class

    Code greatly inspired by that of Tiziano Zingales
    """

    def __init__(self, paramsdic):
        """
        Initializes transit model with the given parameters, ideally from a YAML file
        
        :param:
        paramsdic: dict
            Dictionary containing transit parameters loaded from YAML file
        """
        self.params = batman.TransitParams()
        self.params.pl_name = paramsdic.get("pl_name", "Planet")
        self.params.t0 = paramsdic.get('t0', 0.0)
        self.params.per = paramsdic.get('per')
        self.params.rp = paramsdic.get('rp', 0)
        self.params.a = paramsdic.get('a', 0)
        self.params.inc = paramsdic.get('inc')
        self.params.ecc = paramsdic.get('ecc', 0.0)
        self.params.w = paramsdic.get('w', 90.0)
        self.params.u = paramsdic.get('u', [0.1, 0.3])
        self.params.limb_dark = paramsdic.get('limb_dark', 'quadratic')
        self.params.rp_e = paramsdic.get('rp_e', 0)
        self.params.a_au = paramsdic.get('a_au', 0)
        self.params.st_rad = paramsdic.get('st_rad', 0)

        # Convert radius and a to proper units for batman, if rp and a not given
        if self.params.rp == 0 and self.params.st_rad != 0 and self.params.rp_e != 0:
            self.params.rp = radius_convert(self.params.rp_e, self.params.st_rad)
        if self.params.a == 0 and self.params.st_rad != 0 and self.params.a_au != 0:
            self.params.a = semimajor_convert(self.params.a_au, self.params.st_rad)

        self.t = np.linspace(-0.1, 0.1, 1000)  # times at which to calculate light curve
        self.model = batman.TransitModel(self.params, self.t)  # initializes model

    def compute_light_curve(self):
        """
        Function to compute light curve from transit model
        :returns:
        flux: ndarray
            relative flux values
        """
        self.flux = self.model.light_curve(self.params)
        return self.flux

    def plot_light_curve(self, output_file='lightcurve.png', show=False):
        """
        Function to plot computed light curve from transit model
        :param:
        output_file: str, optional
            Name of file to save plot to
        """
        if not hasattr(self, 'flux'):
            self.compute_light_curve()

        plt.plot(self.t, self.flux)
        plt.title(str(self.params.pl_name) + ' Model Light Curve')
        plt.xlabel('Time from central transit (days)')
        plt.ylabel('Relative flux')
        plt.savefig(output_file, dpi=150)
        if show:
            plt.show()
        plt.close()
        print(f"Light curve saved to {output_file}")
        print(self.params.rp)

    def run(self, output_file='light_curve.png'):
        """
        Function to run everything—compute the light curve from transit model and plot it
        :param:
        output_file: str, optional
            Name of file to save plot to
        """
        self.compute_light_curve()
        self.plot_light_curve(output_file)

# More redundant code that may be helpful for future work and testing
if False:
    params = batman.TransitParams()
    for key, value in paramsdic.items():     # Assigns attributes from dictionary entries
        setattr(params, key, value)

    t = np.linspace(-0.1, 0.1, 1000)  #times at which to calculate light curve
    m = batman.TransitModel(params, t)    #initializes model
    flux = m.light_curve(params)

    plt.plot(t, flux)
    plt.title(paramsdic["pl_name"] + ' Transit Model')
    plt.xlabel('Time (d)')      # Pretty sure the units are days
    plt.ylabel('Normalized Flux')
    plt.savefig(paramsdic["pl_name"] + '_assignment1_taskF.png')
    plt.show()

import batman
import numpy as np
import matplotlib.pyplot as plt

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
def radius_convert(pl_rade, st_rad, rade_per_radsol = 109): #Can change conversion factor
    return (pl_rade / rade_per_radsol) / st_rad

# Similar function to convert pl_a to units of host star radius
def semimajor_convert(pl_a, st_rad, radsol_per_au = 215.032):
    return (pl_a * radsol_per_au) / st_rad

# Convert radius and a to proper units for batman, if rp and a not given
if paramsdic["rp"] == 0:
    paramsdic["rp"] = radius_convert(paramsdic["rp_e"], paramsdic["st_rad"])
if paramsdic["a"] == 0:
    paramsdic["a"] = semimajor_convert(paramsdic["a_au"], paramsdic["st_rad"])

params = batman.TransitParams()    #Create params object

# Less pretty way to setting object attributes
# params.t0 = 0.                       #time of inferior conjunction (set to 0)
# params.per = 32.9                       #orbital period (I think in days)
# params.rp = 0.05                       #planet radius (in units of stellar radii)
# #Star is 0.411 Rs, Planet is 0.211 Rj, 1 Rs ~= 6.957e8/6.9886e7 ~ 9.95 Rj
# # (0.211 / 9.95) / 0.411    Need to double-check
# params.a = 75.                        #semi-major axis (in units of stellar radii)
# #Star is 0.411 Rs = , Planet at 0.1429 AU, 1 Rs = 4.65047e-3 AU
# # 0.1429 / 4.65047e-3 / 0.411   Need to double-check
# params.inc = 90.                      #orbital inclination (in degrees)
# params.ecc = 0.                       #eccentricity
# params.w = 90.                        #longitude of periastron (in degrees)
# params.limb_dark = "nonlinear"        #limb darkening model
# params.u = [0.5, 0.1, 0.1, -0.1]      #limb darkening coefficients [u1, u2, u3, u4]

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

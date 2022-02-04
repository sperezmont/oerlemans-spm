# general simulation settings
bed_type = 'linear'	# bed profile type
hx_model = 'plastic'   # ice sheet profile 
geo_model = 'oerlemans2003'  # bed slope effect in ice profile 
Acc_model = 'linear'        # type of accumulation 
zE_variation ='sin'     # type of variation in zE: 'constant', 'linear', 'sin', 'list'
sea_level = 'sin' # sea-level parameterization: 'constant', 'linear', 'sin', 'list'

domain = 2000   # [km] horizontal domain
zdomain = 6000  # [m]   vertical domain
dx = 10         # [km] horizontal resolution
dz = 100        # [m] vertical resolution
dt = 1000		# [yrs] time resolution

T = 44000		# [yrs] length of the simulation

# initial conditions
zE0 = 415 		# [m]  initial equilibrium height 
R0 = 1		# [km] initial radium

s = 0.001		# bed slope
d0 = 250		# central bed elevation [m]

# geometry parameters
mu0 = 8			# profile parameter [m**1/2]
c = 2e6			# [m**1/2]

# thermodynamics
A0 = 1			# mass balance above the runoff line value (constant)  [m ice/yr]
beta = 0.005		# mass balance gradient with respect to altitude [1/yr]
CR = 500        # [km] distance where A = 1/e A

zEA = 415   # amplitude of variation in zE [m]
zEP = 22000   # forcing period [yr]

# sea-level
eta0 = 0			# eustatic sea-level [m]
etaA = 50           # sea-level forcing amplitude [m]
etaP = 22000        # sea-level forcing period [yr]

# grounding line
f = 1			# yr-1

# properties	
rhoi = 917		# ice density [kg/m3]
rhow = 1000		# water density [kg/m3]
rhob = 2700		# bed density [kg/m3]

A_oc = 3.618*10**8 # ocean area [km2]



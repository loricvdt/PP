if __name__ == "__main__":
	print("main.py should be started instead")
	exit()

# Calculation range (nm)
x_min = -4
x_max = 6

# Potential
default_V_0 = 0  # (eV)
V_0 = default_V_0
default_V_barrier = 1
V_barrier = default_V_barrier
default_barrier_start = 0  # (nm)
barrier_start = default_barrier_start
default_barrier_end = 2
barrier_end = default_barrier_end

potential = [[], []]  # Potential plot data

# Energy
E = 1
E_min = -1
E_max = 3


def calculate_potential():
	""" Calculates the value of the potential """
	global potential
	potential[0] = [x_min, barrier_start, barrier_start, barrier_end, barrier_end, x_max]
	potential[1] = [V_0, V_0, V_barrier, V_barrier, V_0, V_0]
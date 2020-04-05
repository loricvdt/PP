if __name__ == "__main__":
	print("main.py should be started instead")
	exit()

import numpy as np

# Calculation range (nm)
x_min = -4
x_max = 6

# Potential
default_V_0 = 0  # (eV)
V_0 = default_V_0
default_V_barrier = 1
V_barrier = default_V_barrier
default_V_1 = 0
V_1 = default_V_1
default_barrier_start = 0  # (nm)
barrier_start = default_barrier_start
default_barrier_end = 2
barrier_end = default_barrier_end

potential = [[], []]  # Potential plot data

# Energy
default_E = 1
E = default_E
E_min = -1
E_max = 3

energy = [[x_min, x_max], []]  # Potential plot data

# Wave number
k_0 = 6

# Constants
k_s = 0
k_b = 0
k_e = 0
A = 0
B = 0
R = 0
T = 0

# Wave function
psi_min = -1
psi_max = 3
psi = [[], []]


def calculate_potential():
	""" Calculates the value of the potential """
	global potential
	potential[0] = [x_min, barrier_start, barrier_start, barrier_end, barrier_end, x_max]
	potential[1] = [V_0, V_0, V_barrier, V_barrier, V_1, V_1]


def calculate_energy():
	""" Calculates the value of the potential """
	global energy
	energy[1] = [E, E]


def calculate_wave_function():
	""" Calculates the wave function """
	global psi
	calculate_constants()

	psi[0] = np.linspace(x_min, x_max, 500)
	psi[1] = []

	for x in psi[0]:
		psi[1].append(np.abs(wave_function_value(x)))


def calculate_k(v):
	""" Returns the value of k or K according to the potential """
	if E - v >= 0:  # Returns k
		return np.sqrt((E - v) / E) * k_0
	else:  # E - v < 0  # Returns K
		return np.sqrt((v - E) / E) * k_0


def calculate_constants():
	""" Calculate needed constants for the wave function """
	global k_s, k_b, k_e, A, B, R, T
	k_s = calculate_k(V_0)
	k_b = calculate_k(V_barrier)
	k_e = calculate_k(V_1)
	x_s = barrier_start
	x_e = barrier_end

	if E - V_barrier >= 0 and E - V_1 >= 0:  # Case 1
		A = 1 / (np.exp(2 * 1j * k_b * x_e) + (1 + k_b / k_s) / (1 - k_b / k_s) * np.exp(2 * 1j * k_b * x_s)) * (2 * np.exp(1j * k_s * k_b * x_s)) / (1 - k_b / k_s)
		B = A * np.exp(2 * 1j * k_b * x_e)
		R = np.exp(1j * k_s * x_s) * (A * np.exp(1j * k_b * x_s) + B * np.exp(-1j * k_b * x_s) - np.exp(1j * k_s * x_s))
		T = np.exp(-1j * k_e * x_e) * (A * np.exp(1j * k_b * x_e) + B * np.exp(-1j * k_b * x_e))
		print("T = ", abs(T))


def wave_function_value(x):
	""" Returns value of the wave function at a x value """
	if E - V_0 < 0:
		return 0
	else:  # E-V_0 >= 0
		if x < barrier_start:
			return np.exp(1j * k_s * x) + R * np.exp(-1j * k_s * x)
		elif barrier_start <= x <= barrier_end:
			if E - V_barrier >= 0:
				return A * np.exp(1j * k_b * x) + B * np.exp(-1j * k_b * x)
			else:  # E-V_barrier <0
				return 0
		else:  # x > barrier_end
			if E - V_1 >= 0:
				return T * np.exp(1j * k_e * x)
			else:  # E-V_barrier <0
				return 0

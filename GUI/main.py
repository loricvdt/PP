import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
import scipy.constants as cst

# For mouse precision
relative_epsilon = 0.05
in_range = ""

# Calculation range (nm)
x_min = -4
x_max = 6
epsilon_x = (x_max - x_min) * relative_epsilon

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


def calculate_potential():
	global potential
	potential[0] = [x_min, barrier_start, barrier_start, barrier_end, barrier_end, x_max]
	potential[1] = [V_0, V_0, V_barrier, V_barrier, V_0, V_0]


# Energy
E = 1
E_min = -1
E_max = 3
epsilon_E = (E_max - E_min) * relative_epsilon

# Create window
window = tk.Tk()
window.title("PP GUI")
window.iconbitmap("")
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", exit)

# Create figure
figure = plt.Figure()

# Add figure to window
canvas = FigureCanvasTkAgg(figure, window)
canvas.get_tk_widget().pack(side=tk.LEFT)

# Create plot
ax = figure.add_subplot(111)
ax.set_xlim(x_min, x_max)
ax.set_ylim(E_min, E_max)
calculate_potential()
potential_plt, = ax.plot(potential[0], potential[1])
figure.tight_layout()


def update_textbox(textbox, value):
	textbox.delete(0, tk.END)
	textbox.insert(0, value)


def update_v_0(value):
	global V_0
	V_0 = float(value)
	V_0_slider.set(V_0)
	update_textbox(V_0_textbox, round(V_0, 3))
	update_potential()


def update_v_barrier(value):
	global V_barrier
	V_barrier = float(value)
	V_barrier_slider.set(V_barrier)
	update_textbox(V_barrier_textbox, round(V_barrier, 3))
	update_potential()


def update_barrier_start(value):
	global barrier_start
	if float(value) < barrier_end - epsilon_x:
		barrier_start = float(value)
	else:
		barrier_start = barrier_end - epsilon_x
	barrier_start_slider.set(barrier_start)
	update_textbox(barrier_start_textbox, round(barrier_start, 3))
	update_potential()


def update_barrier_end(value):
	global barrier_end
	if float(value) > barrier_start + epsilon_x:
		barrier_end = float(value)
	else:
		barrier_end = barrier_start + epsilon_x
	barrier_end_slider.set(barrier_end)
	update_textbox(barrier_end_textbox, round(barrier_end, 3))
	update_potential()


def update_potential():
	calculate_potential()
	potential_plt.set_data(potential[0], potential[1])
	plt.draw()
	canvas.draw()


def reset_values(event):
	update_v_0(default_V_0)
	update_v_barrier(default_V_barrier)
	update_barrier_start(default_barrier_start)
	update_barrier_end(default_barrier_end)


def button_press_callback(event):
	global in_range
	if event.inaxes:
		if (
				x_min <= event.xdata <= barrier_start or barrier_end <= event.xdata <= x_max) and V_0 - epsilon_E <= event.ydata <= V_0 + epsilon_E:
			in_range = "V_0"
		elif barrier_start <= event.xdata <= barrier_end and V_barrier - epsilon_E <= event.ydata <= V_barrier + epsilon_E:
			in_range = "V_barrier"
		elif barrier_start - epsilon_x <= event.xdata <= barrier_start + epsilon_x and V_0 <= event.ydata <= V_barrier:
			in_range = "barrier_start"
		elif barrier_end - epsilon_x <= event.xdata <= barrier_end + epsilon_x and V_0 <= event.ydata <= V_barrier:
			in_range = "barrier_end"
		else:
			in_range = ""

	else:
		in_range = ""


def button_release_callback(event):
	global in_range
	in_range = ""


def motion_notify_callback(event):
	if event.button and event.inaxes:
		if in_range == "V_0":
			update_v_0(event.ydata)
		elif in_range == "V_barrier":
			update_v_barrier(event.ydata)
		elif in_range == "barrier_start":
			update_barrier_start(event.xdata)
		elif in_range == "barrier_end":
			update_barrier_end(event.xdata)


def update_v_0_from_tb(event):
	update_v_0(good_value(V_0_textbox.get(), V_0))


def update_v_barrier_from_tb(event):
	update_v_barrier(good_value(V_barrier_textbox.get(), V_barrier))


def update_barrier_start_from_tb(event):
	update_barrier_start(good_value(barrier_start_textbox.get(), barrier_start))


def update_barrier_end_from_tb(event):
	update_barrier_end(good_value(barrier_end_textbox.get(), barrier_end))


def good_value(value, old_value):
	try:
		float(value)
		return float(value)
	except ValueError:
		return old_value


# Connecting figure interaction with methods
figure.canvas.mpl_connect('button_press_event', button_press_callback)
figure.canvas.mpl_connect('button_release_event', button_release_callback)
figure.canvas.mpl_connect('motion_notify_event', motion_notify_callback)

# Creating sliders
left_frame = tk.Frame()
V_0_slider = tk.Scale(left_frame, from_=E_min, to=E_max, resolution=0.01, orient=tk.HORIZONTAL, length=200,
					 			label="Initial potential (eV)", showvalue=0, command=update_v_0)
V_barrier_slider = tk.Scale(left_frame, from_=E_min, to=E_max, resolution=0.01, orient=tk.HORIZONTAL, length=200,
								label="Barrier potential (eV)", showvalue=0, command=update_v_barrier)
barrier_start_slider = tk.Scale(left_frame, from_=x_min, to=x_max, resolution=0.01, orient=tk.HORIZONTAL, length=200,
								label="Barrier start (nm)", showvalue=0, command=update_barrier_start)
barrier_end_slider = tk.Scale(left_frame, from_=x_min, to=x_max, resolution=0.01, orient=tk.HORIZONTAL, length=200,
							  label="Barrier end (nm)", showvalue=0, command=update_barrier_end)
V_0_slider.set(V_0)
V_barrier_slider.set(V_barrier)
barrier_start_slider.set(barrier_start)
barrier_end_slider.set(barrier_end)

# Creating text boxes
V_0_textbox = tk.Entry(left_frame, width=10)
V_barrier_textbox = tk.Entry(left_frame, width=10)
barrier_start_textbox = tk.Entry(left_frame, width=10)
barrier_end_textbox = tk.Entry(left_frame, width=10)
update_textbox(V_0_textbox, V_0)
update_textbox(V_barrier_textbox, V_barrier)
update_textbox(barrier_start_textbox, barrier_start)
update_textbox(barrier_end_textbox, barrier_end)
V_0_textbox.bind("<Return>", update_v_0_from_tb)
V_barrier_textbox.bind("<Return>", update_v_barrier_from_tb)
barrier_start_textbox.bind("<Return>", update_barrier_start_from_tb)
barrier_end_textbox.bind("<Return>", update_barrier_end_from_tb)

# Creating reset button
reset_button = tk.Button(left_frame, text="Reset")
reset_button.bind("<Button-1>", reset_values)

# Adding all to view
left_frame.pack(side=tk.RIGHT, padx=10, anchor=tk.N)
V_0_slider.grid(row=0, column=0)
V_0_textbox.grid(row=0, column=1, sticky=tk.S)
V_barrier_slider.grid(row=1, column=0)
V_barrier_textbox.grid(row=1, column=1, sticky=tk.S)
barrier_start_slider.grid(row=2, column=0)
barrier_start_textbox.grid(row=2, column=1, sticky=tk.S)
barrier_end_slider.grid(row=3, column=0)
barrier_end_textbox.grid(row=3, column=1, sticky=tk.S)
reset_button.grid(row=4, column=1, sticky=tk.NSEW)

window.mainloop()

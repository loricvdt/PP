if __name__ == "__main__":
	print("main.py should be started instead")
	exit()


import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import maths
import controller

# Create window
window = tk.Tk()
window.title("PP GUI")
window.iconbitmap("")
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", exit)
left_frame = tk.Frame()

# Create figure
figure = plt.Figure()

# Add figure to window
canvas = FigureCanvasTkAgg(figure, window)
canvas.get_tk_widget().pack(side=tk.LEFT)

# Create and initialise plots
ax = figure.add_subplot(111)
ax.set_xlim(maths.x_min, maths.x_max)
ax.set_ylim(maths.E_min, maths.E_max)
ax.set_ylabel('Energy (eV)')
ax.set_xlabel('Position (nm)')
ax.set_facecolor((1, 1, 1, 0))

ax2 = ax.twinx()
ax2.set_ylim(maths.psi_min, maths.psi_max)
ax2.set_ylabel('Wave function')
ax2.set_zorder(-1)

maths.calculate_energy()
energy_plt, = ax.plot(maths.energy[0], maths.energy[1], 'g--', linewidth=1, label="Energy")

maths.calculate_potential()
potential_plt, = ax.plot(maths.potential[0], maths.potential[1], 'b', label="Potential")

maths.calculate_wave_function()
wave_function_plt, = ax2.plot(maths.psi[0], maths.psi[1], 'k', linewidth=1, label="Wave function")

ax.legend()
figure.tight_layout()

# Creating sliders
E_slider = tk.Scale()
V_0_slider = tk.Scale()
V_barrier_slider = tk.Scale()
V_1_slider = tk.Scale()
barrier_start_slider = tk.Scale()
barrier_end_slider = tk.Scale()

# Creating text boxes
E_textbox = tk.Entry(left_frame, width=10)
V_0_textbox = tk.Entry(left_frame, width=10)
V_barrier_textbox = tk.Entry(left_frame, width=10)
V_1_textbox = tk.Entry(left_frame, width=10)
barrier_start_textbox = tk.Entry(left_frame, width=10)
barrier_end_textbox = tk.Entry(left_frame, width=10)

# Creating reset button
reset_button = tk.Button(left_frame, text="Reset")


def initialise():
	global  V_0_slider, V_barrier_slider, barrier_start_slider, barrier_end_slider, E_slider

	# Updating sliders with correct values and binding command
	E_slider = tk.Scale(left_frame, from_=maths.E_min, to=maths.E_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Energy (eV)", showvalue=0, command=controller.update_e)
	V_0_slider = tk.Scale(left_frame, from_=maths.E_min, to=maths.E_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Potential before barrier (eV)", showvalue=0, command=controller.update_v_0)
	V_barrier_slider = tk.Scale(left_frame, from_=maths.E_min, to=maths.E_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Barrier potential (eV)", showvalue=0, command=controller.update_v_barrier)
	V_1_slider = tk.Scale(left_frame, from_=maths.E_min, to=maths.E_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Potential after barrier (eV)", showvalue=0, command=controller.update_v_1)
	barrier_start_slider = tk.Scale(left_frame, from_=maths.x_min, to=maths.x_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Barrier start (nm)", showvalue=0, command=controller.update_barrier_start)
	barrier_end_slider = tk.Scale(left_frame, from_=maths.x_min, to=maths.x_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Barrier end (nm)", showvalue=0, command=controller.update_barrier_end)

	# Adding all to view
	left_frame.pack(side=tk.RIGHT, padx=10, anchor=tk.N)
	E_slider.grid(row=0, column=0)
	E_textbox.grid(row=0, column=1, sticky=tk.S)
	V_0_slider.grid(row=1, column=0)
	V_0_textbox.grid(row=1, column=1, sticky=tk.S)
	V_barrier_slider.grid(row=2, column=0)
	V_barrier_textbox.grid(row=2, column=1, sticky=tk.S)
	V_1_slider.grid(row=3, column=0)
	V_1_textbox.grid(row=3, column=1, sticky=tk.S)
	barrier_start_slider.grid(row=4, column=0)
	barrier_start_textbox.grid(row=4, column=1, sticky=tk.S)
	barrier_end_slider.grid(row=5, column=0)
	barrier_end_textbox.grid(row=5, column=1, sticky=tk.S)
	reset_button.grid(row=6, column=1, sticky=tk.NSEW)

	# Binding textbox and button actions
	E_textbox.bind("<Return>", controller.update_e_from_tb)
	V_0_textbox.bind("<Return>", controller.update_v_0_from_tb)
	V_barrier_textbox.bind("<Return>", controller.update_v_barrier_from_tb)
	V_1_textbox.bind("<Return>", controller.update_v_1_from_tb)
	barrier_start_textbox.bind("<Return>", controller.update_barrier_start_from_tb)
	barrier_end_textbox.bind("<Return>", controller.update_barrier_end_from_tb)
	reset_button.bind("<Button-1>", controller.reset_values)

	# Setting default values
	controller.update_textbox(E_textbox, maths.E)
	controller.update_textbox(V_0_textbox, maths.V_0)
	controller.update_textbox(V_barrier_textbox, maths.V_barrier)
	controller.update_textbox(V_1_textbox, maths.V_1)
	controller.update_textbox(barrier_start_textbox, maths.barrier_start)
	controller.update_textbox(barrier_end_textbox, maths.barrier_end)

	E_slider.set(maths.E)
	V_0_slider.set(maths.V_0)
	V_barrier_slider.set(maths.V_barrier)
	V_1_slider.set(maths.V_1)
	barrier_start_slider.set(maths.barrier_start)
	barrier_end_slider.set(maths.barrier_end)

	window.mainloop()

if __name__ == "__main__":
	print("main.py should be started instead")
	exit()


import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import data
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

# Create and initialise plot
ax = figure.add_subplot(111)
ax.set_xlim(data.x_min, data.x_max)
ax.set_ylim(data.E_min, data.E_max)
ax.set_ylabel('$Energy$ (eV)')
ax.set_xlabel('$Position$ (nm)')

data.calculate_energy()
energy_plt, = ax.plot(data.energy[0], data.energy[1], 'g--', linewidth=1, label="Energy")

data.calculate_potential()
potential_plt, = ax.plot(data.potential[0], data.potential[1], 'b', label="Potential")
ax.legend()
figure.tight_layout()

# Creating sliders
E_slider = tk.Scale()
V_0_slider = tk.Scale()
V_barrier_slider = tk.Scale()
barrier_start_slider = tk.Scale()
barrier_end_slider = tk.Scale()

# Creating text boxes
E_textbox = tk.Entry(left_frame, width=10)
V_0_textbox = tk.Entry(left_frame, width=10)
V_barrier_textbox = tk.Entry(left_frame, width=10)
barrier_start_textbox = tk.Entry(left_frame, width=10)
barrier_end_textbox = tk.Entry(left_frame, width=10)

# Creating reset button
reset_button = tk.Button(left_frame, text="Reset")


def initialise():
	global  V_0_slider, V_barrier_slider, barrier_start_slider, barrier_end_slider, E_slider

	# Updating sliders with correct values and binding command
	E_slider = tk.Scale(left_frame, from_=data.E_min, to=data.E_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Energy (eV)", showvalue=0, command=controller.update_e)
	V_0_slider = tk.Scale(left_frame, from_=data.E_min, to=data.E_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Initial potential (eV)", showvalue=0, command=controller.update_v_0)
	V_barrier_slider = tk.Scale(left_frame, from_=data.E_min, to=data.E_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Barrier potential (eV)", showvalue=0, command=controller.update_v_barrier)
	barrier_start_slider = tk.Scale(left_frame, from_=data.x_min, to=data.x_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Barrier start (nm)", showvalue=0, command=controller.update_barrier_start)
	barrier_end_slider = tk.Scale(left_frame, from_=data.x_min, to=data.x_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Barrier end (nm)", showvalue=0, command=controller.update_barrier_end)

	# Adding all to view
	left_frame.pack(side=tk.RIGHT, padx=10, anchor=tk.N)
	E_slider.grid(row=0, column=0)
	E_textbox.grid(row=0, column=1, sticky=tk.S)
	V_0_slider.grid(row=1, column=0)
	V_0_textbox.grid(row=1, column=1, sticky=tk.S)
	V_barrier_slider.grid(row=2, column=0)
	V_barrier_textbox.grid(row=2, column=1, sticky=tk.S)
	barrier_start_slider.grid(row=3, column=0)
	barrier_start_textbox.grid(row=3, column=1, sticky=tk.S)
	barrier_end_slider.grid(row=4, column=0)
	barrier_end_textbox.grid(row=4, column=1, sticky=tk.S)
	reset_button.grid(row=5, column=1, sticky=tk.NSEW)

	# Binding textbox and button actions
	E_textbox.bind("<Return>", controller.update_e_from_tb)
	V_0_textbox.bind("<Return>", controller.update_v_0_from_tb)
	V_barrier_textbox.bind("<Return>", controller.update_v_barrier_from_tb)
	barrier_start_textbox.bind("<Return>", controller.update_barrier_start_from_tb)
	barrier_end_textbox.bind("<Return>", controller.update_barrier_end_from_tb)
	reset_button.bind("<Button-1>", controller.reset_values)

	# Setting default values
	controller.update_textbox(E_textbox, data.E)
	controller.update_textbox(V_0_textbox, data.V_0)
	controller.update_textbox(V_barrier_textbox, data.V_barrier)
	controller.update_textbox(barrier_start_textbox, data.barrier_start)
	controller.update_textbox(barrier_end_textbox, data.barrier_end)

	E_slider.set(data.E)
	V_0_slider.set(data.V_0)
	V_barrier_slider.set(data.V_barrier)
	barrier_start_slider.set(data.barrier_start)
	barrier_end_slider.set(data.barrier_end)

	window.mainloop()

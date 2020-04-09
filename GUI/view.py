if __name__ == "__main__":
	print("main.py should be started instead")
	exit()


import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import maths
import controller

play_icon = "⏵"
pause_icon = "⏸"


# Create window
window = tk.Tk()
window.title("PP GUI")
window.iconbitmap("")
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", exit)
left_frame = tk.Frame()
left_frame.pack(side=tk.LEFT)
right_frame = tk.Frame()
right_frame.pack(side=tk.RIGHT, padx=10, anchor=tk.N)
time_control_frame = tk.Frame(left_frame)
time_control_frame.pack(side=tk.BOTTOM, padx=5, pady=2, fill=tk.X)
time_control_frame.columnconfigure(3, weight=1)


# Create figure
figure = plt.Figure()

# Add figure to window
canvas = FigureCanvasTkAgg(figure, left_frame)
canvas.get_tk_widget().pack(side=tk.TOP)

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
E_slider = tk.Scale(right_frame, from_=maths.E_limit, to=maths.E_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Energy (eV)", showvalue=0)
V_0_slider = tk.Scale(right_frame, from_=maths.E_min, to=maths.E_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Potential before barrier (eV)", showvalue=0)
V_barrier_slider = tk.Scale(right_frame, from_=maths.E_min, to=maths.E_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Barrier potential (eV)", showvalue=0)
V_1_slider = tk.Scale(right_frame, from_=maths.E_min, to=maths.E_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Potential after barrier (eV)", showvalue=0)
barrier_start_slider = tk.Scale(right_frame, state="disabled", from_=maths.x_min, to=maths.x_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Barrier start (nm) [disabled]", showvalue=0)
barrier_end_slider = tk.Scale(right_frame, from_=maths.x_min, to=maths.x_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Barrier end (nm)", showvalue=0)

# Creating text boxes
E_textbox = tk.Entry(right_frame, width=10)
V_0_textbox = tk.Entry(right_frame, width=10)
V_barrier_textbox = tk.Entry(right_frame, width=10)
V_1_textbox = tk.Entry(right_frame, width=10)
barrier_start_textbox = tk.Entry(right_frame, width=10, state="disabled")
barrier_end_textbox = tk.Entry(right_frame, width=10)

# Creating radio buttons
wave_packet_bool = tk.BooleanVar()
wave_packet_bool.set(maths.wave_packet)
plane_wave = tk.Radiobutton(right_frame, text="Plane wave", variable=wave_packet_bool, val=False)
wave_packet = tk.Radiobutton(right_frame, text="Wave packet", variable=wave_packet_bool, val=True)

# Creating reset button
reset_button = tk.Button(right_frame, text="Reset")

# Time controls
t_label = tk.Label(time_control_frame, text="Time")
t_play_pause = tk.Button(time_control_frame, text=play_icon, state="disabled")
t_stop = tk.Button(time_control_frame, text="⏹")
t_slider = tk.Scale(time_control_frame, from_=maths.t_min, to=maths.t_max, resolution=0.01, orient=tk.HORIZONTAL, showvalue=0)
t_textbox = tk.Entry(time_control_frame, width=10)

# Adding all to view
t_label.grid(row=0, column=0)
t_play_pause.grid(row=0, column=1)
t_stop.grid(row=0, column=2)
t_slider.grid(row=0, column=3, sticky=tk.EW)
t_textbox.grid(row=0, column=4)

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
plane_wave.grid(row=7, column=0, sticky=tk.W)
wave_packet.grid(row=8, column=0, sticky=tk.W)


def initialise():
	# Bind plot actions with corresponding functions
	figure.canvas.mpl_connect('button_press_event', controller.button_press_callback)
	figure.canvas.mpl_connect('button_release_event', controller.button_release_callback)
	figure.canvas.mpl_connect('motion_notify_event', controller.motion_notify_callback)

	# Binding command to sliders
	E_slider.configure(command=controller.update_e)
	V_0_slider.configure(command=controller.update_v_0)
	V_barrier_slider.configure(command=controller.update_v_barrier)
	V_1_slider.configure(command=controller.update_v_1)
	barrier_start_slider.configure(command=controller.update_barrier_start)
	barrier_end_slider.configure(command=controller.update_barrier_end)
	t_slider.configure(command=controller.update_t)

	# Binding button actions
	reset_button.configure(command=controller.reset_values)
	t_play_pause.configure(command=controller.play_pause)
	t_stop.configure(command=controller.stop)

	# Binding radio button actions
	plane_wave.configure(command=controller.change_wave_type)
	wave_packet.configure(command=controller.change_wave_type, state="disabled")

	# Binding textbox actions
	E_textbox.bind("<Return>", controller.update_e_from_tb)
	V_0_textbox.bind("<Return>", controller.update_v_0_from_tb)
	V_barrier_textbox.bind("<Return>", controller.update_v_barrier_from_tb)
	V_1_textbox.bind("<Return>", controller.update_v_1_from_tb)
	barrier_start_textbox.bind("<Return>", controller.update_barrier_start_from_tb)
	barrier_end_textbox.bind("<Return>", controller.update_barrier_end_from_tb)
	t_textbox.bind("<Return>", controller.update_t_from_tb)

	# Setting default values
	controller.update_textbox(E_textbox, maths.E)
	controller.update_textbox(V_0_textbox, maths.V_0)
	controller.update_textbox(V_barrier_textbox, maths.V_barrier)
	controller.update_textbox(V_1_textbox, maths.V_1)
	controller.update_textbox(barrier_start_textbox, maths.barrier_start)
	controller.update_textbox(barrier_end_textbox, maths.barrier_end)
	controller.update_textbox(t_textbox, maths.t)

	E_slider.set(maths.E)
	V_0_slider.set(maths.V_0)
	V_barrier_slider.set(maths.V_barrier)
	V_1_slider.set(maths.V_1)
	barrier_start_slider.set(maths.barrier_start)
	barrier_end_slider.set(maths.barrier_end)
	t_slider.set(maths.t)

	window.mainloop()

if __name__ == "__main__":
	print("main.py should be started instead")
	exit()


import data
import view

# For mouse precision (also dictates how close the sides of the potential can be)
relative_epsilon = 0.05
in_range = ""
epsilon_x = (data.x_max - data.x_min) * relative_epsilon
epsilon_E = (data.E_max - data.E_min) * relative_epsilon


def update_textbox(textbox, value):
	textbox.delete(0, view.tk.END)
	textbox.insert(0, value)


def update_v_0(value):
	data.V_0 = float(value)
	view.V_0_slider.set(data.V_0)
	update_textbox(view.V_0_textbox, round(data.V_0, 3))
	update_potential()


def update_v_barrier(value):
	data.V_barrier = float(value)
	view.V_barrier_slider.set(data.V_barrier)
	update_textbox(view.V_barrier_textbox, round(data.V_barrier, 3))
	update_potential()


def update_barrier_start(value):
	if float(value) < data.barrier_end - epsilon_x:
		data.barrier_start = float(value)
	else:
		data.barrier_start = data.barrier_end - epsilon_x
	view.barrier_start_slider.set(data.barrier_start)
	update_textbox(view.barrier_start_textbox, round(data.barrier_start, 3))
	update_potential()


def update_barrier_end(value):
	if float(value) > data.barrier_start + epsilon_x:
		data.barrier_end = float(value)
	else:
		data.barrier_end = data.barrier_start + epsilon_x
	view.barrier_end_slider.set(data.barrier_end)
	update_textbox(view.barrier_end_textbox, round(data.barrier_end, 3))
	update_potential()


def update_potential():
	data.calculate_potential()
	view.potential_plt.set_data(data.potential[0], data.potential[1])
	view.plt.draw()
	view.canvas.draw()


def reset_values(event):
	update_v_0(data.default_V_0)
	update_v_barrier(data.default_V_barrier)
	update_barrier_start(data.default_barrier_start)
	update_barrier_end(data.default_barrier_end)


def button_press_callback(event):
	global in_range
	if event.inaxes:
		if (
				data.x_min <= event.xdata <= data.barrier_start or data.barrier_end <= event.xdata <= data.x_max) and data.V_0 - epsilon_E <= event.ydata <= data.V_0 + epsilon_E:
			in_range = "V_0"
		elif data.barrier_start <= event.xdata <= data.barrier_end and data.V_barrier - epsilon_E <= event.ydata <= data.V_barrier + epsilon_E:
			in_range = "V_barrier"
		elif data.barrier_start - epsilon_x <= event.xdata <= data.barrier_start + epsilon_x and data.V_0 <= event.ydata <= data.V_barrier:
			in_range = "barrier_start"
		elif data.barrier_end - epsilon_x <= event.xdata <= data.barrier_end + epsilon_x and data.V_0 <= event.ydata <= data.V_barrier:
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
	update_v_0(good_value(view.V_0_textbox.get(), data.V_0))


def update_v_barrier_from_tb(event):
	update_v_barrier(good_value(view.V_barrier_textbox.get(), data.V_barrier))


def update_barrier_start_from_tb(event):
	update_barrier_start(good_value(view.barrier_start_textbox.get(), data.barrier_start))


def update_barrier_end_from_tb(event):
	update_barrier_end(good_value(view.barrier_end_textbox.get(), data.barrier_end))


def good_value(value, old_value):
	try:
		float(value)
		return float(value)
	except ValueError:
		return old_value


def connect_figure_actions():
	view.figure.canvas.mpl_connect('button_press_event', button_press_callback)
	view.figure.canvas.mpl_connect('button_release_event', button_release_callback)
	view.figure.canvas.mpl_connect('motion_notify_event', motion_notify_callback)


def initialise():
	connect_figure_actions()
	view.initialise()

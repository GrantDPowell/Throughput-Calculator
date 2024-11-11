import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from pandastable import Table  # Used to display data tables within Tkinter GUI

# Calculation functions for cycles per instruction (CPI) and throughput
# These functions return the CPI and throughput for cases with and without branch prediction

def calculate_no_prediction(Pb, Pt, b):
    """
    Calculate CPI and throughput without branch prediction.
    Pb: Probability of a branch instruction
    Pt: Probability that the branch is taken
    b: Branch penalty (in cycles)
    """
    cpi = 1 + Pb * Pt * b  # Basic CPI formula without branch prediction
    throughput = 1 / cpi  # Throughput is the reciprocal of CPI
    return cpi, throughput

def calculate_with_prediction(Pb, Pt, b, Pc, c):
    """
    Calculate CPI and throughput with branch prediction.
    Pb: Probability of a branch instruction
    Pt: Probability that the branch is taken
    b: Branch penalty (in cycles) for mispredictions
    Pc: Probability of a correct branch prediction
    c: Reduced penalty (in cycles) for correctly predicted branches
    """
    cpi = 1 + Pb * ((1 - Pc) * Pt * b + Pc * Pt * c)  # CPI formula with branch prediction
    throughput = 1 / cpi  # Throughput is the reciprocal of CPI
    return cpi, throughput

# Functions to increment or decrement a value in the Tkinter interface
def increment(var, step=0.1):
    """Increments a Tkinter variable by a specified step."""
    var.set(round(float(var.get()) + step, 2))

def decrement(var, step=0.1):
    """Decrements a Tkinter variable by a specified step, ensuring it doesn't go negative."""
    new_value = round(float(var.get()) - step, 2)
    if new_value >= 0:  # Only update if new value is non-negative
        var.set(new_value)

# Toggle function to switch the Y-axis between CPI and Throughput on graphs
def toggle_y_axis(y_axis_var, update_func):
    """Toggles the Y-axis between 'CPI' and 'Throughput' and updates the graph."""
    y_axis_var.set("Throughput" if y_axis_var.get() == "CPI" else "CPI")
    update_func()  # Calls the update function to refresh the graph

# Part A: Update Graph for calculations without branch prediction
def update_graph_part_a(all_data=False):
    """
    Updates the graph for Part A (No Branch Prediction).
    If all_data=True, iterates over a range of values; otherwise, uses single user-selected values.
    """
    fig_part_a.clear()  # Clear previous plot
    ax = fig_part_a.add_subplot(111)  # Add new subplot
    
    # Define the range for Pb (Branch Probability)
    Pb_min = float(pb_min_var.get())
    Pb_max = float(pb_max_var.get())
    pb_res = float(pb_res_var.get())
    Pb_values = [round(Pb_min + pb_res * i, 10) for i in range(int((Pb_max - Pb_min) / pb_res) + 1)]
    if Pb_values[-1] < Pb_max:
        Pb_values.append(Pb_max)  # Ensure the maximum value is included
    
    # Define Pt and b values based on user selection or full range
    if all_data:
        Pt_min = float(pt_min_var.get())
        Pt_max = float(pt_max_var.get())
        pt_res = float(pt_res_var.get())
        Pt_values = [round(Pt_min + pt_res * i, 10) for i in range(int((Pt_max - Pt_min) / pt_res) + 1)]
        if Pt_values[-1] < Pt_max:
            Pt_values.append(Pt_max)  # Ensure the maximum value is included
        b_values = [3, 4]  # Test with branch penalties of 3 and 4 cycles
    else:
        Pt_values = [pt_slider_a.get()]
        b_values = [b_slider_a.get()]
    
    # Plot the CPI or Throughput vs Pb for each Pt and b value
    for b in b_values:
        linestyle = '-' if b == 3 else '--'  # Different line styles for different b values
        for Pt in Pt_values:
            values = [calculate_no_prediction(Pb, Pt, b) for Pb in Pb_values]  # Calculate values
            y_values = [val[0] if y_axis_var_a.get() == "CPI" else val[1] for val in values]
            ax.plot(Pb_values, y_values, label=f'Pt={Pt:.2f}, b={b}', linestyle=linestyle)
    
    # Label and render the plot
    ax.set_title(f"{y_axis_var_a.get()} vs Pb (No Prediction)")
    ax.set_xlabel("Pb (Branch Probability)")
    ax.set_ylabel(y_axis_var_a.get())
    ax.legend(loc="upper left", fontsize='small')
    ax.grid(True)
    canvas_part_a.draw()

# Part A: Update Table for displaying data without branch prediction
def update_table_part_a(all_data=False):
    """
    Updates the data table for Part A (No Branch Prediction).
    If all_data=True, iterates over a range of values; otherwise, uses single user-selected values.
    """
    data_no_pred = {"Pb": [], "Pt": [], "b": [], "CPI": [], "Throughput": []}
    
    # Define the range for Pb values
    Pb_min = float(pb_min_var.get())
    Pb_max = float(pb_max_var.get())
    pb_res = float(pb_res_var.get())
    Pb_values = [round(Pb_min + pb_res * i, 10) for i in range(int((Pb_max - Pb_min) / pb_res) + 1)]
    if Pb_values[-1] < Pb_max:
        Pb_values.append(Pb_max)  # Ensure the maximum value is included
    
    # Define Pt and b values based on user selection or full range
    if all_data:
        Pt_min = float(pt_min_var.get())
        Pt_max = float(pt_max_var.get())
        pt_res = float(pt_res_var.get())
        Pt_values = [round(Pt_min + pt_res * i, 10) for i in range(int((Pt_max - Pt_min) / pt_res) + 1)]
        if Pt_values[-1] < Pt_max:
            Pt_values.append(Pt_max)  # Ensure the maximum value is included
        b_values = [3, 4]
    else:
        Pt_values = [pt_slider_a.get()]
        b_values = [b_slider_a.get()]
    
    # Populate the data dictionary for each combination of Pb, Pt, and b
    for b in b_values:
        for Pt in Pt_values:
            for Pb in Pb_values:
                cpi, throughput = calculate_no_prediction(Pb, Pt, b)
                data_no_pred["Pb"].append(Pb)
                data_no_pred["Pt"].append(round(Pt, 3))
                data_no_pred["b"].append(b)
                data_no_pred["CPI"].append(round(cpi, 3))
                data_no_pred["Throughput"].append(round(throughput, 3))

    # Create DataFrame and display in the PandasTable
    df_no_pred = pd.DataFrame(data_no_pred)
    table_part_a.model.df = df_no_pred
    table_part_a.redraw()


# Part B: Update Graph for calculations with branch prediction
def update_graph_part_b(all_data=False):
    """
    Updates the graph for Part B (With Branch Prediction).
    If all_data=True, iterates over a range of values; otherwise, uses single user-selected values.
    """
    fig_part_b.clear()
    ax = fig_part_b.add_subplot(111)
    
    # Define the range for Pc (Prediction Accuracy)
    Pc_min = float(pc_min_var.get())
    Pc_max = float(pc_max_var.get())
    pc_res = float(pc_res_var.get())
    Pc_values = [Pc_min + pc_res * i for i in range(int((Pc_max - Pc_min) / pc_res) + 1)]
    
    # Fixed values for Pt and b in Part B, testing with different c values
    Pb, Pt, b = 0.25, 0.6, 4
    if all_data:
        c_values = [0, 1, 2]
    else:
        c_values = [c_slider_b.get()]
    
    # Plot CPI or Throughput vs Pc for each value of c
    for c in c_values:
        values = [calculate_with_prediction(Pb, Pt, b, Pc, c) for Pc in Pc_values]
        y_values = [val[0] if y_axis_var_b.get() == "CPI" else val[1] for val in values]
        ax.plot(Pc_values, y_values, label=f'c={c}')
    
    # Label and render the plot
    ax.set_title(f"{y_axis_var_b.get()} vs Pc (With Prediction)")
    ax.set_xlabel("Pc (Prediction Accuracy)")
    ax.set_ylabel(y_axis_var_b.get())
    ax.legend(loc="upper left", fontsize='small')
    ax.grid(True)
    canvas_part_b.draw()

# Part B: Update Table for displaying data with branch prediction
def update_table_part_b(all_data=False):
    """
    Updates the data table for Part B (With Branch Prediction).
    If all_data=True, iterates over a range of values; otherwise, uses single user-selected values.
    """
    data_pred = {"Pc": [], "Pt": [], "b": [], "c": [], "CPI": [], "Throughput": []}
    
    # Define the range for Pc values
    Pc_min = float(pc_min_var.get())
    Pc_max = float(pc_max_var.get())
    pc_res = float(pc_res_var.get())
    Pc_values = [Pc_min + pc_res * i for i in range(int((Pc_max - Pc_min) / pc_res) + 1)]
    
    # Fixed values for Pb, Pt, and b, with varying values for c
    Pb, Pt, b = 0.25, 0.6, 4
    if all_data:
        c_values = [0, 1, 2]
    else:
        c_values = [c_slider_b.get()]
    
    # Populate the data dictionary for each combination of Pc and c
    for c in c_values:
        for Pc in Pc_values:
            cpi, throughput = calculate_with_prediction(Pb, Pt, b, Pc, c)
            data_pred["Pc"].append(Pc)
            data_pred["Pt"].append(Pt)
            data_pred["b"].append(b)
            data_pred["c"].append(c)
            data_pred["CPI"].append(round(cpi, 3))
            data_pred["Throughput"].append(round(throughput, 3))

    # Create DataFrame and display in the PandasTable
    df_pred = pd.DataFrame(data_pred)
    table_part_b.model.df = df_pred
    table_part_b.redraw()

# GUI Setup
root = tk.Tk()
root.title("Pipeline Calculator - Parts A & B")
root.geometry("1600x850")

# Tab control setup for Part A and Part B
tab_control = ttk.Notebook(root)
tab_part_a = ttk.Frame(tab_control)
tab_part_b = ttk.Frame(tab_control)
tab_control.add(tab_part_a, text="Part A: No Branch Prediction")
tab_control.add(tab_part_b, text="Part B: With Branch Prediction")
tab_control.pack(expand=1, fill='both')

# Resolution Adjuster Dropdowns
res_options = [0.1, 0.05, 0.02, 0.01]

# Part A Widgets
tk.Label(tab_part_a, text="Pt (Branch Taken Probability)").grid(row=0, column=0, sticky='w')
pt_slider_a = tk.Scale(tab_part_a, from_=0.1, to=1, resolution=0.01, orient=tk.HORIZONTAL)
pt_slider_a.set(0.6)
pt_slider_a.grid(row=0, column=1, sticky='w')

tk.Label(tab_part_a, text="Pt Resolution (Calculate All)").grid(row=0, column=2, sticky='w')
pt_res_var = tk.StringVar(value="0.1")
pt_res_menu = ttk.Combobox(tab_part_a, textvariable=pt_res_var, values=res_options, width=5)
pt_res_menu.grid(row=0, column=3, sticky='w')

tk.Label(tab_part_a, text="Pt Min").grid(row=1, column=3, sticky='w')
pt_min_var = tk.StringVar(value="0.5")
tk.Button(tab_part_a, text="-", command=lambda: decrement(pt_min_var)).grid(row=1, column=3, sticky='e')
tk.Label(tab_part_a, textvariable=pt_min_var, width=5).grid(row=1, column=4)
tk.Button(tab_part_a, text="+", command=lambda: increment(pt_min_var)).grid(row=1, column=5, sticky='w')

tk.Label(tab_part_a, text="Pt Max").grid(row=2, column=3, sticky='w')
pt_max_var = tk.StringVar(value="0.7")
tk.Button(tab_part_a, text="-", command=lambda: decrement(pt_max_var)).grid(row=2, column=3, sticky='e')
tk.Label(tab_part_a, textvariable=pt_max_var, width=5).grid(row=2, column=4)
tk.Button(tab_part_a, text="+", command=lambda: increment(pt_max_var)).grid(row=2, column=5, sticky='w')

tk.Label(tab_part_a, text="b (Branch Penalty)").grid(row=2, column=0, sticky='w')
b_slider_a = tk.Scale(tab_part_a, from_=3, to=4, resolution=1, orient=tk.HORIZONTAL)
b_slider_a.set(3)
b_slider_a.grid(row=2, column=1, sticky='w')

# Range selector for Pb with + and - buttons
tk.Label(tab_part_a, text="Pb Resolution (Calculate All)").grid(row=3, column=2, sticky='w')
pb_res_var = tk.StringVar(value="0.01")
pb_res_menu = ttk.Combobox(tab_part_a, textvariable=pb_res_var, values=res_options, width=5)
pb_res_menu.grid(row=3, column=3, sticky='w')

tk.Label(tab_part_a, text="Pb Min").grid(row=4, column=3, sticky='w')
pb_min_var = tk.StringVar(value="0.2")
tk.Button(tab_part_a, text="-", command=lambda: decrement(pb_min_var)).grid(row=4, column=3, sticky='e')
tk.Label(tab_part_a, textvariable=pb_min_var, width=5).grid(row=4, column=4)
tk.Button(tab_part_a, text="+", command=lambda: increment(pb_min_var)).grid(row=4, column=5, sticky='w')

tk.Label(tab_part_a, text="Pb Max").grid(row=5, column=3, sticky='w')
pb_max_var = tk.StringVar(value="0.3")
tk.Button(tab_part_a, text="-", command=lambda: decrement(pb_max_var)).grid(row=5, column=3, sticky='e')
tk.Label(tab_part_a, textvariable=pb_max_var, width=5).grid(row=5, column=4)
tk.Button(tab_part_a, text="+", command=lambda: increment(pb_max_var)).grid(row=5, column=5, sticky='w')

# Toggle for Y-axis
y_axis_var_a = tk.StringVar(value="Throughput")
y_axis_button_a = ttk.Button(tab_part_a, text="Toggle Y-axis (CPI/Throughput)", command=lambda: toggle_y_axis(y_axis_var_a, update_graph_part_a))
y_axis_button_a.grid(row=5, column=0, columnspan=1)

calc_button_a = ttk.Button(tab_part_a, text="Calculate 1 Pt", command=lambda: [update_graph_part_a(), update_table_part_a()])
calc_button_a.grid(row=5, column=1, pady=10)
calc_all_button_a = ttk.Button(tab_part_a, text="Calculate All Pt", command=lambda: [update_graph_part_a(all_data=True), update_table_part_a(all_data=True)])
calc_all_button_a.grid(row=5, column=2, pady=10)

# Graph and Table setup for Part A
fig_part_a = plt.Figure(figsize=(10, 6), dpi=100)
canvas_part_a = FigureCanvasTkAgg(fig_part_a, master=tab_part_a)
canvas_part_a.get_tk_widget().grid(row=6, column=0, columnspan=8, sticky="nsew")

table_frame_a = tk.Frame(tab_part_a)
table_frame_a.grid(row=1, column=8, rowspan=10, columnspan=6, sticky="nsew")
table_part_a = Table(table_frame_a, dataframe=pd.DataFrame(), showtoolbar=False, showstatusbar=False)
table_part_a.show()

# Part B Widgets - Slider, Range Selectors, Buttons, Graph, and Table
tk.Label(tab_part_b, text="c (Prediction Penalty)").grid(row=0, column=0, sticky='w')
c_slider_b = tk.Scale(tab_part_b, from_=0, to=2, resolution=1, orient=tk.HORIZONTAL)
c_slider_b.set(1)
c_slider_b.grid(row=0, column=1, sticky='w')

tk.Label(tab_part_b, text="Pc Resolution (Calculate All)").grid(row=0, column=3, sticky='w')
pc_res_var = tk.StringVar(value="0.1")
pc_res_menu = ttk.Combobox(tab_part_b, textvariable=pc_res_var, values=res_options, width=5)
pc_res_menu.grid(row=0, column=4, sticky='w')

# Range selector for Pc with + and - buttons
tk.Label(tab_part_b, text="Pc Min").grid(row=1, column=3, sticky='w')
pc_min_var = tk.StringVar(value="0.4")
tk.Button(tab_part_b, text="-", command=lambda: decrement(pc_min_var)).grid(row=1, column=3, sticky='e')
tk.Label(tab_part_b, textvariable=pc_min_var, width=5).grid(row=1, column=4)
tk.Button(tab_part_b, text="+", command=lambda: increment(pc_min_var)).grid(row=1, column=5, sticky='w')

tk.Label(tab_part_b, text="Pc Max").grid(row=2, column=3, sticky='w')
pc_max_var = tk.StringVar(value="0.8")
tk.Button(tab_part_b, text="-", command=lambda: decrement(pc_max_var)).grid(row=2, column=3, sticky='e')
tk.Label(tab_part_b, textvariable=pc_max_var, width=5).grid(row=2, column=4)
tk.Button(tab_part_b, text="+", command=lambda: increment(pc_max_var)).grid(row=2, column=5, sticky='w')

# Toggle for Y-axis in Part B
y_axis_var_b = tk.StringVar(value="Throughput")
y_axis_button_b = ttk.Button(tab_part_b, text="Toggle Y-axis (CPI/Throughput)", command=lambda: toggle_y_axis(y_axis_var_b, update_graph_part_b))
y_axis_button_b.grid(row=3, column=0, columnspan=1)

calc_button_b = ttk.Button(tab_part_b, text="Calculate 1 Pc", command=lambda: [update_graph_part_b(), update_table_part_b()])
calc_button_b.grid(row=3, column=1, pady=10)
calc_all_button_b = ttk.Button(tab_part_b, text="Calculate All Pc", command=lambda: [update_graph_part_b(all_data=True), update_table_part_b(all_data=True)])
calc_all_button_b.grid(row=3, column=2, pady=10)

# Graph and Table setup for Part B
fig_part_b = plt.Figure(figsize=(10, 6), dpi=100)
canvas_part_b = FigureCanvasTkAgg(fig_part_b, master=tab_part_b)
canvas_part_b.get_tk_widget().grid(row=4, column=0, columnspan=6, sticky="nsew")

table_frame_b = tk.Frame(tab_part_b)
table_frame_b.grid(row=1, column=8, rowspan=10, columnspan=6, sticky="nsew")
table_part_b = Table(table_frame_b, dataframe=pd.DataFrame(), showtoolbar=False, showstatusbar=False)
table_part_b.show()

root.mainloop()

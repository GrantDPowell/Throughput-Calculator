# Pipeline Throughput Calculator

A Python-based GUI application designed to calculate and analyze CPU pipeline throughput and cycles per instruction (CPI), with a focus on branch prediction and pipeline penalties. This application was developed as part of the *CPSC 4700 - Computer Architecture* course.

## Project Overview

This application computes CPI and throughput by varying input parameters and visually represents the results through graphs and tables. The calculator is structured into two main sections:

- **Part A:** Pipeline performance without branch prediction.
- **Part B:** Pipeline performance with branch prediction.

### Application Features

- **User-defined parameter controls**
- **Dynamic graphing** of CPI and throughput
- **Tabulated data views**

## Features

- **Graphical User Interface**: Built using Tkinter, featuring interactive sliders and buttons.
- **Data Visualization**: Utilizes Matplotlib for graphing CPI and throughput against various pipeline parameters.
- **Data Handling**: Uses the Pandas library for managing tabulated data, allowing flexible data export.
- **CX_Freeze Executable**: A pre-built executable for Windows systems.

## Usage

### 1. Installation

To run the source code, you’ll need Python and the following libraries:

- Tkinter
- Matplotlib
- Pandas
- Pandastable

Install these dependencies with:

```bash
pip install matplotlib pandas pandastable

### 2. Running the Application

To start the GUI application, navigate to the project directory and run:

```bash
python pipeline_calculator.py

Alternatively, use the provided executable file in the `exe` folder. If the shortcut doesn’t work, run the `.exe` directly from the root folder.

### 3. Parameter Controls

- **Part A (No Branch Prediction):** Control branch probability (Pb), branch taken probability (Pt), and branch penalty (b).
- **Part B (With Branch Prediction):** Adjust prediction accuracy (Pc) and reduced penalty (c) for correct predictions.

### 4. Toggle Y-Axis

Switch between CPI and Throughput display in graphs by clicking the toggle button.

## Analysis Reports

### Part A: Without Branch Prediction

Analyzes the impact of:

- **Branch Probability (Pb):** Increasing Pb leads to higher CPI and lower throughput.
- **Branch Taken Probability (Pt):** Higher Pt results in increased CPI and decreased throughput.
- **Branch Penalty (b):** A higher branch penalty directly reduces performance.

### Part B: With Branch Prediction

Explores the effects of:

- **Prediction Accuracy (Pc):** Increased Pc improves throughput by reducing CPI.
- **Reduced Penalty (c):** Lower penalties for correct predictions yield better performance.

## Graphs and Tables

Both parts include visual graphs and tables for easy analysis of parameter effects.

## Notes

- The source code includes raw calculation sheets for verification.
- A shortcut for the executable is included. If it fails, locate the `.exe` in the root directory.
- The project includes an Excel file for cross-checking calculations.

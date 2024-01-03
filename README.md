# Multi-Format Simulation Data Management of Mass-Spring-Damper System

## Project Overview

**Title:** Multi-Format Simulation Data Management of Mass-Spring-Damper System

**Objective:** Modeling and simulation of a mass-spring-damper system using the Runge-Kutta method based on reading-writing operations on different file formats and databases.

## Project Structure

### 1. SystemVisualization (Base Class):

- **Purpose:** Visualization of simulation results.

### 2. SystemWriter (Derived from SystemVisualization):

- **Purpose:** Manages writing simulation data to various file formats and a database.

### 3. SystemSolver (Derived from SystemWriter):

- **Purpose:** Models the mass-spring-damper system using the Runge-Kutta method.

The classes are organized in a hierarchical structure, facilitating code reuse and maintainability.

## Running Simulations

You can use the `SystemSolver` and `SystemVisualization` classes to perform simulations and visualize results. Below are examples of how to use these functionalities:

Create an instance of SystemSolver

    system = SystemSolver()

Solve the system using the Runge-Kutta method

    system.solve_system_runge_kutta()

Create an instance of SystemVisualization

    solver = SystemVisualization()

Visualize the simulation results

    system.visualize_results()

## Running Your Own Simulations

You can use and change the `SystemSolver` class to run your own simulations.

Customizing Simulation Parameters:

    mass: Mass of the system.
    damping_coefficient: Damping coefficient of the system.
    spring_constant: Spring constant of the system.
    force: External force applied to the system.
    sampling_frequency: Sampling frequency for the simulation.
    total_time: Total simulation time.

Adjust these parameters according to your specific simulation requirements to obtain your own simulation data.

This example simulates the system with the following parameters:

    mass=1.0
    damping_coefficient=1.0
    spring_constant=1.0
    force=1.0
    sampling_frequency=100
    total_time=10.0
![Simulation Visualization1](System%20Visualization/visualize_1.png)

This example simulates the system with the following parameters:

    mass=1.0
    damping_coefficient=3.0
    spring_constant=5.0
    force=3.0
    sampling_frequency=40
    total_time=10.0
![Simulation Visualization](System%20Visualization/visualize_2.png)

## Exporting to Excel
You can use the `SystemWriter` class to store simulation parameters, write simulation data, and export results to Excel. Below are examples of how to use these functionalities:

Create an instance of SystemWriter

    excel = SystemWriter()

Store simulation parameters

    excel.store_parameters()

Write simulation data to Excel

    excel.write_to_excel()

Write parameters to Excel

    excel.write_parameters_to_excel()

Write results to Excel

    excel.write_results_to_excel()

## Exporting to .txt .db .dat

Write to text file

    excel.write_to_text()

Write to dat file

    excel.write_to_dat()

Write to database

    excel.write_to_database()
    
## Restrictions

- Only `pandas`, `matplotlib.pyplot`, and `sqlalchemy` libraries are allowed for this project.

## Required Libraries

- `pandas`: For data manipulation and storage.
- `matplotlib.pyplot`: For data visualization.
- `sqlalchemy`: For interacting with databases.

## Project Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/erblgc/Multi-Format-Simulation-Data-Management-of-Mass-Spring-Damper-System
    ```

2. **Install the required libraries:**

    ```bash
    pip install pandas matplotlib sqlalchemy
    ```

## Usage

1. **Navigate to the project directory:**

    ```bash
    cd Multi-Format-Simulation-Data-Management-of-Mass-Spring-Damper-System
    ```

2. **Run the main script:**

    ```bash
    python main.py
    ```

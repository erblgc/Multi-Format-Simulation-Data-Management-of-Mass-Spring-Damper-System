import matplotlib.pyplot as plt
import pandas as pd
import sqlalchemy as db

# visualization of simulation result which mean plot the results
class SystemVisualization:
    def __init__(self, positions=[], velocities=[], sampling_frequency=0):
        self.positions = positions
        self.velocities = velocities
        self.sampling_frequency = sampling_frequency
    # plot results function
    def visualize_results(self, euler_type='Runge-Kutta'):
        plt.plot(self.time, self.positions, label='position')
        plt.plot(self.time, self.velocities, label='velocity')
        plt.xlabel('time')
        plt.ylabel('position&velocity')
        plt.title('System Visualization')
        plt.legend()
        plt.show()

# Manages the system parameters and writes the simulation data to a file
class SystemWriter(SystemVisualization):
    def __init__(self, positions=[], velocities=[], sampling_frequency=0):
        super().__init__(positions, velocities, sampling_frequency)
        self.time = [0.0]
    # store parameters function 
    def store_parameters(self, mass=1.0, damping_coefficient=1.0, spring_constant=1.0, force=1.0, sampling_frequency=100, total_time=10.0):
        self.mass = mass
        self.damping_coefficient = damping_coefficient
        self.spring_constant = spring_constant
        self.force = force
        self.sampling_frequency = sampling_frequency
        self.total_time = total_time
        solver = SystemSolver()
        solver.solve_system_runge_kutta()
        self.positions = solver.positions
        self.velocities = solver.velocities
        self.time = solver.time
    # writes simulation data to an Excel file function
    def write_to_excel(self, filename="simulation_data.xlsx"):
        df = pd.DataFrame({'time': self.time, 'position': self.positions, 'velocity': self.velocities})
        df.to_excel(filename)
    # write parameters to excel function
    def write_parameters_to_excel(self, filename="parameters.xlsx"):
        data = {'mass': self.mass, 
                'damping_coefficient': self.damping_coefficient, 
                'spring_constant': self.spring_constant, 
                'force': self.force, 
                'sampling_frequency': self.sampling_frequency, 
                'total_time': self.total_time}
        
        df = pd.DataFrame(data, index=[0]) 
        df.to_excel(filename, index=False)
    # write final results to excel function
    def write_results_to_excel(self, filename = "results.xlsx"):

        data = {'time': self.time[-1], 
                'position': self.positions[-1], 
                'velocity': self.velocities[-1]}
        
        df = pd.DataFrame(data, index=[0]) 
        df.to_excel(filename, index=False)

    # Reads simulation data from an Excel file
    def read_excel_file(self, filename="simulation_data.xlsx"):
        # read excel file
        df = pd.read_excel(filename)
        self.time = df['time'].tolist()
        self.positions = df['position'].tolist()
        self.velocities = df['velocity'].tolist()

    # Writes simulation data to a text file
    def write_to_text(self, filename="simulation_data.txt"):

        df = pd.DataFrame({'time': self.time, 'position': self.positions, 'velocity': self.velocities})
        df.to_csv(filename, sep='\t', index=False)

    # Reads simulation data from a text file
    def read_text_file(self, filename="simulation_data.txt"):
        df = pd.read_csv(filename, sep='\t')
        self.time = df['time'].tolist()
        self.positions = df['position'].tolist()
        self.velocities = df['velocity'].tolist()

    # Writes simulation data to a .dat file
    def write_to_dat(self, filename="simulation_data.dat"):

        df = pd.DataFrame({'time': self.time, 'position': self.positions, 'velocity': self.velocities})
        df.to_csv(filename, sep='\t', index=False)

    # Reads simulation data from a .dat file        
    def read_dat_file(self, filename="simulation_data.dat"):
        df = pd.read_csv(filename, sep='\t')
        self.time = df['time'].tolist()
        self.positions = df['position'].tolist()
        self.velocities = df['velocity'].tolist()

    def write_to_database(self, database_url="sqlite:///simulation_data.db"):
        df = pd.DataFrame({'time': self.time, 'position': self.positions, 'velocity': self.velocities})
        engine = db.create_engine(database_url)
        df.to_sql('simulation_data', engine, if_exists='replace')

    # Reads simulation data from a database
    def read_from_database(self, database_url="sqlite:///simulation_data.db"):
        engine = db.create_engine(database_url)
        connection = engine.connect()
        metadata = db.MetaData()
        simulation_data = db.Table('simulation_data', metadata, autoload=True, autoload_with=engine)
        query = db.select([simulation_data.columns.time, simulation_data.columns.position, simulation_data.columns.velocity])
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        self.time = [result[0] for result in ResultSet]
        self.positions = [result[1] for result in ResultSet]
        self.velocities = [result[2] for result in ResultSet]

class SystemSolver(SystemWriter):
    def __init__(self, mass=1.0, damping_coefficient=1.0, spring_constant=1.0, force=1.0,sampling_frequency=100, total_time=10.0):
        super().__init__(positions=[], velocities=[])
        self.mass = mass
        self.damping_coefficient = damping_coefficient
        self.spring_constant = spring_constant
        self.force = force
        self.sampling_frequency = sampling_frequency
        self.total_time = total_time
        self.time = [0.0]
        self.initial_position = 0.0
        self.initial_velocity = 0.0
        self.delta = 1.0/sampling_frequency
        self.x = self.initial_position
        self.v = self.initial_velocity
    # Solves the system using the Runge-Kutta method.
    def solve_system_runge_kutta(self):
        # initial conditions appended to lists
        self.positions.append(self.initial_position) 
        self.velocities.append(self.initial_velocity)

        # runde kutta method loop
        number_of_steps = int(self.total_time*self.sampling_frequency)

        for a in range(number_of_steps):    

            k1v = -((self.damping_coefficient*self.v)- (self.spring_constant*self.x) + self.force)/self.mass
            k1x = self.v
            k2v = (-self.damping_coefficient*(self.v + self.delta*k1v/2)  - self.spring_constant*(self.x + self.delta*k1x/2)+ self.force)/self.mass
            k2x = self.v + self.delta*k1v/2
            k3v = (-self.damping_coefficient*(self.v + self.delta*k2v/2)  - self.spring_constant*(self.x + self.delta*k2x/2)+ self.force)/self.mass
            k3x = self.v + self.delta*k2v/2
            k4v = (-self.damping_coefficient*(self.v + self.delta*k3v)  - self.spring_constant*(self.x + self.delta*k3x)+ self.force)/self.mass
            k4x = self.v + self.delta*k3v

            self.v = self.v + self.delta*(k1v + 2*k2v + 2*k3v + k4v)/6
            self.x = self.x + self.delta*(k1x + 2*k2x + 2*k3x + k4x)/6
            
            self.positions.append(self.x)
            self.velocities.append(self.v)

            self.time.append(self.time[-1] + self.delta)

        return self.positions, self.velocities

excel = SystemWriter()
system = SystemSolver()
solver = SystemVisualization()

system.solve_system_runge_kutta() # to solve the  system 
system.visualize_results() # see plot


excel.store_parameters() # store parameters
excel.write_to_excel() # write simulation datas to excel
excel.write_parameters_to_excel() # write parameters to excel
excel.write_results_to_excel() # write results to excel


# read excel file and print usage
"""
excel.read_excel_file("simulation_data.xlsx")
print("Time:")
for time in excel.time:
    print(time)

print("Positions:")
for position in excel.positions:
    print(position)

print("Velocities:")
for velocity in excel.velocities:
    print(velocity)
"""

excel.write_to_text() # write to text file

# read text file and print usage
"""
excel.read_text_file("simulation_data.txt") 

print("Time:")
for time in excel.time:
    print(time)
print("Positions:")
for position in excel.positions:
    print(position)

print("Velocities:")
for velocity in excel.velocities:
    print(velocity)
"""

excel.write_to_dat() # write to dat file

# read dat file and print usage
"""
excel.read_dat_file("simulation_data.dat")

print("Time:")
for time in excel.time:
    print(time)

print("Positions:")
for position in excel.positions:
    print(position)

print("Velocities:")
for velocity in excel.velocities:
    print(velocity)
"""
excel.write_to_database() # write to database

# read database and print usage
"""
excel.read_from_database()

print("Time:")
for time in excel.time:
    print(time)

print("Positions:")
for position in excel.positions:
    print(position)

print("Velocities:")
for velocity in excel.velocities:
    print(velocity)
"""


    
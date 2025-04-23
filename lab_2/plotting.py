import pandas as pd

import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'data.csv'  # Replace with your .csv file path
data = pd.read_csv(file_path)
# Extract data
time = data['Time']
position = data['Position']
acceleration_x = data['ax']
acceleration_y = data['ay']
acceleration_z = data['az']

# Plot position
plt.figure(figsize=(10, 6))
plt.plot(time, position, label='Position')
plt.title('Position vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Position')
plt.legend()
plt.grid()


#plot with subplots
fig, axs = plt.subplots(3, 1, figsize=(10, 10))
axs[0].plot(time, acceleration_x, label='Acceleration X')
axs[0].set_title('Acceleration X vs Time')
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Acceleration X')
axs[0].legend()
axs[0].grid()
axs[1].plot(time, acceleration_y, label='Acceleration Y')
axs[1].set_title('Acceleration Y vs Time')
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Acceleration Y')
axs[1].legend()
axs[1].grid()
axs[2].plot(time, acceleration_z, label='Acceleration Z')
axs[2].set_title('Acceleration Z vs Time')
axs[2].set_xlabel('Time (s)')
axs[2].set_ylabel('Acceleration Z')
axs[2].legend()
axs[2].grid()
plt.tight_layout()
plt.show()
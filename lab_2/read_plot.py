import serial
import time
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import json
import pandas as pd
# Serial port configuration
serial_port = '/dev/tty.wchusbserial14140'  # Replace with your Arduino's serial port (e.g., COM3 on Windows)
baud_rate = 115200
timeout = 5



# List to store all data for saving to CSV
all_data = []

# Function to save the data to a CSV file
def save_to_csv():
    if all_data:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"serial_data_{now}.csv"
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Time', 'Position', 'ax', 'ay', 'az'])
            writer.writerows(all_data)
        print(f"\nData saved to '{filename}'")
    else:
        print("\nNo data to save.")
    return filename

def plot_from_csv(csv_tag):
    # Load the CSV file
    data = pd.read_csv(csv_tag)
    # Extract data
    time = data['Time']
    # Convert time to seconds numpy array
    time = pd.to_numeric(time, errors='coerce').to_numpy()
    position = data['Position']
    acceleration_x = data['ax']
    acceleration_y = data['ay']
    acceleration_z = data['az']
    #angular speed from position/time
    angular_speed = [0]
    for i in range(1, len(position)):
        angular_speed.append((position[i] - position[i-1]) / (time[i] - time[i-1]))

    #angular acceleration from angular speed/time
    angular_acceleration = [0]
    for i in range(1, len(angular_speed)):
        angular_acceleration.append((angular_speed[i] - angular_speed[i-1]) / (time[i] - time[i-1]))

    # subplot position and angular speed
    fig, axs = plt.subplots(3, 1, figsize=(10, 8))
    axs[0].plot(time, position, label='Position')
    axs[0].set_title('Position vs Time')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Position (degrees)')
    axs[0].legend()
    axs[0].grid()
    axs[1].plot(time, angular_speed, label='Angular Speed', color='orange')
    axs[1].set_title('Angular Speed vs Time')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Angular Speed (degrees/s)')
    axs[1].legend()
    axs[1].grid()
    axs[2].plot(time, angular_acceleration, label='Angular Acceleration', color='green')
    axs[2].set_title('Angular Acceleration vs Time')
    axs[2].set_xlabel('Time (s)')
    axs[2].set_ylabel('Angular Acceleration (degrees/s^2)')
    axs[2].legend()
    axs[2].grid()
    plt.tight_layout()



    #plot with subplots
    fig, axs = plt.subplots(3, 1, figsize=(10, 8))
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


try:
    ser = serial.Serial(serial_port, baud_rate, timeout=timeout)
    time.sleep(2)  # Wait for the serial port to initialize
    input("Press Enter to start receiving data...")
    while True:
        
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if not line:
            continue
        elif line.startswith('{'):
            try:
                # Parse the JSON data
                data_dict = json.loads(line)
            except json.JSONDecodeError as e:
                print(e)
                continue  # Skip invalid JSON
        
            # Extract the values from the JSON data
            arduino_time = float(data_dict['time']) / 1000.0
            position = float(data_dict['p'])*360.0/1000.0 
            ax = float(data_dict['ax'])/1000.0
            ay = float(data_dict['ay'])/1000.0
            az = float(data_dict['az'])/1000.0

            # Add the data to the list for saving to CSV
            all_data.append([arduino_time, position, ax, ay, az])

except serial.SerialException as e:
    print(f"Error opening serial port {serial_port}: {e}")
except KeyboardInterrupt:
    print("Program terminated by user.")
    file=save_to_csv()
    plot_from_csv(file)

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")
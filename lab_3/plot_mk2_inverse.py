import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
from serial_control import SerialControl
import time

def inverse_kinematics(X=150,Y=0,Z=60, eff_off_x=65, eff_off_z=0):

    link_lengths = [55, 39, 135, 147, 66.3]
    offset_z = 100
    zb = Z - offset_z + eff_off_z
    l1 = link_lengths[2]
    l2 = link_lengths[3]
    
    q0 = np.arctan2(Y,X)

    if np.abs(Y)<1e-2:
        xo = X-eff_off_x
    else:
        xo = np.sqrt((X-eff_off_x*np.cos(q0))**2 + (Y-eff_off_x*np.sin(q0))**2)

    q1 = np.pi - np.arctan2(zb,xo) - np.arccos((xo**2 + zb**2 + l1**2-l2**2)/(2*l1*np.sqrt(xo**2 + zb**2)))
    q2 = np.pi/2 - q1 + np.arccos((l1**2+l2**2-xo**2-zb**2)/(2*l1*l2))

    #to deg
    q0 = -2*np.round(np.rad2deg(q0),0)+90
    q1 = np.round(np.rad2deg(q1),0)
    q2 = np.round(np.rad2deg(q2),0)
    return np.array([q0,q1,q2])



def move_xyz(x, y, z, eff_off = [56, 0, 0]):
    eff_off_x, eff_off_y, eff_off_z = eff_off
    q0, q1, q2 = inverse_kinematics(x, y, z, eff_off_x, eff_off_z)
    return q0, q1, q2


# The function to be called anytime a slider's value changes
def update(val):
    global mk2_comm
    #line.set_ydata(f(t, amp_slider.val, freq_slider.val))
    fig.canvas.draw_idle()
    # move the robot
    x = x_slider.val
    y = y_slider.val
    z = z_slider.val
    #update the point
    point.set_data(x, y)
    point2.set_data(x, z)


    q0,q1,q2 = move_xyz(x, y, z, eff_off=[60, 0, 24])
    #update the point
    mk2_comm.send_command([q0, q1, q2])
    print("q0,q1,q2: ",q0, q1, q2)

    
def reset(event):
    x_slider.reset()
    y_slider.reset()
    z_slider.reset()
    


if __name__ == "__main__":

    mk2_comm = SerialControl(port='COM8', baudrate=115200)
    mk2_comm.open_serial()
    time.sleep(1)
    # Create two subplots side view and top view
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax.set_title('Top view')
    ax2.set_title('Side view')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Z')
    ax.set_xlim(0, 300)
    ax.set_ylim(-100, 100)
    ax2.set_xlim(0, 300)
    ax2.set_ylim(0, 300)
    ax.grid()
    ax2.grid()
    
    #create a point to represent the end effector
    point, = ax.plot([], [], 'ro', markersize=10)
    point2, = ax2.plot([], [], 'ro', markersize=10)

    # adjust the main plot to make room for the sliders
    fig.subplots_adjust(bottom=0.25)

    #Make x slider
    axx = fig.add_axes([0.25, 0.15, 0.5, 0.05])
    x_slider = Slider(
        ax=axx,
        label="x",
        valmin=150,
        valmax=250,
        valinit=220,
        orientation="horizontal"
    )

    #Make y slider
    axy = fig.add_axes([0.25, 0.1, 0.5, 0.05])
    y_slider = Slider(
        ax=axy,
        label="y",
        valmin=-100,
        valmax=100,
        valinit=0,
        orientation="horizontal"
    )

    #Make z slider
    axz = fig.add_axes([0.25, 0.05, 0.5, 0.05])
    z_slider = Slider(
        ax=axz,
        label="z",
        valmin=0,
        valmax=250,
        valinit=220,
        orientation="horizontal"
    )

    # register the update function with each slider
    x_slider.on_changed(update)
    y_slider.on_changed(update)
    z_slider.on_changed(update)

    # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
    resetax = fig.add_axes([0.85, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', hovercolor='0.975')
    button.on_clicked(reset)

    plt.show()
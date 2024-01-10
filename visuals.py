import zmq
import json
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import time
import sys


fig, ax = plt.subplots()
line1, = ax.plot([], label='Ball 1',color='red')
line2, = ax.plot([], label='Ball 2',color='blue')
ax.legend()


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, "")



max_points = 50
time_points = deque(maxlen=max_points)
ball1_y_values = deque(maxlen=max_points)
ball2_y_values = deque(maxlen=max_points)

def update_plot(frame):
    # Set a timeout for receiving messages (in milliseconds)
    timeout = 100

    # Use Poller to check for messages
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    
    # Poll for messages with timeout
    socks = dict(poller.poll(timeout))
    if socket in socks and socks[socket] == zmq.POLLIN:
        message = socket.recv_string()
        data = json.loads(message)

        # Extract data and timestamp
        ball1_y, ball2_y, timestamp = data["ball1_y"], data["ball2_y"], data["timestamp"]
        
        
        '''
        # Record the timestamp when received
        receive_timestamp = time.time()

        # Calculate the delay
        delay = receive_timestamp - timestamp
        '''

        time_points.append(time_points[-1] + 1 if time_points else 0)
        ball1_y_values.append(ball1_y)
        ball2_y_values.append(ball2_y)

        line1.set_xdata(time_points)
        line1.set_ydata(ball1_y_values)
        line2.set_xdata(time_points)
        line2.set_ydata(ball2_y_values)
        ax.relim()
        ax.autoscale_view()
    else:
        print("No message received. Exiting.")
        plt.close()
        sys.exit()

ani = FuncAnimation(fig, update_plot, interval=1)
plt.show()


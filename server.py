import socket
import rospy
from geometry_msgs.msg import Pose

publish = rospy.Publisher('/drone', Pose, queue_size=10)
rospy.init_node('server')
rate = rospy.Rate(60) #max out if needed to 120

print("Trying to connect")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.1.10', 59090)) #computer running motive ip, high port number(must be same on motive computer)
print("connected")

prev = None
name = ""
pos = (0, 0, 0)
rot = (0, 0, 0, 0)

while True:
    stream = sock.recv(1024).decode('utf-8')
    data = stream.split(',')
    if data == "":
        print("No Data")
        rate.sleep()
        continue
    if (len(data) != 8):
        print("invalid data")
        continue
    else:
        name = data[0]
        pos = (float(data[1]), float(data[2]), float(data[3]))
        rot = (float(data[4]), float(data[5]), float(data[6]), float(data[7]))
        if (pos == prev):
            print("no new data")
        prev = pos
        print(pos)
        dronePose = Pose()
        dronePose.position.x = pos[0]
        dronePose.position.y = pos[1]
        dronePose.position.z = pos[2]
        dronePose.orientation.x = rot[0]
        dronePose.orientation.y = rot[1]
        dronePose.orientation.z = rot[2]
        dronePose.orientation.w = rot[3]
        publish.publish(dronePose)
        rate.sleep()

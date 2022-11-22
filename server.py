import socket
import rospy
import std_msgs.msg
from geometry_msgs.msg import PoseStamped

publish = rospy.Publisher('/drone', PoseStamped, queue_size=10)
rospy.init_node('server')
rate = rospy.Rate(60) #max out if needed to 120

print("Trying to connect")


prev = None
name = ""
pos = (0, 0, 0)
rot = (0, 0, 0, 0)
frame = 0
while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('192.168.1.3', 59090)) #computer running motive ip, high port number(must be same on motive computer)
    stream = sock.recv(1024).decode('utf-8')
    data = stream.split(',')
    sock.close()
    if data == "":
        print("No Data")
        rate.sleep()
        continue
    if (len(data) != 8):
        print("invalid data")
        rate.sleep()
        continue
    else:
        name = data[0]
        pos = (float(data[1]), float(data[2]), float(data[3]))
        rot = (float(data[4]), float(data[5]), float(data[6]), float(data[7]))
        if (pos == prev):
            print("no new data")
        prev = pos
        print(pos)
        dronePose = PoseStamped()
        dronePose.pose.position.x = pos[0]
        dronePose.pose.position.y = pos[1]
        dronePose.pose.position.z = pos[2]
        dronePose.pose.orientation.x = rot[0]
        dronePose.pose.orientation.y = rot[1]
        dronePose.pose.orientation.z = rot[2]
        dronePose.pose.orientation.w = rot[3]
        dronePose.header.frame_id = "map"
        dronePose.header.stamp = rospy.Time.now()
        publish.publish(dronePose)
        rate.sleep()

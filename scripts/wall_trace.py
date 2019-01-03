#!/usr/bin/env python
import rospy, copy, math
from pimouse_ros.msg import LightSensorValues
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse

class WallStopAccel():
	def __init__(self):
		self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

		self.sensor_values=LightSensorValues()
		rospy.Subscriber('lightsensors', LightSensorValues, self.callback)

	def callback(self, messages):
		self.sensor_values = messages
			
	def run(self):
		rate = rospy.Rate(20)
		data = Twist()

		accel = 0.01
		
		while not rospy.is_shutdown():
			data.linear.x += 0.02
			s = self.sensor_values 

			if s.sum_forward >= 50: data.linear.x = 0.0
			elif data.linear < 0.1: data.linear.x = 0.1
			elif data.linear >= 0.15: data.linear.x = 0.15

			if data.linear < 0.08: data.angular.z = 0.0
			elif s.left_side < 10: data.angular.z = 0.0
			else:
				target = 50
				error = (target - s.left_side)/50.0
				data.angular.z = error * 20 * math.pi /180.0

			self.cmd_vel.publish(data)
			rate.sleep()

if __name__ == '__main__':
	rospy.init_node('wall_stop_accel')
	rospy.wait_for_service('/motor_on')
	rospy.wait_for_service('/motor_off')
	rospy.on_shutdown(rospy.ServiceProxy('/motor_off', Trigger).call)
	rospy.ServiceProxy('/motor_on', Trigger).call()
	WallStopAccel().run()

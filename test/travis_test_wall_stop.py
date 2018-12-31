#! /usr/bin/evn python

class WallStopTest(unittest.TestCase):
	def set_andget(self,lf,ls,rs,rf):

	def test_io(self):


if __name__ = '__main__':
	time.sleep(3)
	rospy.init_node('travis_test_wall_stop')
	rostest.rosrun('pimouse_run_corridor','travis_test_wall_stop', WallStopTest)

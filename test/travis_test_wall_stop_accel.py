#! /usr/bin/evn python

class WallStopTest(unittest.TestCase):
	def set_and_get(self,lf,ls,rs,rf):
            with open("/dev/rtlighsensor0", "w") as f:
                f.write("%d %d %d %d\n", % (rf, rs, ls, lf))

            time.sleep(0.3)
            
            with open("/dev/rtmotor_raw_l0", "r") as lf,\
                 open("/dev/rtmotor_raw_r0", "r") as rf:
                left = int(lf.readline().rstrip())
                right = int(rf.readline().rstrip())

            return left, right

	def test_io(self):
            left, right = set_and_get(100, 100, 400, 0) #total 600
            self.assertTrue(left == 0 and right == 0, "can't stop")

            left, right = set_and_get(99, 0, 400, 0) #total 499
            self.assertTrue(left != 0 and right != 0, "can't move again")

            left, right = set_and_get(100, 0, 400, 0) #total 500
            self.assertTrue(left == 0 and right == 0, "can't stop")

if __name__ = '__main__':
	time.sleep(3)
	rospy.init_node('travis_test_wall_stop')
	rostest.rosrun('run_corridor','travis_test_wall_stop', WallStopTest)

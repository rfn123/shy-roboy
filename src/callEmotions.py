#!/usr/bin/env python

import rospy
from roboy_control_msgs.srv import ShowEmotion
from std_msgs.msg import Int8
import time


class EmotionReaction(object):
    def __init__(self):
        self.last_publish_time = None
        self.sleep_time_after_execution = 5
        rospy.wait_for_service('/roboy/cognition/face/emotion')
        rospy.init_node('emotion_reaction')
        rospy.Subscriber('shy_roboy/state', Int8, self.process_state)
        self.face_emotion = rospy.ServiceProxy(
            '/roboy/cognition/face/emotion', ShowEmotion)

    def process_state(self, data):
        current_state = data.data

        if current_state in [2, 3]:
            self.call_emotion_service("\"emotion: 'angry'\"")

    def call_emotion_service(self, emotion):
        try:
            if self.last_publish_time is None:
                self.last_publish_time = time.time()
            elif (time.time() - self.last_publish_time) > self.sleep_time_after_execution:
                response = self.face_emotion(emotion)
                print(response)
        except rospy.ServiceException, e:
            print "Service call failed: %s" % e


if __name__ == "__main__":
    er = EmotionReaction()
    rospy.spin()
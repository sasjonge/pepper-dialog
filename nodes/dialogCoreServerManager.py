#!/usr/bin/env python

import socket
import sys
import rospy
import roslib
from std_msgs.msg import String
import subprocess
from naoqi import ALProxy
#Here is a client for core management of dialogue


SELF_CLIENT_SOCKET=''

class DialogCoreClientManager(object):
   def __init__(self):

        #constants to mark begin and end of discussions
        self.TALKSTART=':TALKSTART'
        self.TALKEND=':TALKEND'
        self.INIT   =':INIT'
        self.USERID=0
        rospy.init_node('dialogCoreServerManager')
        rospy.on_shutdown(self.cleanup)
        rospy.loginfo("Starting core server manager node...")
        #read the parameter
        self.CORESERVERIP = rospy.get_param("CORESERVERIP", "localhost")
        self.CORESERVERPORT = int(rospy.get_param("CORESERVERPORT", "1024"))
        self.CORESERVERPATH=rospy.get_param("CORESERVERPATH", "clear")
        self.CORESERVERCWD=rospy.get_param("CORESERVERCWD", "")
        self.PEPPERIP = rospy.get_param("PEPPERIP", "192.168.101.69")
        self.PEPPERPORT = rospy.get_param("PEPPERPORT", "9559") 
        self.ADDR = (self.CORESERVERIP, self.CORESERVERPORT) 
        self.USERNAME= 'user'+str(self.USERID)
        self.BOT=''
        self.DATA_IN=''
        self.DATA_OUT=''
        #Publisher
        self.pub=rospy.Publisher('~coreDialogBus',String,queue_size=1000)
        # Subscriber
        rospy.Subscriber('dialogManager/coreDialogBus', String, self.process)
        #chartscript server
        rospy.loginfo("starting core server Manager ...")
        self.animation = ALProxy("ALAnimationPlayer", self.PEPPERIP, int(self.PEPPERPORT))
        #connection to chatscript server cd BINARIES && ./LinuxChatScript64
        #initalize the dialogue
        #rospy.sleep(10)
        #self.process(String(self.TALKSTART))

  

   def cleanup(self):
        rospy.loginfo("Shutting down core server manager node...")

   def process(self,msg):
        #connection to chatscript server cd BINARIES && ./LinuxChatScript64
        try:
  		    #read request of the user
          if(msg.data==self.TALKSTART):
            self.DATA_IN=':reset'
          else:
            self.DATA_IN=msg.data

          #system's reaction
          self.DATA_OUT = self.DATA_IN
          rospy.loginfo('before*********************')
          rospy.loginfo(self.DATA_IN)
          if(self.DATA_OUT =='dance'):
            self.animation.run("animations/Stand/Gestures/Hey_1")

          #publish reaction
          self.pub.publish(String(self.DATA_OUT))
          #change user
          if(msg.data==self.TALKSTART):
            self.USERID+=1
            self.USERNAME= 'user'+str(self.USERID)

          #print Inputs and Outputs of core system manager

          rospy.loginfo('CORE SERVER INPUT: '+self.DATA_IN) 
          rospy.loginfo('CORE SERVER OUTPUT: '+self.DATA_OUT)

        except:
          rospy.loginfo('Error occured!!!'+str(self.ADDR))  
		  

if __name__=="__main__":
    try:
        DialogCoreClientManager()
        rospy.loginfo('We came here')
        rospy.spin()
    except:
        e = sys.exc_info()[0]
        rospy.loginfo("Danger: An ERROR ocurred: %s" % e)

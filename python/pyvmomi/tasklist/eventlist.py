#!/usr/bin/python

"""
Python program for listing recent vCenter tasks in a very basic way
"""

from optparse import OptionParser, make_option
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vmodl

import pyVmomi
import textwrap
import argparse
import atexit
import time
import math
import sys
import os
import MySQLdb

def GetArgs():
   """
   Supports the command-line arguments listed below.
   """
   parser = argparse.ArgumentParser(description='Process args for retrieving all the Virtual Machines')
   parser.add_argument('-s', '--host', required=True, action='store', help='Remote host to connect to')
   parser.add_argument('-o', '--port', default=443,   action='store', help='Port to connect on')
   parser.add_argument('-u', '--user', required=True, action='store', help='User name to use when connecting to host')
   parser.add_argument('-p', '--password', required=True, action='store', help='Password to use when connecting to host')
   args = parser.parse_args()
   return args

def main():
   """
   Simple command-line program for listing the virtual machines on a system.
   """

   args = GetArgs()
   try:
      si = None
      try:
         si = SmartConnect(
            host  = args.host,
            user  = args.user,
            pwd   = args.password,
            port  = int(args.port)
         )
      except IOError, e:
        pass
      if not si:
         print "Could not connect to the specified host using given credentials"
         return -1

      atexit.register(Disconnect, si)

      # fetch the terminal columns
      rows, columns = os.popen('stty size', 'r').read().split()

      # Calculating Terminal width to adjust columns size
      columns = int(columns) - 12 # remove the formatting layout size

      # The calculations here, reflect my personal preferences, you might need
      # to adapt for yours :-)
      timeSize          = math.trunc(float(columns)/100*1.0)
      userSize          = math.trunc(float(columns)/100.0*11.0)
      entityNameSize    = math.trunc(float(columns)/100.0*40.0)
      descriptionSize   = math.trunc(float(columns)/100.0*30.0)
      stateSize         = math.trunc(float(columns)/100.0*1.0) 

      # Formatting Columns
      formatColumns     =  "%" + str(timeSize) + \
                           "s | %" + str(userSize) + \
                           "s | %" + str(entityNameSize) + \
                           "s | %" + str(descriptionSize) + \
                           "s | %" + str(stateSize) + \
                           "s" 

      lastTask = None

      content = si.RetrieveContent()
      while True:
        event = content.eventManager.latestEvent:
        try:
           if lastTask != event.chainId
                lastTask = taskNum

                # print the task information
                print formatColumns % (
                   str(task.info.startTime).split(".")[0],
                   task.info.reason.userName,
                   task.info.entityName,
                   task.info.descriptionId,
                   task.info.state
                )
                starttime =  str(task.info.startTime).split(".")[0]
                username = task.info.reason.userName
                entityname = task.info.entityName
                descriptionid = task.info.descriptionId
                state = task.info.state

                db = MySQLdb.connect("localhost","root","","tech" )
                sql = "INSERT INTO task (task_startTime, task_userName, task_entityName, task_descriptionId, task_state) VALUES (%s, %s, %s, %s, %s)"
                cursor = db.cursor()
                cursor.execute(sql,(starttime, username, entityname, descriptionid, state))
                db.close()
            
        except Exception, x:
                do = "nothing"

        time.sleep(1)

   except vmodl.MethodFault, e:
      print "Caught vmodl fault : " + e.msg
      return -1
   except Exception, e:
      print "Caught exception : " + str(e)
      return -1

   return 0

# Start program
if __name__ == "__main__":
   main()

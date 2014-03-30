# -*- coding:utf-8 -*-

from optparse import OptionParser, make_option
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vmodl

import argparse
import atexit
import sys
import pyVmomi

class VMware:

	def GetArgs(self):
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

	def GetVmInfo(self,vminfos,vm):
	   """
	   Print information for a particular virtual machine.
	   """
	   summary = vm.summary
	   vminfo = {}
	   vminfo["name"] = summary.config.name
	   vminfo["vmPathName"] = summary.config.vmPathName
	   vminfo["instanceUuid"] = summary.config.instanceUuid
	   vminfo["numCpu"] = summary.config.numCpu
	   vminfo["memorySizeMB"] = summary.config.memorySizeMB
	   for device in vm.config.hardware.device:
	      if device.deviceInfo.summary == 'VLAN 12':
	         vminfo["macAddress"] = device.macAddress
	   vminfos.append(vminfo)


	def getvm(self):
	   """
	   Simple command-line program for listing the virtual machines on a system.
	   """

	   args = GetArgs()
	   try:
	      si = None
	      try:
	         si = SmartConnect(host=args.host,
	                user=args.user,
	                pwd=args.password,
	                port=int(args.port))
	      except IOError, e:
	        pass
	      if not si:
	         print "Could not connect to the specified host using specified username and password"
	         return -1

	      atexit.register(Disconnect, si)

	      content = si.RetrieveContent()
	      datacenter = content.rootFolder.childEntity[0]
	      vmFolder = datacenter.vmFolder
	      vmList = vmFolder.childEntity
	      vminfos = []
	      for target in vmList:
	         if type(target) == pyVmomi.types.vim.Folder:
	            vms = target.childEntity
	            for vm in vms:
	               GetVmInfo(vminfos, vm)
	         else:
	            vm = target
	            GetVmInfo(vminfos, vm)
	   except vmodl.MethodFault, e:
	      print "Caught vmodl fault : " + e.msg
	      return -1
	   except Exception, e:
	      print "Caught exception : " + str(e)
	      return -1

	   return 0

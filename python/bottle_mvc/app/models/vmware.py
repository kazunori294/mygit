# -*- coding:utf-8 -*-

from optparse import OptionParser, make_option
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vmodl, vim

import argparse
import atexit
import sys
import pyVmomi

class VMware:

        def getvm(self):
           """
           Simple command-line program for listing the virtual machines on a system.
           """

           #args = GetArgs()
           try:
              si = None
              try:
                 #si = SmartConnect(host=args.host,
                 #       user=args.user,
                 #       pwd=args.password,
                 #       port=int(args.port))
                 si = SmartConnect(host='vc.kazu.linux',
                        user='root',
                        pwd='51SdlQ#A',
                        port=443)
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
		           summary = vm.summary
		           vminfo = {}
		           vminfo["name"] = summary.config.name
		           vminfo["vmPathName"] = summary.config.vmPathName
		           vminfo["instanceUuid"] = summary.config.instanceUuid
		           vminfo["numCpu"] = summary.config.numCpu
		           vminfo["memorySizeMB"] = summary.config.memorySizeMB
			   vminfo["powerState"] = vm.runtime.powerState
                           vminfo["ipAddress"] = vm.guest.ipAddress
		           for device in vm.config.hardware.device:
		              if device.deviceInfo.summary == 'VLAN 12':
		                 vminfo["macAddress"] = device.macAddress
		           vminfos.append(vminfo)
                 else:
                           vm = target
		           summary = vm.summary
		           vminfo = {}
		           vminfo["name"] = summary.config.name
		           vminfo["vmPathName"] = summary.config.vmPathName
		           vminfo["instanceUuid"] = summary.config.instanceUuid
		           vminfo["numCpu"] = summary.config.numCpu
		           vminfo["memorySizeMB"] = summary.config.memorySizeMB
                           vminfo["powerState"] = vm.runtime.powerState
                           vminfo["ipAddress"] = vm.guest.ipAddress
		           for device in vm.config.hardware.device:
		              if device.deviceInfo.summary == 'VLAN 12':
		                 vminfo["macAddress"] = device.macAddress
		           vminfos.append(vminfo)

           except vmodl.MethodFault, e:
              print "Caught vmodl fault : " + e.msg
              return -1
           except Exception, e:
              print "Caught exception : " + str(e)
              return -1

           return vminfos

####################################################################
        def clonevm(self, params):

	   try:
	      si = None
	      try:
	         si = SmartConnect(host='vc.kazu.linux',
	                user='root',
	                pwd='51SdlQ#A',
	                port=443)
	      except IOError, e:
	        pass
	      if not si:
	         print "Could not connect to the specified host using specified username and password"
	         return -1

	      atexit.register(Disconnect, si)

              content = si.RetrieveContent()
	      obj_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.VirtualMachine],True)
	      vm_list = obj_view.view
              for vm in vm_list:
		 if vm.name == 'Template-CentOS-64bit':
                    template_vm = vm

	      # Creating relocate spec and clone spec
	      relocateSpec = vim.vm.RelocateSpec()
	      cloneSpec = vim.vm.CloneSpec(powerOn=False,template=False,location=relocateSpec)

	      # Creating clone task
	      vmname = params["vmname"]
              clonetask = template_vm.Clone(name=vmname,folder=template_vm.parent,spec=cloneSpec)

	   except Exception, e:
	      print "Caught exception : " + str(e)
	      return -1

	   return 0


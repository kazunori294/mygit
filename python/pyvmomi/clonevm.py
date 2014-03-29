#!/usr/bin/python
# VMware vSphere Python SDK
# Copyright (c) 2008-2013 VMware, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Python program for listing the vms on an ESX / vCenter host
"""

from optparse import OptionParser, make_option
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vmodl, vim

import argparse
import atexit
import sys
import time

template_name = "Template-CentOS-64bit"

def GetArgs():
   """
   Supports the command-line arguments listed below.
   """
   parser = argparse.ArgumentParser(description='Process args for retrieving all the Virtual Machines')
   parser.add_argument('-s', '--host', required=True, action='store', help='Remote host to connect to')
   parser.add_argument('-o', '--port', default=443,   action='store', help='Port to connect on')
   parser.add_argument('-u', '--user', required=True, action='store', help='User name to use when connecting to host')
   parser.add_argument('-p', '--password', required=True, action='store', help='Password to use when connecting to host')
   parser.add_argument('-n', '--vmname', required=True, action='store', help='Name to be created')
   args = parser.parse_args()
   return args


def find_vm(si,name):
   """
   Find original vm for clone
   """
   content = si.RetrieveContent()
   obj_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.VirtualMachine],True)
   vm_list = obj_view.view

   for vm in vm_list:
      if vm.name == name:
         return vm
   return None



def WaitTask(task, actionName='job', hideResult=False):
    """
    Waits and provides updates on a vSphere task
    """
    while task.info.state == vim.TaskInfo.State.running:
       time.sleep(2)
    
    if task.info.state == vim.TaskInfo.State.success:
       if task.info.result is not None and not hideResult:
          out = '%s completed successfully, result: %s' % (actionName, task.info.result)
       else:
          out = '%s completed successfully.' % actionName
    else:
       out = '%s did not complete successfully: %s' % (actionName, task.info.error)
       raise task.info.error # should be a Fault... check XXX
    
    # may not always be applicable, but can't hurt.
    return task.info.result

def GetVmInfo(vm):
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
      if device.key == 4000:
         vminfo["macAddress"] = device.macAddress
   print vminfo

def main():
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

      template_vm = find_vm(si,template_name)

      # Creating relocate spec and clone spec
      relocateSpec = vim.vm.RelocateSpec()
      cloneSpec = vim.vm.CloneSpec(powerOn=False,template=False,location=relocateSpec)

      # Creating clone task
      clonetask = template_vm.Clone(name=args.vmname,folder=template_vm.parent,spec=cloneSpec)
      result = WaitTask(clonetask, 'VM clone task')
      GetVmInfo(find_vm(si,args.vmname))

   except Exception, e:
      print "Caught exception : " + str(e)
      return -1

   return 0

# Start program
if __name__ == "__main__":
   main()

#!/usr/bin/env python
"""This Alert-Script sends a triggered push-warning to a Growl-Client
Note: Its modified to cut the relevant part from the warning and currently works for Sensor-Removed and Temperature-Threshold-Breach
Zabbix can call different alert scripts for different types of push-warnings. Or a modification of the script scans the push-warning of its type and 
filters the relevant parts
Original Version of the script: http://lab4.org/files/growlmessage.py.txt """ 

import gntp.notifier

def cutInformation(raw_info):
     info =str(raw_info).rfind("Value")
     info =raw_info[(info-8):]  
     return info
    
growl = gntp.notifier.GrowlNotifier(
    applicationName      = "Zabbix",
    notifications        = ["Disaster","High","Average","Warning","Information","Unknown"],
    defaultNotifications = ["Unknown"],
    hostname             = sys.argv[1], 

)
try:
    growl.register()
except:
    print "Sending growl message to "+sys.argv[1]+" failed"
    return 1

confirmation = growl.notify(
	    noteType = "High",
	    title = sys.argv[2],
	    description = cutInformation(sys.argv[3]),
	    sticky = False,
	    priority = 1,
    )

if confirmation == True:
    print "Message sent"
    return 0
else:
    print "Sending growl message to "+sys.argv[1]+" failed. "+str(confirmation)
    
    return 1

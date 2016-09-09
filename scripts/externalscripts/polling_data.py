#!/usr/bin/env python
from pyZabbixSender import pyZabbixSender
import json
from easysnmp import Session
"""This SNMP-Polling-Script acts like an SNMP-Manager and polls data from the agent of a Monitoring-Client and transmitts the data to zabbix"""

def push_status_data_to_zabbix(data,host):
    timestamp=0
    z = pyZabbixSender("localhost")
    for item in data:
        for attribute, value in item.iteritems():
                z.addData("monitoring_client_1", attribute,value)
    results = z.sendData()
    

def push_sensor_data_to_zabbix(data,host):
    timestamp=0
    for item in data:
        try:
           timestamp=item['time']
        except:
            pass
    z = pyZabbixSender('localhost')
    for item in data:
        for attribute, value in item.iteritems():
            if attribute != 'time':
                z.addData(host, attribute,value,timestamp)

    results = z.sendData()
    
    

    

if __name__ == "__main__":
        
        """Using SNMP-Bulk-Request to fetch all data into one Request"""   
        session = Session(hostname='10.0.0.22', community='public', version=2)
        try:
           oid_list =['.1.3.6.1.4.1.8072.9999.9999.1','.1.3.6.1.4.1.8072.9999.9999.2']
           response_snmp = session.get_bulk(oid_list,200,200)
        
        #Iterate through SNMP-Response and push data to zabbix-sender, which will transmitt the data to zabbix
           for item in response_snmp:
                #Check for status data
                if item.oid=='iso.3.6.1.4.1.8072.9999.9999.1':
                    push_status_data_to_zabbix(json.loads(str(item.value)),'monitoring_client_1')
                else:
                    push_sensor_data_to_zabbix(json.loads(str(item.value)),'monitoring_client_1')
                
           print 0 
        except:
           print 1
            
           
    

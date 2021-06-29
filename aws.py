#!/usr/bin/python3
import boto3
import time




res=boto3.resource('ec2')
clnt=boto3.client('ec2')
inst=res.Instance('i-08731b77caf284d34')

stat=inst.state['Name']


if stat=='running':
        inst.stop()
        clnt.get_waiter('instance_stopped')
        print(f"instance id {inst.id} is now in {inst.state['Name']} state" )
else:
        print("Already in stopped State")

time.sleep(30)
response = clnt.modify_instance_attribute(InstanceId = 'i-08731b77caf284d34',InstanceType={'Value': 't2.medium'})
clnt.get_waiter('system_status_ok')


if inst.state['Name']=='stopped':
        inst.start()
        clnt.get_waiter('instance_running')
        print(f"instance id {inst.id} is now in {inst.state['Name']} state" )
else:
        print("Something went wrong")

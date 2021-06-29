#!/usr/bin/python3
import boto3
import time
import sys

res=boto3.resource('ec2')
clnt=boto3.client('ec2')
inst=res.Instance(sys.argv[1])

stat=inst.state['Name']


if stat=='running':
        inst.stop()
        clnt.get_waiter('instance_stopped')
        print(f"instance id {inst.id} is now in {inst.state['Name']} state" )
else:
        print("Already in stopped State")

time.sleep(30)
response = clnt.modify_instance_attribute(InstanceId = sys.argv[1],InstanceType={'Value': sys.argv[2]})
clnt.get_waiter('system_status_ok')


if inst.state['Name']=='stopped':
        inst.start()
        clnt.get_waiter('instance_running')
        print(f"instance id {inst.id} is now in {inst.state['Name']} state" )
else:
        print("Something went wrong")

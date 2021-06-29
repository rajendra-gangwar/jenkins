#!/usr/bin/python3
import boto3
import time
import sys, os


res=boto3.resource('ec2')
clnt=boto3.client('ec2')
inst=res.Instance(sys.argv[1])
stat=inst.state['Name']

print("Checking if EC2 Instance is Running")
if stat=='running':
        print("Stopping Running Instance")
        inst.stop()
        clnt.get_waiter('instance_stopped')
        stat=inst.state['Name']
        print(f"instance id {inst.id} is now in {inst.state['Name']} state" )
else:
        print("Already in stopped State")

print("Changing the instance type to ",sys.argv[2])
time.sleep(60)
response = clnt.modify_instance_attribute(InstanceId = sys.argv[1],InstanceType={'Value': sys.argv[2]})
#clnt.get_waiter('system_status_ok')
time.sleep(10)
printf("Starting the Instance")


response = client.start_instances(InstanceIds=[sys.argv[2]], AdditionalInfo='string', DryRun=False)

print(response)

'''inst.start()
clnt.get_waiter('instance_running')
        print(f"instance id {inst.id} is now in {inst.state['Name']} state" )
else:
        print("Something went wrong")
'''

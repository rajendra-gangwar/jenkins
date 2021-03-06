#!/usr/bin/python3
import boto3
import time
import sys


res=boto3.resource('ec2')
clnt=boto3.client('ec2')


file=open('currtype.txt','r')
inst_type=file.read()
file.close()

file=open('currentid.txt','r')
inst_id=file.read()
file.close()

inst=res.Instance(inst_id)
stat=inst.state['Name']

print("Checking if EC2 Instance is Running")
if stat=='running':
    print("Stopping Running Instance")
    response = clnt.stop_instances(InstanceIds=[inst_id,], DryRun=False)
    print(response)
    stopped_instance_waiter = clnt.get_waiter('instance_stopped')
    stopped_instance_waiter.wait(InstanceIds=[inst_id,])
    
else:
        print("Already in stopped State")

print("Changing the instance type to ",inst_type)

response = clnt.modify_instance_attribute(InstanceId = inst_id,InstanceType={'Value': inst_type})
print("Sleep 10 sec")
time.sleep(10)
print(response)

print("Starting the Instance")       
       
response = clnt.start_instances(InstanceIds= [inst_id,], AdditionalInfo='string', DryRun=False)
print(response)

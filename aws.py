#!/usr/bin/python3
import boto3
import time
import sys, os


res=boto3.resource('ec2')
clnt=boto3.client('ec2')
inst=res.Instance(sys.argv[1])
stat=inst.state['Name']

print("Checking current InstanceType")
response = clnt.describe_instance_attribute(Attribute='instanceType', DryRun=False, InstanceId=sys.argv[1])
currentinst=response['InstanceType']['Value']

file=open('currtype.txt','w')
file.write(currentinst)
file.write("\n")
file.close()

    
print("Checking if EC2 Instance is Running")
if stat=='running':
    print("Stopping Running Instance")
    response = clnt.stop_instances(InstanceIds=[sys.argv[1],], DryRun=False)
    clnt.get_waiter('instance_stopped')
    print(response)
    print(f"instance id {inst.id} is now in {inst.state['Name']} state" )
    print("Sleeping for 60 sec")
    time.sleep(60)
else:
        print("Already in stopped State")

print("Changing the instance type to ",sys.argv[2])

response = clnt.modify_instance_attribute(InstanceId = sys.argv[1],InstanceType={'Value': sys.argv[2]})
print("Sleep 10 sec")
time.sleep(10)
print(response)

print("Starting the Instance")       
       
response = clnt.start_instances(InstanceIds= [sys.argv[1],], AdditionalInfo='string', DryRun=False)
print(response)

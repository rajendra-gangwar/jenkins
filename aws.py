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

'''if currentinst==sys.argv[2]:
    print("No change in instance type")
    break
else:'''
os.environ["beforechange"] = currentinst
print("Current instance type is", currentinst)

print("Checking if EC2 Instance is Running")
if stat=='running':
    print("Stopping Running Instance")
    try:
        response = ec2.stop_instances(InstanceIds=sys.argv[1], DryRun=False)
        clnt.get_waiter('instance_stopped')
        print(response)
    except ClientError as e:
        print(e)
        
    stat=inst.state['Name']
    print(f"instance id {inst.id} is now in {inst.state['Name']} state" )
    time.sleep(60)
else:
        print("Already in stopped State")

print("Changing the instance type to ",sys.argv[2])

try:
   response = clnt.modify_instance_attribute(InstanceId = sys.argv[1],InstanceType={'Value': sys.argv[2]})
#clnt.get_waiter('system_status_ok')
   print("Sleep 60")
   time.sleep(10)
   print(response)
   
except ClientError as e:
        print(e)

print("Starting the Instance")       
try:        
 
    response = clnt.start_instances(InstanceIds=[sys.argv[1]], AdditionalInfo='string', DryRun=False)
    print(response)
except ClientError as e:
        print(e)

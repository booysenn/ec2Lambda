#!/usr/bin/env python
#title           :tagEC2Instances.py
#description     :AWS Lambda python script to tag instances in all regions with 			
#                 "LambdaStop" and "LambdaStart" tags, both set to "false". This 
#                 is to make it easier to modify only those needing to auto stop start
#author          :booysenn
#date            :20160916
#version         :0.1
#usage           :copy to Lambda function. Can trigger with Cloudwatch schedule
#notes           :Execution time 13 seconds
#==============================================================================import boto3

def lambda_handler(event, context):

    ec2 = boto3.client('ec2')
    regions = ec2.describe_regions()
	#Run sccript in each EC2 region
    for region in regions['Regions']:
        ec2b = boto3.client('ec2', region_name=region['RegionName'])
        response = ec2b.describe_instances()
        tagStartInstances = []
        tagStopInstances = []
        for res in response['Reservations']:
            for inst in res['Instances']:
                addLambdaStart = "inst['InstanceId']"
                addLambdaStop = "inst['InstanceId']"
                #Loop through tags and add instances withpout ec2Lambda tags to "startInstances" in order to add tags
                for tag in inst['Tags']:
                    #if tag matches do not add to list. We do not need to add it again
                    if tag['Key'] == "LambdaStart":
                        addLambdaStart = None
                    if tag['Key'] == "LambdaStop":
                        addLambdaStop = None
                if addLambdaStart is not None:
                    tagStartInstances.append(inst['InstanceId'])
                if addLambdaStop is not None:
                    tagStopInstances.append(inst['InstanceId'])
		#Add LambdaStart tags
		if tagStartInstances:
            ec2b.create_tags(Resources=tagStartInstances,Tags=[{'Key': 'LambdaStart','Value': 'false'}])
		#Add LambdaStop tags
        if tagStopInstances:
            ec2b.create_tags(Resources=tagStopInstances,Tags=[{'Key': 'LambdaStop','Value': 'false'}])
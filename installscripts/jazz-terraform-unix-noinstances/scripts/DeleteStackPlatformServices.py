#!/usr/bin/python
import json
import sys
import subprocess
import os
import os.path


def checkCFServiceAvailable(servicename):
    return subprocess.call(
        "aws cloudformation list-stack-resources --stack-name " + servicename,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)


def deleteCFService(servicename):
    return subprocess.call(
        "aws cloudformation delete-stack --stack-name " + servicename,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)


#return subprocess.call("aws cloudformation list-stack-resources --stack-name " + servicename, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def getServicesList():
    return subprocess.call(
        'aws cloudformation list-stacks --stack-status-filter "CREATE_IN_PROGRESS" "CREATE_FAILED" "CREATE_COMPLETE" "UPDATE_IN_PROGRESS" "UPDATE_COMPLETE" >> listservice.json',
        shell=True)


def deleteCloudFormationService(service_name):
    return_code = checkCFServiceAvailable(service_name)
    if return_code == 0:
        print("Service::" + service_name +
              ": exists. Service deletion started.........")
        delete_return_code = deleteCFService(service_name)
        if delete_return_code == 0:
            print("\tSuccessfully deleted service " + service_name)
        else:
            print("\tError while deleting service " + service_name +
                  " errorcode=" + delete_return_code)
    else:
        print('Error service not found::' + service_name)


if (len(sys.argv) != 3):
    print(
        "Error - Please provide Argument1='stack name' and Argument1='Delete Client servies option true or false' "
    )
    print("Argument1=<StackName> Argument2=<true/false>")
    exit(1)

print(str(sys.argv))

stackName = sys.argv[1].lower() + "-"
deleteClientServices = sys.argv[2]

if (deleteClientServices.lower() != 'true'):
    exit(0)

print("\r\nStarting deletion of micro services\r\n\r\n")

## Delete user services Cloud formations
fname = 'listservice.json'
if os.path.isfile(fname):
    os.remove(fname)

valresp = getServicesList()
if (valresp != 0):
    exit(1)

jsonFile = open(fname, 'r')
values = json.load(jsonFile)
jsonFile.close()

ss = values['StackSummaries']

spLen = len(stackName)

inval = 0
for item in ss:
    if (item['StackName'].startswith(stackName)):
         deleteCloudFormationService(item['StackName'])

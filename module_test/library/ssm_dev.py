#!/usr/bin/python

from __future__ import print_function
import boto3,time
from sys import exit
from ansible.module_utils.basic import *


def main():
    module_args = {
        'document_name':{'type':'str','required':True},
        'region':{'type':'str','required':True}
    }

    module = AnsibleModule(
        argument_spec=module_args
    )

    client = boto3.client('ssm',region_name =  module.params['region'])
    
    response = client.start_automation_execution(
    DocumentName='EC2Test',
    DocumentVersion='2',
    Parameters={
        'AMIID': ['ami-ff4ea59d'],
        'InstanceType': ['t2.micro'] 
        },
    Mode='Auto'
    )

    execution_id = response['AutomationExecutionId']
    
    error = 0
    
    while True:
        checker = client.describe_automation_executions(
            Filters=[
                {
                    'Key': 'ExecutionId',
                    'Values': [execution_id]
                },
                ]
            )
        checker = checker['AutomationExecutionMetadataList'][0]['AutomationExecutionStatus']
        if checker in ['InProgress','Waiting','Cancelling']:
            time.sleep(10)
        elif checker  == 'Pending':
            pass
        elif checker == 'Cancelled':
            system.exit('execution stopped!')
        elif checker  == 'Success':
            print ('execution successful')
            break
        else:
            error = 1
            break
      
    if error:
        print ("execution error!")
        sys.exit(0)

    execution_result = client.describe_automation_executions(
        Filters=[
            {
            'Key': 'ExecutionId',
            'Values': [execution_id]
            },
        ]
    )

    response = execution_result['AutomationExecutionMetadataList'][0]['Outputs']
    module.exit_json(changed=False, meta=response)

if __name__ == '__main__':
    main()



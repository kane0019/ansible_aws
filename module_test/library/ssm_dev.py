#!/usr/bin/python

import boto3,time
from ast import literal_eval
from sys import exit
from ansible.module_utils.basic import *


def main():
    # initial module with input "document_name" & "region"
    module_args = {
        'aws_access_key':{'type':'str','required':False,'default': None},
        'aws_secret_key':{'type':'str','required':False,'default': None},
        'security_token':{'type':'str','required':False,'default': None},
        'document_name':{'type':'str','required':True},
        'document_version':{'type':'str','required':False},
        'document_parameters':{'type':'str','required':False},
        'region':{'type':'str','required':True}
    }

    module = AnsibleModule(
        argument_spec=module_args
    )

    # call boto to retreive ssm client
    client = boto3.client('ssm', aws_access_key_id = module.params['aws_access_key'], aws_secret_access_key = module.params['aws_secret_key'], aws_session_token = module.params['security_token'], region_name =  module.params['region'])
    
    # start ssm_automation execution
    response = client.start_automation_execution(
            DocumentName = module.params['document_name'],
            Parameters = literal_eval(module.params['document_parameters']),
            Mode='Auto'
    )

    # get execution ID
    execution_id = response['AutomationExecutionId']
    
    
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
            break
        else:
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
    module.exit_json(changed=True, meta=response)

if __name__ == '__main__':
    main()




#Instance Template

COMPUTE = 'https://www.googleapis.com/compute/v1'

def GenerateConfig(context):

    project = '/projects/' + context.properties['project']
   
    resources = [{
        'name': context.env['name'], 
        'type': 'compute.v1.instanceTemplate', 
        'properties': {
            'project': ''.join([COMPUTE, project]),
            #Instance Template contains 'properties' nested within 'properties'
            'properties': {
                'machineType': context.properties['machineType'],
                'networkInterfaces':[{
                    'network': context.properties['network'],
                    'accessConfigs': [{
                        'name': 'External NAT',
                        'type': 'ONE_TO_ONE_NAT'
                    }]#end accessConfigs
                }],#end networkInterfaces
                'tags': {
                        'items': ['swarm-cluster']
                },
                'metadata': {
                'items': [{
                        'key':'swarm-origin-ip', #swarm needs manager network ip to join
                        'value': '$(ref.' + context.env['deployment'] + '-origin-mgr1.networkInterfaces[0].networkIP)'
                    },{
                    'key': 'startup-script',
                    'value':'''#! /bin/bash
sudo apt-get update && sudo apt-get --only-upgrade install -y kubectl google-cloud-sdk google-cloud-sdk-datastore-emulator google-cloud-sdk-pubsub-emulator google-cloud-sdk-app-engine-go google-cloud-sdk-app-engine-java google-cloud-sdk-app-engine-python google-cloud-sdk-cbt google-cloud-sdk-bigtable-emulator google-cloud-sdk-datalab
curl -fsSL get.docker.com -o get-docker.sh
sh get-docker.sh
MANAGER_IP=$(curl "http://metadata/computeMetadata/v1/instance/attributes/swarm-origin-ip" -H "Metadata-Flavor: Google")
WORKER_TOKEN=$(curl "http://metadata/computeMetadata/v1/project/attributes/workerToken" -H "Metadata-Flavor: Google")
sudo docker swarm join --token $WORKER_TOKEN $MANAGER_IP:2377
ZONE=$(curl "http://metadata/computeMetadata/v1/instance/zone" -H "Metadata-Flavor: Google")
#TO REMOVE EXTERNAL IP IF NECESSARY
#gcloud compute instances delete-access-config $(hostname) --access-config-name="External NAT" --zone=$ZONE
'''
                    }]
                },#end metadata
                'serviceAccounts': [{
                    'email': 'default',
                        'scopes': [
                            'https://www.googleapis.com/auth/devstorage.read_write', 
                            'https://www.googleapis.com/auth/logging.write',
                            'https://www.googleapis.com/auth/monitoring.write',
                            'https://www.googleapis.com/auth/servicecontrol',
                            'https://www.googleapis.com/auth/service.management.readonly',
                            'https://www.googleapis.com/auth/compute',
                            'https://www.googleapis.com/auth/cloud-platform'
                        ]
                }],
                'disks': [{
                    'boot': True,
                    'type': 'PERSISTENT',
                    'autoDelete': True,
                    'index': 0,
                    'interface': 'SCSI',
                    'mode': 'READ_WRITE',
                    'initializeParams':{
                        'name': context.env['name'] + '-boot',
                        'sourceImage': context.properties['sourceImage'],
                        'diskType': 'pd-ssd',
                        'diskSizeGb': 10
                    }#end initializeParams
                },{
                    'boot': False,
                    'type': 'PERSISTENT',
                    'autoDelete': True,
                    'index': 1,
                    'interface': 'SCSI',
                    'mode': 'READ_WRITE',
                    'initializeParams':{
                        'diskName': context.env['name'] + '-data',
                        'sourceImage':context.properties['sourceImage'],
                        'diskType': 'pd-standard',
                        'diskSizeGb': 500
                    }#end initializeParams
                }],#end disk 
            }#end inner properties
        }#end properties
    }]#end resources

    return {'resources': resources}

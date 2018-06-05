#Instance Template

COMPUTE = 'https://www.googleapis.com/compute/v1'

def GenerateConfig(context):

    project = '/projects/' + context.properties['project']
    zone = '/zones/' + context.properties['zone']
    machinetype = '/machineTypes/' + context.properties['machineType']

    resources = [{
        'name': context.env['name'], 
        'type': 'compute.v1.instance', 
        'properties': {
            'project': ''.join([COMPUTE, project]),
            'zone': context.properties['zone'],
            'machineType': ''.join([COMPUTE, project, zone, machinetype]),
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
                   'key': 'startup-script-status',
                   'value': 'pending' #startup script will change this to 'finished' when done running
                },{
                   'key': 'startup-script',
                   'value':'''#! /bin/bash
        sudo apt-get update && sudo apt-get --only-upgrade install -y kubectl google-cloud-sdk google-cloud-sdk-datastore-emulator google-cloud-sdk-pubsub-emulator google-cloud-sdk-app-engine-go google-cloud-sdk-app-engine-java google-cloud-sdk-app-engine-python google-cloud-sdk-cbt google-cloud-sdk-bigtable-emulator google-cloud-sdk-datalab
        curl -fsSL get.docker.com -o get-docker.sh
        sh get-docker.sh
        sleep 5
        sudo docker swarm init
        gcloud compute project-info add-metadata --metadata workerToken=$(sudo docker swarm join-token -q worker),managerToken=$(sudo docker swarm join-token -q manager)
        ZONE=$(curl "http://metadata/computeMetadata/v1/instance/zone" -H "Metadata-Flavor: Google")
        gcloud compute instances add-metadata $(hostname) --metadata startup-script-status=finished --zone=$ZONE
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
                    'diskType': ''.join([COMPUTE, project, zone, '/diskTypes/pd-ssd']),
                    'diskSizeGb': 10
                }#end initializeParams
            },{
                'boot': False,
                'type': 'PERSISTENT',
                'autoDelete': True, #CHANGE THIS TO FALSE IF USING AS DATA STORAGE
                'index': 1,
                'interface': 'SCSI',
                'mode': 'READ_WRITE',
                'initializeParams':{
                    'diskName': context.env['name'] + '-data',
                    'sourceImage':context.properties['sourceImage'],
                    'diskType': ''.join([COMPUTE, project, zone, '/diskTypes/pd-standard']),
                    'diskSizeGb': 500
                }#end initializeParams
            }],#end disk 
        }#end properties
    }]#end resources

    return {'resources': resources}

#Top-level template
#Contains: Instance, Worker Instance, Other Firewall

def GenerateConfig(context):

    resources = [{
        'name': context.env['deployment'] + '-origin-mgr1', 
        'type': 'swarm-manager-origin.py', 
        'properties':{
            'project': context.properties['project'],
            'zone': context.properties['zone'],
            'network': context.properties['network'],
            'machineType': context.properties['machine_type'],
            'sourceImage': context.properties['sourceImage']
        }
    },{
        'name': context.env['deployment'] + '-manager-it',
        'type': 'swarm-manager-instance.py',
        'properties':{
            'project': context.properties['project'],
            'network': context.properties['network'],
            'machineType': context.properties['machine_type'],
            'sourceImage': context.properties['sourceImage']
        }
    },{
        'name': context.env['deployment'] + '-manager-group-manager',
        'type': 'manager-group-manager.py',
        'properties':{
            'project': context.properties['project'],
            'network': context.properties['network'],
            'machineType': context.properties['machine_type'],
            'sourceImage': context.properties['sourceImage'],
            'targetSize': context.properties['target_size'],
            'region': context.properties['region']
        }
    },{
        'name': context.env['deployment'] + '-worker-it',
        'type': 'swarm-worker-instance.py',
        'properties':{
            'project': context.properties['project'],
            'network': context.properties['network'],
            'machineType': context.properties['machine_type'],
            'sourceImage': context.properties['sourceImage']
        }
    },{
        'name': context.env['deployment'] + '-worker-group-manager',
        'type': 'worker-group-manager.py',
        'properties':{
            'project': context.properties['project'],
            'network': context.properties['network'],
            'machineType': context.properties['machine_type'],
            'sourceImage': context.properties['sourceImage'],
            'targetSize': context.properties['target_size'],
            'region': context.properties['region']
        }
    },{
        'name': context.env['deployment'] + '-tcp-udp-firewall',
        'type': 'swarm-firewall.py',
        'properties':{
            'network': context.properties['network']
        }
    }]

    return {'resources': resources}

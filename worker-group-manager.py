#Group Manager

def GenerateConfig(context):

    workerTemplate = '$(ref.' + context.env['deployment'] + '-worker-it.selfLink)'    

    resources = [{
        'name': context.env['name'], #takes name from top-template
        'type': 'compute.v1.regionInstanceGroupManager',
        'properties': {
            'project': context.properties['project'],
            'region': context.properties['region'],
            'targetSize': context.properties['targetSize'], #number of instances to be maintained
            'baseInstanceName': context.env['deployment'] + '-worker',
            'instanceTemplate': workerTemplate,
            'versions':[{
                'instanceTemplate': workerTemplate,
                'targetSize':{
                    'fixed': context.properties['targetSize']
                }
            }]        
        }#end properties
    }]

    return {'resources': resources}
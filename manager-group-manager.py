#Group Manager

def GenerateConfig(context):

    managerTemplate = '$(ref.' + context.env['deployment'] + '-manager-it.selfLink)'    

    resources = [{
        'name': context.env['name'], #takes name from top-template
        'type': 'compute.v1.regionInstanceGroupManager',
        'properties': {
            'project': context.properties['project'],
            'region': context.properties['region'],
            'targetSize': context.properties['targetSize'], #number of instances to be maintained
            'baseInstanceName': context.env['deployment'] + '-manager',
            'instanceTemplate': managerTemplate,
            'versions':[{
                'instanceTemplate': managerTemplate,
                'targetSize':{
                    'fixed': context.properties['targetSize']
                }
            }]        
        }#end properties
    }]

    return {'resources': resources}
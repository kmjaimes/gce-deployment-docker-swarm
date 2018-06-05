#TCP & UDP Firewalls

def GenerateConfig(context):

    resources = [{
        'name': context.env['name'],
        'type': 'compute.v1.firewall',
        'properties': {
            'network': context.properties['network'],
            'allowed': [{
                'IPProtocol': 'TCP',
                'ports':[2377, 7946]
            },{
                'IPProtocol': 'UDP',
                'ports':[7946, 4789]
            }],#end allowed
            'targetTags': ['swarm-cluster'],
            'sourceTags': ['swarm-cluster']
        }#end properties
    }]

    return {'resources': resources}
README.md

This is a deployment for Google Compute Engine that will create five instances in different zones and automatically initialize and add all nodes to a Docker Swarm. 

# Method of Deployment

[Google SDK command line](https://cloud.google.com/sdk/downloads)

# Configuration

The deployment utilizes a yaml configuration file that imports python templates. A template is a separate file that is imported and used as a type in a configuration. Deployment Manager will recursively expand any imported templates to create the full configuration.

The swarm consists of five instances spread across multiple zones. Three instances are managers and the remaining two are workers. Instances are created in a different zones to mitigate any potential zone outages. Two of the manager instances and both of the worker instances are created with Regional Group Managers and Instance Templates. In the event the swarm loses a manager, it will continue to function as long as there is a quorum of master nodes. Therefore, in this configuration, the swarm can lose 1 manager and continue to function.

config-swarm.yaml<br>
top-template-swarm.py<br>
swarm-manager-origin.py<br>
manager-group-manager.py<br>
swarm-manager-instance.py<br>
worker-group-manager.py<br>
swarm-worker-instance.py<br>
swarm-firewall.py<br>


### Required items:
project name<br>
network<br>
machineType<br>


# Template Summary

config-swarm.yaml
- imports path to all template files used
- sets the values for template properties (project, zone, network, machineType, etc)

top-template-swarm.py
- creates an array of resources used in the configuration file

swarm-manager-origin.py
- creates an instance that will be manager leader node
- startup-script - installs docker, initiates the docker swarm, writes join tokens to the project metadata

manager-group-manager.py
- uses the swarm-manager-instance.py Instance Template to create two manager instances
- Regional Group Managers allow instances to be created in different zones to protect from zone outages
- the group manager will automatically maintain the number of non-leader manager instances

swarm-manager-instance.py
- Instance Template used by manager-group-manager.py to create non-leader manager instances
- startup-script - installs docker, accesses the swarm manager join token from the project metadata, and joins the swarm as a manager

worker-group-manager.py
- uses the swarm-worker-instance.py Instance Template to create two worker instances
- Regional Group Managers allow instances to be created in different zones to protect from zone outages
- the group manager will automatically maintain the number of worker instances

swarm-worker-instance.py
- Instance Template used to create 2 worker instances
- startup-script - installs docker, accesses the swarm worker join token from the project metadata, and joins the swarm as a worker

swarm-firewall.py
- creates firewall rules for swarm to communicate on the network


### Dependencies

GC Deployment Manager service resolves dependencies automatically and in order
(https://cloud.google.com/deployment-manager/docs/configuration/use-references)

For the startup script to read/write data to project and instance metadata, scopes must include 'https://www.googleapis.com/auth/compute'

### DOCKER

Recommendation from Docker regarding installation: "On production systems, you should install a specific version of Docker CE instead of always using the latest."

# Deployment instructions

    If you do not already have Cloud SDK installed, follow the instructions at the following link to install and initialize it:
    (https://cloud.google.com/sdk/downloads)

    The Cloud SDK Shell must be set to the appropriate project:

    *Check configuration settings: `gcloud config list`

    *Set project if necessary: `gcloud config set project [project name]`

    cd to the folder containing your deployment scripts

    choose a base name for the VM instances/swarm nodes and replace [name of deployment] with the base name

    To DEPLOY in gcloud: 
    `gcloud deployment-manager deployments create [name of deployment] --config [configuration filename].yaml --automatic-rollback-on-error`

    To DELETE deployment in gcloud - will delete ALL resources associated with deployment 
    `gcloud deployment-manager deployments delete [name of deployment]`


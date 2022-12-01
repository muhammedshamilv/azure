from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network.models import NetworkSecurityGroup
from azure.mgmt.network.models import SecurityRule

credential = AzureCliCredential()

subscription_id = "183f18e4-754f-4be4-82d6-94ae8dd571aa"

resource_client = ResourceManagementClient(credential, subscription_id)

RESOURCE_GROUP_NAME = "vmconnect"
LOCATION = "eastus"

#create resourse group

rg_result = resource_client.resource_groups.create_or_update(RESOURCE_GROUP_NAME,
    {
        "location": LOCATION
    }
)

print(f"Resource group {rg_result} ")

#create a virtual network

VNET_NAME = "vnet"
SUBNET_NAME = "subnet"
IP_NAME = "ip"
IP_CONFIG_NAME = "ip-config"
NIC_NAME = "nic"
NSG_NAME="nsg"

network_client = NetworkManagementClient(credential, subscription_id)

poller = network_client.virtual_networks.begin_create_or_update(RESOURCE_GROUP_NAME,
    VNET_NAME,
    {
        "location": LOCATION,
        "address_space": {
            "address_prefixes": ["10.0.0.0/16"]
        }
    }
)

vnet_result = poller.result()

print(f"virtual network {vnet_result}")

# create subnet from the virtual network

poller = network_client.subnets.begin_create_or_update(RESOURCE_GROUP_NAME, 
    VNET_NAME, SUBNET_NAME,
    { "address_prefix": "10.0.0.0/24" }
)
subnet_result = poller.result()

print(f"subnet {subnet_result}")

# create IP address 

poller = network_client.public_ip_addresses.begin_create_or_update(RESOURCE_GROUP_NAME,
    IP_NAME,
    {
        "location": LOCATION,
        "sku": { "name": "Standard" },
        "public_ip_allocation_method": "Static",
        "public_ip_address_version" : "IPV4"
    }
)

ip_address_result = poller.result()

print(f"IP address {ip_address_result}")

# create network security group  

parameters = NetworkSecurityGroup()
parameters.location = "eastus"
parameters.security_rules = [SecurityRule(
        protocol = 'Tcp',
        access = 'Allow',
        direction = 'Inbound', 
        description='Allow SSH port 22',
        source_address_prefix = '*',
        destination_address_prefix = '*',
        source_port_range='*', 
        destination_port_range='22', 
        priority=300, 
        name='SSH')]   
poller = network_client.network_security_groups.begin_create_or_update(RESOURCE_GROUP_NAME, NSG_NAME, parameters)

nsg_result = poller.result()

print(f"network security group {nsg_result}")


# create network interface

poller = network_client.network_interfaces.begin_create_or_update(RESOURCE_GROUP_NAME,
    NIC_NAME, 
    {
        "location": LOCATION,
        'network_security_group': {
        'id': nsg_result.id
            },
        "ip_configurations": [ {
            "name": IP_CONFIG_NAME,
            "subnet": { "id": subnet_result.id },
            "public_ip_address": {"id": ip_address_result.id }
        }]
    }
)

nic_result = poller.result()

print(f"network interface client {nic_result}")

# create virtual machine

compute_client = ComputeManagementClient(credential, subscription_id)

VM_NAME = "TestVM"
USERNAME = "azureuser"
PASSWORD = "user@123"

print(f"creating virtual machine will take some time")

poller = compute_client.virtual_machines.begin_create_or_update(RESOURCE_GROUP_NAME, VM_NAME,
    {
        "location": LOCATION,
        "storage_profile": {
            "image_reference": {
                "publisher": 'Canonical',
                "offer": "UbuntuServer",
                "sku": "16.04.0-LTS",
                "version": "latest"
            }
        },
        "hardware_profile": {
            "vm_size": "Standard_DS1_v2"
        },
        "os_profile": {
            "computer_name": VM_NAME,
            "admin_username": USERNAME,
            "admin_password": PASSWORD
        },
        "network_profile": {
            "network_interfaces": [{
                "id": nic_result.id,
            }]
        }        
    }
)

vm_result = poller.result()

print(f"virtual machine {vm_result.name}")
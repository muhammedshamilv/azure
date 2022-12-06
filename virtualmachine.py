import pdb
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network.models import NetworkSecurityGroup
from azure.mgmt.network.models import SecurityRule
import settings

credential = AzureCliCredential()

subscription_id = settings.subscription_id

resource_client = ResourceManagementClient(credential, subscription_id)

LOCATION = "eastus"


def create_vm(rgname, **kwargs):
    #create resourse group
    rg_result = resource_client.resource_groups.create_or_update(rgname,
        {
            "location": LOCATION
        }
    )
    #create a virtual network

    VNET_NAME = "vnet"
    SUBNET_NAME = "subnet"
    IP_NAME = "ip"
    IP_CONFIG_NAME = "ip-config"
    NIC_NAME = "nic"
    NSG_NAME="nsg"

    network_client = NetworkManagementClient(credential, subscription_id)

    poller = network_client.virtual_networks.begin_create_or_update(rgname,
        VNET_NAME,
        {
            "location": LOCATION,
            "address_space": {
                "address_prefixes": ["10.0.0.0/16"]
            }
        }
    )

    vnet_result = poller.result()

    # create subnet from the virtual network

    poller = network_client.subnets.begin_create_or_update(rgname, 
        VNET_NAME, SUBNET_NAME,
        { "address_prefix": "10.0.0.0/24" }
    )
    subnet_result = poller.result()

    # create IP address 

    poller = network_client.public_ip_addresses.begin_create_or_update(rgname,
        IP_NAME,
        {
            "location": LOCATION,
            "sku": { "name": "Standard" },
            "public_ip_allocation_method": "Static",
            "public_ip_address_version" : "IPV4"
        }
    )

    ip_address_result = poller.result()
    
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
    poller = network_client.network_security_groups.begin_create_or_update(rgname, NSG_NAME, parameters)

    nsg_result = poller.result()

    # create network interface

    poller = network_client.network_interfaces.begin_create_or_update(rgname,
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

    # create virtual machine

    compute_client = ComputeManagementClient(credential, subscription_id)

    VM_NAME = "TestVM"
    USERNAME = "azureuser"
    PASSWORD = "user@123"

    print(f"creating virtual machine will take some time")

    poller = compute_client.virtual_machines.begin_create_or_update(rgname, VM_NAME,
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

    response={
        "resource-group":rg_result.name,
        "virtual-network":vnet_result.name,
        "subnet-name":subnet_result.name,
        "ip-address-result":ip_address_result.ip_address,
        "network-security-groups":nsg_result.name,
        "network-interfaces":nic_result.name,
        "virtual-machine-name":vm_result.name
    }

    return response
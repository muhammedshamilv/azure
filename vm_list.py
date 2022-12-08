import settings
from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import ServicePrincipalCredentials
from azure.identity import AzureCliCredential
subscription_id = settings.subscription_id
credential = AzureCliCredential()

compute_client = ComputeManagementClient(credential, subscription_id)

def list_vm():
    vm_list = compute_client.virtual_machines.list_all()
    # vm_list = compute_client.virtual_machines.list('resource_group_name')
    vm_names=[]
    for vm in vm_list:
        vm_names.append(vm.name)
    return vm_names 
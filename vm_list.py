import settings
from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import ServicePrincipalCredentials
from azure.identity import AzureCliCredential
subscription_id = settings.subscription_id
credential = AzureCliCredential()

compute_client = ComputeManagementClient(credential, subscription_id)

vm_list = compute_client.virtual_machines.list_all()
# vm_list = compute_client.virtual_machines.list('resource_group_name')
i= 0
for vm in vm_list:
    array = vm.id.split("/")
    resource_group = array[4]
    vm_name = array[-1]
    statuses = compute_client.virtual_machines.instance_view(resource_group, vm_name).statuses
    status = len(statuses) >= 2 and statuses[1]

    if status and status.code == 'PowerState/running':
        print(vm_name)
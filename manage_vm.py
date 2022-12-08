import settings
from azure.mgmt.compute import ComputeManagementClient
from azure.identity import AzureCliCredential

subscription_id = settings.subscription_id
credential = AzureCliCredential()

compute_client = ComputeManagementClient(credential, subscription_id)

def start_vm(rgname,vm_name):
    start = compute_client.virtual_machines.begin_start(rgname, vm_name)
    start.wait()
    return f"Started {vm_name}"

def restart_vm(rgname,vm_name):
    restart = compute_client.virtual_machines.begin_restart(rgname, vm_name)
    restart.wait()
    return f"Restarted {vm_name}"

def stop_vm(rgname,vm_name):
    stop = compute_client.virtual_machines.begin_power_off(rgname,vm_name)
    stop.wait()
    return f"{vm_name} stopped"
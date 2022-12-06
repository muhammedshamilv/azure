from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.monitor.models import RuleMetricDataSource
from azure.identity import AzureCliCredential
from azure.mgmt.monitor.models import ThresholdRuleCondition
from azure.mgmt.monitor.models import RuleEmailAction

from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import ServicePrincipalCredentials
from azure.identity import AzureCliCredential
subscription_id = "183f18e4-754f-4be4-82d6-94ae8dd571aa"
credential = AzureCliCredential()
resource_group_name = "test"
vm = "myVm"
compute_client = ComputeManagementClient(credential, subscription_id)
vm_list = compute_client.virtual_machines.list(resource_group_name)
for vm in vm_list:
    if vm.name == "myVm":
        id= vm.id
resource_uri = id
resource_id = (
    "subscriptions/{}/"
    "resourceGroups/{}/"
    "providers/Microsoft.Compute/virtualMachines/{}"
).format(subscription_id,resource_group_name,vm)
monitor_client = MonitorManagementClient(
    credential,
    subscription_id
)
# create client
client = MonitorManagementClient(
    credential,
    subscription_id
)

rule_name = 'testerror'


metric_alert = monitor_client.metric_alerts.create_or_update(
    resource_group_name,
    rule_name,
    {
    "location": "global",
    "description": "This is the description of the rule1",
    "severity": "4",
    "enabled": True,
    "scopes": [
        resource_uri
    ],
    "evaluation_frequency": "PT1M",
    "window_size": "PT15M",
    "target_resource_type": "Microsoft.Compute/virtualMachines",
    "target_resource_region": "eastus",
    "criteria": {
        "odata.type": "Microsoft.Azure.Monitor.MultipleResourceMultipleMetricCriteria",
        "all_of": [
        {
            "criterion_type": "DynamicThresholdCriterion",
            "name": "High_CPU_8",
            "metric_name": "Percentage CPU",
            "metric_namespace": "microsoft.compute/virtualmachines",
            "operator": "GreaterOrLessThan",
            "time_aggregation": "Average",
            "dimensions": [],
            "alert_sensitivity": "high",
            "failing_periods": {
            "number_of_evaluation_periods": "3",
            "min_failing_periods_to_alert": "2"
            },
        }
        ]
    },
    "auto_mitigate": False,
    "actions": [
    ]
    }
)
print("Create metric alert:\n{}".format(metric_alert))


# Get metric alert
metric_alert = monitor_client.metric_alerts.get(
    resource_group_name,
    rule_name
)
print("Get metric alert:\n{}".format(metric_alert))


# Delete metric alert
monitor_client.metric_alerts.delete(
    resource_group_name,
    rule_name
)
print("Delete metric alert.\n")
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.monitor.models import RuleMetricDataSource
from azure.identity import AzureCliCredential
from azure.mgmt.monitor.models import ThresholdRuleCondition
from azure.mgmt.monitor.models import RuleEmailAction
from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import ServicePrincipalCredentials
from azure.identity import AzureCliCredential
import settings
credential = AzureCliCredential()
subscription_id = settings.subscription_id

def metric(virtualmachine,rgname,rulename,**kwargs):
    compute_client = ComputeManagementClient(credential, subscription_id)
    vm_list = compute_client.virtual_machines.list(rgname)
    for vm in vm_list:
        if vm.name == virtualmachine:
            id= vm.id
    resource_uri = id
    resource_id = (
        "subscriptions/{}/"
        "resourceGroups/{}/"
        "providers/Microsoft.Compute/virtualMachines/{}"
    ).format(subscription_id,rgname,virtualmachine)
    monitor_client = MonitorManagementClient(
        credential,
        subscription_id
    )

    rule_name = rulename

    metric_alert = monitor_client.metric_alerts.create_or_update(
        rgname,
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

    # # Get metric alert
    # metric_alert = monitor_client.metric_alerts.get(
    #     rgname,
    #     rule_name
    # )
  
    # # Delete metric alert
    # monitor_client.metric_alerts.delete(
    #     rgname,
    #     rule_name
    # )

    return f"{rule_name} succesfully created"
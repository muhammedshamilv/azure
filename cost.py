import settings
from datetime import *
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.costmanagement.models import QueryDefinition, QueryDataset, QueryTimePeriod, QueryAggregation, QueryGrouping 
from azure.identity import AzureCliCredential
subscription_id = settings.subscription_id

credential = AzureCliCredential()

client = CostManagementClient(credential)
def cost_bill(rgname,start_date,end_date):
    time_period=QueryTimePeriod(from_property=start_date, to=end_date)
    query_aggregation = dict()
    query_aggregation["totalCost"] = QueryAggregation(name="Cost", function="Sum") 
    query_aggregation["totalCostUSD"] = QueryAggregation(name="CostUSD", function="Sum")
    query_grouping = [QueryGrouping(type="Dimension", name="ResourceId"), QueryGrouping(type="Dimension", name="ChargeType"),
                        QueryGrouping(type="Dimension", name="PublisherType")]

    querydataset = QueryDataset(granularity=None, configuration=None, aggregation=query_aggregation, grouping=query_grouping)
    query = QueryDefinition(type="ActualCost", timeframe="Custom", time_period=time_period, dataset=querydataset)
    resource_id = (
        "subscriptions/{}/"
        "resourceGroups/{}/"
    ).format(subscription_id,rgname)

    result = client.query.usage(scope = resource_id, parameters=query)
    cost_sum =0
    for row in result.as_dict()['rows']:
        cost_sum += row[1]
    return (f"Cost for [{time}] days for resource group [{rgname}] is [{cost_sum}] USD")
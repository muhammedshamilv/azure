from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient

credential = AzureCliCredential()

subscription_id = "183f18e4-754f-4be4-82d6-94ae8dd571aa"

client = ResourceManagementClient(credential, subscription_id)

resource_group_params = { 'location': "eastus"}

resource_group_name = "test"

# CREATE a resource group

client.resource_groups.create_or_update(resource_group_name, resource_group_params)

print("Resorce group is created!")

# To update the resource group

rg_result = client.resource_groups.create_or_update(
    resource_group_name,
    {
        "location": "centralus"
    }
)

# To update the resource group, repeat the call with different properties, such as tags

rg_result = client.resource_groups.create_or_update(
    resource_group_name,
    {
        "location": "eastus",
        "tags": { "environment":"test", "department":"tech" }
    }
)

# READ all resource group

list_of_resource_groups = client.resource_groups.list()
print("Resource groups")
for rg in list_of_resource_groups:
    print(rg.name)

# UPDATE

resource_group_params.update(tags={"testing" : "training"})
client.resource_groups.update(resource_group_name, resource_group_params )
print("Update is successful.")

# READ - all items within a resource group

resource_list = client.resources.list_by_resource_group(resource_group_name)
for resource in resource_list:
    print(resource.name)

# print all resources

resource_list = client.resources.list()
for resource in (resource_list):
    print(resource.name)

# DELETE the resources and the resource group. will take some time

delete_async_op = client.resource_groups.begin_delete(resource_group_name)
delete_async_op.wait()
print("Resource group is now deleted!")


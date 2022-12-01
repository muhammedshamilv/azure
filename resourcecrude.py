import pdb
from flask import Flask,request,jsonify
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient

app = Flask(__name__)

credential = AzureCliCredential()

subscription_id = "183f18e4-754f-4be4-82d6-94ae8dd571aa"

client = ResourceManagementClient(credential, subscription_id)

resource_group_params = { 'location': "eastus"}

resource_group_name = "Flaskgroup"

@app.route("/")
def main():
    return "Dev-anand Welcome Page"

@app.route('/create/resource/group',methods=['POST'])
def resourcegroup():
    req_data = request.get_json()
    rgname = req_data['rgname']
    rg=client.resource_groups.create_or_update(rgname, resource_group_params)
    response = {
        "resource-group": rg.name,
        "location": rg.location,
    }
    return jsonify(response)

@app.route('/list/resource/group',methods=['GET'])
def listresourcegroup():
    list_of_resource_groups = client.resource_groups.list()
    groups=[]
    for rg in list_of_resource_groups:
        groups.append(rg.name)
    return jsonify(groups)

@app.route('/list/resource/bygroup',methods=['GET'])
def listresource():
    req_data = request.get_json()
    rgname = req_data['rgname']
    resource_list = client.resources.list_by_resource_group(rgname)
    resources=list(resource_list)
    rg_list=[]
    for resource in resources:
        rg_list.append(resource.name)
    return jsonify(rg_list)


@app.route('/list/all/resource/',methods=['GET'])
def listallresource():
    resource_list = client.resources.list()
    rg_list=[]
    for resource in resource_list:
        rg_list.append(resource.name)
    return jsonify(rg_list)


@app.route('/delete/resource/group',methods=['POST'])
def deleteresourcegroup():
    req_data = request.get_json()
    rgname = req_data['rgname']
    delete_async_op = client.resource_groups.begin_delete(rgname)
    delete_async_op.wait()
    return f"Resource group is now deleted!"


if __name__ == "__main__":
    app.run(port=8080)

# # To update the resource group

# rg_result = client.resource_groups.create_or_update(
#     resource_group_name,
#     {
#         "location": "centralus"
#     }
# )

# # To update the resource group, repeat the call with different properties, such as tags

# rg_result = client.resource_groups.create_or_update(
#     resource_group_name,
#     {
#         "location": "eastus",
#         "tags": { "environment":"test", "department":"tech" }
#     }
# )

# resource_group_params.update(tags={"testing" : "training"})
# client.resource_groups.update(resource_group_name, resource_group_params )
# print("Update is successful.")

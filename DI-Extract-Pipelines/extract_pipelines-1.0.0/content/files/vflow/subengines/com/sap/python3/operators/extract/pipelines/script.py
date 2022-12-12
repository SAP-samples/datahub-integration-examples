from datetime import datetime
import json
import requests
import os


#
# get users
#
def get_users(connection):
    restapi = "/auth/v2/user"
    url = connection['url'] + restapi
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    resp = requests.get(url, headers=headers, auth=connection['auth'], verify=True)

    users = resp.json()

    return users


#
# get graphs of a use
#
def get_graphs(connection, user, stopped_after, stopped_before, status):
    restapi = "/app/pipeline-modeler/service/v1/runtime/graphsquery"
    url = connection['url'] + restapi
    headers = {'x-requested-with': 'fetch', 'x-datahub-user': user}
    payload = {
        "filter": ["and", ["greaterThan", "stopped", stopped_after], ["lessOrEqualThan", "stopped", stopped_before],
                   ["equal", "status", status]]}
    resp = requests.post(url, headers=headers, auth=connection['auth'], verify=True, data=json.dumps(payload))

    if resp.status_code != 200:
        # api.logger.error(f"Status code for user {user}: {r.status_code}  - {r.text}")
        return []

    graphs = resp.json()
    return graphs


#
# get graphs of a use
#
def get_graph_runtime_details(connection, handle, user):
    restapi = "/app/pipeline-modeler/service/v1/runtime/graphdescriptions"
    url = connection['url'] + restapi + "/" + handle + "?space=tenant"
    headers = {'X-Requested-With': 'XMLHttpRequest', 'x-datahub-user': user}
    resp = requests.get(url, headers=headers, auth=connection['auth'], verify=True)

    if resp.status_code != 200:
        # api.logger.error(f"Status code for url {url}: {r.status_code}  - {r.text}")
        return []

    graph_description = resp.json()
    return graph_description


#
# Callback of operator
#
def gen():
    host = api.config.connection_id['connectionProperties']['host']
    user = api.config.connection_id['connectionProperties']['user']
    pwd = api.config.connection_id['connectionProperties']['password']
    tenant = os.environ.get('VSYSTEM_TENANT')
    
    stopped_after = api.config.connection_id['stopped_after']
    stopped_before = api.config.connection_id['stopped_before']
    status = pi.config.connection_id['status']

    if not tenant:
        api.logger.warning("No system variable \'VSYSTEM_TENANT\' set.")
        tenant = 'default'
    connection = {'url': host, 'auth': (tenant + '\\' + user, pwd)}

    # process

    cluster = host.replace('https://', '')
    conn = '{"configurationType": "Connection Management", "connectionID": "S3_Catalog"}'
    size = 999999
    isDir = False
    modTime = '1982-04-15T00:00:00'

    user_list = get_users(connection)

    for user in user_list:

        user_graphs = get_graphs(connection, user['username'], stopped_after, stopped_before, status)

        timestr = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join('/pipeline/', cluster, tenant, user['username'],
                            user['username'] + '_merged_' + timestr + '.jsonl')
        header = {"com.sap.headers.batch": [0, False, 1, 0, ""],
                  "com.sap.headers.file": [conn, path, size, isDir, modTime]}

        graph_list = list()
        for graph in user_graphs:
            graph_list.append(graph)

            graph_details = get_graph_runtime_details(connection, graph['handle'], user['username'])

            if graph_details:
                graph_list.append(graph_details)

        tbl1 = api.Table(graph_list)
        api.outputs.output.publish(tbl1, header=header)


api.set_prestart(gen)
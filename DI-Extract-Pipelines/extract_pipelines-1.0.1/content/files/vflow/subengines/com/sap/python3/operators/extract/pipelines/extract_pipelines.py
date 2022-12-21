from datetime import datetime
import json
import requests
import io
import os


#
# get users
#
def get_users(connection):
    restapi = "/auth/v2/user"
    url = connection['url'] + restapi
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    resp = requests.get(url, headers=headers, auth=connection['auth'], verify=True, timeout=5)

    if resp.status_code != 200:
        api.logger.error(f"Status code for user {user}: {resp.status_code}  - {resp.text}")
        return []

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
        "filter": ["and", ["greaterThan", "stopped", stopped_after], ["lessOrEqualThan", "stopped", stopped_before]]}

    if ',' in status:
        status = [x.strip() for x in status.split(',')]
        status_list = ["or"]
        for i in range(len(status)):
            status_list.append(["equal", "status", status[i]])
        payload['filter'].append(status_list)
    else:
        status_list = ["equal", "status"]
        status_list.append(status)
        payload['filter'].append(status_list)

    resp = requests.post(url, headers=headers, auth=connection['auth'], verify=True, data=json.dumps(payload),
                         timeout=5)

    if resp.status_code != 200:
        api.logger.error(f"Status code for user {user}: {resp.status_code}  - {resp.text}")
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
    resp = requests.get(url, headers=headers, auth=connection['auth'], verify=True, timeout=5)

    if resp.status_code != 200:
        api.logger.error(f"Status code for url {url}: {resp.status_code}  - {resp.text}")
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

    stopped_after = api.config.stopped_after
    stopped_before = api.config.stopped_before
    status = api.config.status

    if not tenant:
        api.logger.warning("No system variable \'VSYSTEM_TENANT\' set.")
        tenant = 'default'
    connection = {'url': host, 'auth': (tenant + '\\' + user, pwd)}

    # process

    cluster = host.replace('https://', '')
    conn = '{"configurationType": "Connection Management", "connectionID": "S3_Catalog"}'
    size = 9999999
    isDir = False
    modTime = '1982-04-15T00:00:00'

    user_list = get_users(connection)

    timestr = datetime.now().strftime("%Y%m%d_%H%M%S")

    active_users = list()
    for user in user_list:
        user_graphs = get_graphs(connection, user['username'], stopped_after, stopped_before, status)
        if user_graphs:
            active_users.append(user)

    n = len(active_users)
    for i, user in enumerate(active_users):
        isLast = True if n - 1 == i else False

        user_graphs = get_graphs(connection, user['username'], stopped_after, stopped_before, status)

        path = os.path.join('/pipeline/', cluster, tenant, user['username'],
                            user['username'] + '_' + timestr + '.jsonl')

        header = {"com.sap.headers.batch": [i, isLast, n, 0, ""],
                  "com.sap.headers.file": [conn, path, size, isDir, modTime]}

        graph_list = list()
        for graph in user_graphs:
            graph_bytes = json.dumps(graph, indent=2).encode('utf-8')
            api.outputs.output.publish(io.BytesIO(graph_bytes), n=-1, header=header)

            graph_details = get_graph_runtime_details(connection, graph['handle'], user['username'])
            if graph_details:
                graph_datails_bytes = json.dumps(graph_details, indent=2).encode('utf-8')
                api.outputs.output.publish(io.BytesIO(graph_datails_bytes), n=-1, header=header)


api.set_prestart(gen)

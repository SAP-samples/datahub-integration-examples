import json
import requests
import pandas as pd
import time


#
# get graphs of a user
#
def get_graphs(connection, user):
    restapi = "/app/pipeline-modeler/service/v1/runtime/graphsquery"
    url = connection['url'] + restapi
    headers = {'x-requested-with': 'fetch', 'x-datahub-user': user}
    payload = {"filter": ["equal", "status", "completed"]}
    r = requests.post(url, headers=headers, auth=connection['auth'], verify=True, data=json.dumps(payload))

    if r.status_code != 200:
        api.logger.error(f"Status code for user {user}: {r.status_code}  - {r.text}")
        return []

    graphs = list()
    for g in r.json():
        substitutions = json.dumps(g['configurationSubstitutions']) if 'configurationSubstitutions' in g else '{}'
        runtime = g['stopped'] - g['submitted']

        submitted = g['submitted']
        stopped = g['stopped']
        submitted = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(submitted))
        stopped = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stopped))

        if runtime < 0:
            runtime = 0
        rec = {'user': g['user'], 'tenant': g['tenant'], 'src': g['src'], 'name': g['name'], 'handle': g['handle'],
               'status': g['status'], 'submitted': submitted, 'stopped': stopped, 'runtime': runtime,
               'substitutions': substitutions}
        graphs.append(rec)
    return graphs


#
# Callback of operator
#
def on_input(msg_id, header, data):
    host = header["extract.connection_http"][0]
    user = header["extract.connection_http"][1]
    pwd = header["extract.connection_http"][2]
    tenant = header["extract.connection_http"][4]
    connection = {'url': host, 'auth': (tenant + '\\' + user, pwd)}

    # process
    users = data.get()

    if not users:
        return None

    graphs = list()
    for row in users.body:
        user_graphs = get_graphs(connection, row[1])
        if user_graphs:
            graphs.extend(user_graphs)

    if not graphs:
        return None

    df = pd.DataFrame(graphs)

    # output
    header = {"com.sap.headers.batch": [0, True, 1, 0, ""],
              "extract.connection_http": [host, user, pwd, '', tenant]}

    # Sort the outcome
    v_ref = api.DataTypeReference("table", "extract.runtime_graphs")
    table_vtype = api.type_context.get_vtype(v_ref)
    column_names = list(table_vtype.columns.keys())
    df = df[column_names]

    tbl = api.Table(df.values.tolist(), "extract.runtime_graphs")
    api.outputs.output.publish(tbl, header=header)


api.set_port_callback("input", on_input)


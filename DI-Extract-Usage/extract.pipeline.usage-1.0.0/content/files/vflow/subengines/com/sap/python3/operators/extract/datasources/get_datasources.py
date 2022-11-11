import json
import requests
import pandas as pd


def remove_nan(df):
    # Fill empty values with '' or 0
    for c in df.select_dtypes(include=['float64', 'int64']):
        df[c].fillna(0, inplace=True)
    for c in df.select_dtypes(include=['object']):
        df[c].fillna('', inplace=True)


def columns_with_nan(df):
    nan_cols = [c for c in df.columns if df[c].isna().any()]


#
# get graphs of a use
#
def get_graph_runtime_details(connection, handle, user):
    restapi = "/app/pipeline-modeler/service/v1/runtime/graphdescriptions"
    url = connection['url'] + restapi + "/" + handle + "?space=tenant"
    headers = {'X-Requested-With': 'XMLHttpRequest', 'x-datahub-user': user}
    r = requests.get(url, headers=headers, auth=connection['auth'], verify=True)

    if r.status_code != 200:
        api.logger.error(f"Status code for url {url}: {r.status_code}  - {r.text}")
        return []

    graph_description = r.json()
    return graph_description


#
# get target data sources set in operators
#
def get_datasources(graph_description, handle, substitutions):
    sources = list()
    for name, details in graph_description['processes'].items():
        component = details['component']
        config = details['metadata']['config']
        service = ''
        try:
            if component in ['com.sap.file.read', 'com.sap.file.write', 'com.sap.file.write.v2'] and \
                    'dynamicConnection' not in config and 'path' in config:
                if 'connectionID' not in config['connection']:
                    connection_id = 'LOCAL'
                else:
                    connection_id = config['connection']
                path = config['path']
                direction = 'R' if component == 'com.sap.file.read' else "W"
            elif component in ['com.sap.hana.client2', 'com.sap.hana.readTable', 'com.sap.hana.writeTable',
                               'com.sap.hana.readTable.v2', 'com.sap.hana.writeTable.v2']:
                connection_id = config['connection']['connectionID']
                path = config['tableName']
                if component in ['com.sap.hana.readTable', 'com.sap.hana.readTable.v2']:
                    direction = 'R'
                elif component in ['com.sap.hana.writeTable.v2', 'com.sap.hana.writeTable']:
                    direction = 'W'
                else:
                    direction = 'U'
            elif component in ['com.sap.database.table.consumer.v2', 'com.sap.database.table.producer.v2',
                               'com.sap.database.table.consumer.v3', 'com.sap.database.table.producer.v3',
                               'com.sap.storage.consumer.v2', 'com.sap.storage.producer.v2',
                               'com.sap.storage.consumer.v3', 'com.sap.storage.producer.v3'] and config['service']:
                connection_id = config['serviceConnection']['connectionID']
                path = config['source']['remoteObjectReference']['qualifiedName']
                service = config['service']
                if component in ['com.sap.database.table.consumer.v2', 'com.sap.database.table.consumer.v3',
                                 'com.sap.storage.consumer.v2', 'com.sap.storage.consumer.v3']:
                    direction = 'R'
                else:
                    direction = 'W'
            else:
                continue
            if substitutions:
                subs = json.loads(substitutions)
                for key, value in subs.items():
                    connection_id = connection_id.replace('${' + key + '}', value)
                    path = path.replace('${' + key + '}', value)
            sources.append({'handle': handle, 'connection_id': connection_id, 'type': service, 'path': path,
                            'component': component, 'direction': direction})
        except KeyError as ke:
            api.logger.error(f"KeyError Exception: {ke}")
            raise KeyError(ke)

    return sources


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
    graphs_tbl = data.get()
    table_vtype = api.type_context.get_vtype(graphs_tbl.get_type_reference())
    columns = list(table_vtype.columns.keys())
    df = pd.DataFrame(graphs_tbl.body, columns=columns)
    api.logger.info(f"Got data in DataFrame with columns: {columns}")

    graph_sources = list()
    for index, row in df.iterrows():
        g = get_graph_runtime_details(connection, row['handle'], row['user'])
        if g:
            sources = get_datasources(g, row['handle'], row['substitutions'])
            graph_sources.extend(sources)
    df_sources = pd.DataFrame(graph_sources)

    df_sources['data_source'] = df_sources['type'] + '/' + df_sources['connection_id'] + df_sources['path']
    df_sources = df_sources.drop(['type', 'connection_id', 'path'], axis=1)

    df = pd.DataFrame.merge(df, df_sources, left_on='handle', right_on='handle', how='inner')
    df.drop("substitutions", axis=1, inplace=True)

    # output
    header = [0, True, 1, 0, ""]
    header = {"com.sap.headers.batch": header}

    # Sort the outcome
    v_ref = api.DataTypeReference("table", "$GRAPH.graph_datasources")
    table_vtype = api.type_context.get_vtype(v_ref)
    column_names = list(table_vtype.columns.keys())
    df = df[column_names]

    for c in df.select_dtypes(include=['object']):
        df[c].fillna('', inplace=True)

    api.logger.info(f"Table with columns created and send: {column_names}")
    api.logger.info(f"Datatypes of DataFrame: {df.dtypes}")
    tbl = api.Table(df.values.tolist(), "$GRAPH.graph_datasources")
    api.outputs.output1.publish(tbl, header=header)
    api.outputs.output2.publish(tbl, header=header)


api.set_port_callback("input", on_input)

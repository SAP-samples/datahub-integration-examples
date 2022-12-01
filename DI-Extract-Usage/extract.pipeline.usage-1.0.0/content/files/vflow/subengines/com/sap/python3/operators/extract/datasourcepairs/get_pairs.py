import itertools
import pandas as pd


def flatten(list):
    return [item for sublist in list for item in sublist]


def findsubsets(set, size):
    return list(itertools.combinations(set, size))


#
# get pairs of data sources frequently used together
#
def get_datasource_pairs(df):
    pairs = list()

    pairs_df = df.loc[:, ['handle', 'direction', 'data_source']]
    pairs_df['direction_data_source'] = '[' + pairs_df['direction'] + ']' + ' ' + pairs_df['data_source']
    pairs_df = pairs_df.drop(['direction', 'data_source'], axis=1)

    pairs_df = pairs_df.groupby(['handle'])['direction_data_source'].apply(list).reset_index(
        name='direction_data_source')
    path_list = pairs_df['direction_data_source'].to_list()

    for i in range(len(path_list)):
        pairs.append(findsubsets(path_list[i], 2))
    pairs = flatten(pairs)

    pairs_df = pd.DataFrame(pairs)
    pairs_df.columns = ['data_source1', 'data_source2']
    pairs_df = pairs_df.groupby(['data_source1', 'data_source2']).size().reset_index(name='count')

    return pairs_df


#
# Callback of operator
#
def on_input(msg_id, header, data):
    graphs_tbl = data.get()
    table_vtype = api.type_context.get_vtype(graphs_tbl.get_type_reference())
    columns = list(table_vtype.columns.keys())
    df = pd.DataFrame(graphs_tbl.body, columns=columns)
    api.logger.info(f"Got data in DataFrame with columns: {columns}")

    pairs_df = get_datasource_pairs(df)

    # output
    header = [0, True, 1, 0, ""]
    header = {"com.sap.headers.batch": header}

    # Sort the outcome
    v_ref = api.DataTypeReference("table", "$GRAPH.datasource_pairs")
    table_vtype = api.type_context.get_vtype(v_ref)
    column_names = list(table_vtype.columns.keys())
    pairs_df = pairs_df[column_names]


    api.logger.info(f"Table with columns created and send: {column_names}")
    api.logger.info(f"Datatypes of DataFrame: {pairs_df.dtypes}")
    tbl = api.Table(pairs_df.values.tolist(), "$GRAPH.datasource_pairs")
    api.outputs.output.publish(tbl, header=header)


api.set_port_callback("input", on_input)


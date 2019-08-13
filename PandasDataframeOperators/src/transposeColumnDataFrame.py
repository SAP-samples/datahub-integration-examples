import pandas as pd
import json

MAX_COLUMNS = 2

def process(msg):

    # test if body refers to a DataFrame type
    df = msg.body
    if not isinstance(df,pd.DataFrame) :
        raise TypeError('Message body does not contain a pandas DataFrame')

    #####################
    #  pd operations
    #####################

    if api.config.reset_index:
        df.reset_index(inplace=True)

    ## Selection of values in transpose column to be created as new columns
    if api.config.selected_values or not api.config.selected_values == "None" :
        selection_v_str = api.config.selected_values.replace(" ", "")
        selected_values = selection_v_str.split(',')
    else :
        selected_values = df[api.config.transpose_column].unique()
    if len(selected_values) > MAX_COLUMNS :
        raise ValueError("Maximum columns: " + int(MAX_COLUMNS + "  actual transpose columns: " + int(len(selected_values))))


    # create DataFrame with numbered columns add concat it to df
    new_cols = {api.config.transpose_column + '_' + str(i): selected_values[i] for i in range(0, len(selected_values))}
    cat_df = pd.DataFrame(columns=new_cols.keys(), index=df.index, dtype='int8')
    cat_df = cat_df.fillna(value=0).astype(dtype='int8')
    df = pd.concat([df, cat_df], axis=1)

    # setting the corresponding column to 1 for all category appearances
    for col, val in new_cols.items():
        df.loc[df[api.config.transpose_column] == val, col] = 1
    df.drop(columns=[api.config.transpose_column], inplace=True)


    # group df
    groupby_column = api.config.groupby_column.replace(" ", "")
    aggr_trans = api.config.aggr_trans.replace(" ", "")
    aggr_default = api.config.aggr_default.replace(" ", "")
    if groupby_column:
        aggregation = dict()
        for col in df.columns:
            aggregation[col] = aggr_trans if col in new_cols else aggr_default
        del aggregation[groupby_column]

        df = df.groupby(groupby_column).agg(aggregation)
        # count only occurance of categories
        for col in new_cols.keys():
            df.loc[df[col] >= 1, col] = 1


    #####################
    #  final infos to attributes and info message
    #####################
    prev_att = msg.attributes
    att_dict = dict()
    att_dict['config'] = dict()

    # df from body
    att_dict['operator'] = 'transposeColumnDataFrame' # name of operator
    att_dict['mem_usage'] = df.memory_usage(deep=True).sum() / 1024 ** 2
    att_dict['name'] = prev_att['name']
    att_dict['columns'] = list(df.columns)
    att_dict['number_columns'] = len(att_dict['columns'])
    att_dict['number_rows'] = len(df.index)
    att_dict['example_row_1'] = str(df.iloc[0, :].tolist())

    return api.Message(attributes=att_dict,body = df), new_cols



'''
Mock pipeline engine api to allow testing outside pipeline engine
'''
class test :
    BIGDATA = 1
    SIMPLE = 0

test_scenario = test.SIMPLE

try:
    api
except NameError:
    class api:

        # input data - only used for isolated testing
        def set_test(test_scenario):
            if test_scenario == test.BIGDATA :
                df = pd.read_csv("/Users/madmax/big_data/test1.csv",sep=';')
                df.set_index(keys='index', inplace=True)

            else :
                df = pd.DataFrame(
                    {'icol': [1, 2, 3, 4, 5], 'xcol2': ['1', '1', '2', '2', '3'], 'xcol3': ['K', 'L', 'M', 'N', 'O'], \
                     'xcol4': ['A', 'B', 'A', 'B', 'C']})
                df.set_index(keys='icol', inplace=True)

            # input data
            att = {'format': 'pandas','name':'test'}

            return api.Message(attributes=att,body=df)

        # setting test config data
        def set_config (test_scenario) :
            if test_scenario == test.BIGDATA :
                api.config.transpose_column = ''
                api.config.selected_values = ''
                api.config.groupby_column = '' # integer
                api.config.aggr_trans = 'sum'
                api.config.aggr_default = 'first'
                api.config.reset_index = False
            else :  # test_scenario == test.SIMPLE:
                api.config.transpose_column = 'xcol4'
                api.config.selected_values = 'A,B'
                api.config.groupby_column = 'xcol2'
                api.config.aggr_trans = 'sum'
                api.config.aggr_default = 'first'
                api.config.reset_index = False

        # definition of api.config - variable names should be same as in DI implementation
        class config:
            transpose_column = ''
            selected_values = ''
            groupby_column = ''  # integer
            aggr_trans = 'sum'
            aggr_default = 'first'
            reset_index = False

        # fake definition of api.Message
        class Message:
            def __init__(self, body=None, attributes=""):
                self.body = body
                self.attributes = attributes

        # fake definition - can be used of asserting test results
        def send(port, msg):
            if isinstance(msg,str) :
                print(msg)
            else :
                print(api.set_test(test_scenario).body)
                print(msg.body)
            pass

        # fake definition - called by 'isolated'-test simulation
        def set_port_callback(port, callback):
            if isinstance(port,list) :
                port = str(port)
            print("Call \"" + callback.__name__ + "\"  messages port \"" + port + "\"..")
            # creates the message "send" to the inport based on the test
            msg= api.set_test(test_scenario)
            # sets the configuration based on the test
            api.set_config(test_scenario)
            # calls the "process" function
            callback(msg)

        # called by 'integrated/pipeline-test simulation
        def test_call(msg):
            print('EXTERNAL CALL of module:' + __name__)
            api.set_config(test_scenario)
            result = process(msg)
            # because when called locally via this function, 'api.set_port_callback' and 'interface' are not called
            api.send("DataFrame",result)
            return result

# gateway that gets the data from the inports and sends the result to the outports
def interface(msg):
    result, new_cols = process(msg)
    api.send("outDataFrameMsg", result)
    info_str = json.dumps(result.attributes, indent=4)
    api.send("Info", info_str)
    api.send("NewColumns", str(new_cols))


# Triggers the request for every message
api.set_port_callback("inDataFrameMsg", interface)

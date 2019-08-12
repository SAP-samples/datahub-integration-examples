import pandas as pd
import json

def process(left_msg,right_msg):

    l_att = left_msg.attributes
    r_att = right_msg.attributes

    att_dict = dict()
    att_dict['operator'] = 'joinDataFrames'
    if l_att['name'] == r_att['name'] :
        att_dict['name'] = l_att['name']
    else :
        att_dict['name'] = l_att['name'] + '-' + r_att['name']
    att_dict['config'] = dict()
    att_dict['memory'] = dict()

    # read stream from memory
    left_df = left_msg.body
    right_df = right_msg.body

    # merge according to config
    if api.config.on_index :
        att_dict['config']['on_index'] = api.config.on_index
        df = pd.merge(left_df, right_df, how=api.config.how, left_index=True,right_index=True)
    elif api.config.left_on and api.config.right_on :
        att_dict['config']['left_on'] = api.config.left_on
        att_dict['config']['right_on'] = api.config.right_on
        left_df.reset_index(inplace=True)
        right_df.reset_index(inplace=True)
        df = pd.merge(left_df, right_df, how=api.config.how, left_on=api.config.left_on,right_on=api.config.right_on)
    else :
        raise ValueError("Config setting: Either <on> or both <left_on> and <right_on> has to be set in order to join the dataframes")

    if api.config.new_indices and not api.config.new_indices == 'None':
        att_dict['config']['new_indices'] = api.config.new_indices
        index_list = [x.strip() for x in api.config.new_indices.split(',')]
        df.set_index(keys = index_list,inplace=True)

    if api.config.drop_columns and not api.config.drop_columns == 'None':
        att_dict['config']['drop_columns'] = api.config.drop_columns
        col_list = [x.strip() for x in api.config.drop_columns.split(',')]
        df.drop(labels = col_list,axis=1,inplace=True)

    att_dict['memory']['mem_usage'] = df.memory_usage(deep=True).sum() / 1024 ** 2
    att_dict['columns'] = list(df.columns)
    att_dict['number_columns'] = len(att_dict['columns'])
    att_dict['number_rows'] = len(df.index)
    att_dict['example_row_1'] = str(df.iloc[0, :].tolist())

    # Serialize df, former pickle versions are restricted by 4GB
    mem = df.memory_usage().sum()
    body = df

    return api.Message(attributes=att_dict,body = body)



'''
Mock pipeline engine api to allow testing outside pipeline engine
'''
class test :
    READ_BIG = 1
    SIMPLE = 0
    ORDER_HEADER_DETAIL = 3
    ORDER_PRODUCT_MD = 4
test_scenario = test.READ_BIG

try:
    api
except NameError:
    class api:

        # input data
        def set_test(test_scenario):
            if test_scenario == test.READ_BIG :
                l_df = pd.read_csv("/Users/d051079/OneDrive - SAP SE/Datahub-Dev/data/order_headers.csv",sep=';')
                l_df.set_index(keys='order_id', inplace=True)
                r_df = pd.read_csv("/Users/d051079/OneDrive - SAP SE/Datahub-Dev/data/order_details.csv",sep=';')
                r_df.set_index(keys=['order_id','product_id'], inplace=True)
            else :
                l_df = pd.DataFrame(
                    {'icol': [1, 2, 3, 4, 5], 'xcol2': ['A', 'B', 'C', 'D', 'E'], 'xcol3': ['K', 'L', 'M', 'N', 'O']})
                l_df.set_index(keys='icol', inplace=True)
                r_df = pd.DataFrame(
                    {'icol': [3, 4, 5, 6, 7], 'ycol2': ['C', 'D', 'E', 'F', 'G'], 'ycol3': ['M', 'N', 'O', 'P', 'Q']})
                r_df.set_index(keys='icol', inplace=True)

            # input data
            att1 = {'format': 'pandas','name':'leftDF'}
            att2 = {'format': 'pandas','name':'rightDF'}

            return api.Message(attributes=att1,body=l_df), api.Message(attributes=att2,body=r_df)

        class config:
            how = "inner"
            on_index = False
            left_on = "order_id"
            right_on = "order_id"
            new_indices = "order_id, product_id"
            drop_columns = 'None'

        def set_config (test_scenario) :
            if test_scenario == test.ORDER_HEADER_DETAIL :
                api.config.how = "inner"
                api.config.on_index = False
                api.config.left_on ="order_id"
                api.config.right_on = "order_id"
                api.config.new_indices ="order_id, product_id"
                api.config.drop_columns = 'None'
            elif test_scenario == test.ORDER_PRODUCT_MD :
                api.config.how = "inner"
                api.config.on_index = False
                api.config.left_on ="product_id"
                api.config.right_on = "product_id"
                api.config.new_indices ="order_id, product_id"
                api.config.drop_columns = 'None'
            elif test_scenario == test.READ_BIG :
                api.config.how = "inner"
                api.config.on_index = False
                api.config.left_on ="order_id"
                api.config.right_on = "order_id"
                api.config.new_indices ="order_id, product_id"
                api.config.drop_columns = 'None'
            else :
                api.config.how = "inner"
                api.config.on_index = False
                api.config.left_on ="icol"
                api.config.right_on = "icol"
                api.config.new_indices ="icol"
                api.config.drop_columns = 'None'         # drops columns after merge

        class Message:
            def __init__(self, body=None, attributes=""):
                self.body = body
                self.attributes = attributes

        def send(port, msg):
            #if isinstance(msg,pd.DataFrame) :
            #    print(msg.body.head(1))
            #else :
            #    print(msg)
            pass

        # called by 'isolated'-test simulation
        def set_port_callback(port, callback):
            if isinstance(port,list) :
                port = str(port)
            print("Call \"" + callback.__name__ + "\"  messages port \"" + port + "\"..")
            l_msg, r_msg = api.set_test(test_scenario)
            api.set_config(test_scenario)
            callback(l_msg,r_msg)

        # called by 'integrated/pipeline-test simulation
        def test_call(l_msg, r_msg,scenario):
            print('EXTERNAL CALL of module:' + __name__)
            api.set_config(scenario)
            result = process(l_msg,r_msg)
            api.send("outDataFrame",result)
            return result

def interface(left_msg,right_msg):
    result_df = process(left_msg,right_msg)
    api.send("outDataFrameMsg", result_df)
    info_str = json.dumps(result_df.attributes, indent=4)
    api.send("Info", info_str)


# Triggers the request for every message (the message provides the stock_symbol)
# to be commented when imported for external 'integration' call
#api.set_port_callback(["leftDFMsg","rightDFMsg"], interface)


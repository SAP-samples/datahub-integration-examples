import pandas as pd
import re
import json


def process(df_msg):

    prev_att = df_msg.attributes
    df = df_msg.body

    att_dict = dict()
    att_dict['config'] = dict()
    att_dict['memory'] = dict()
    att_dict['operator'] = 'selectDataFrame'
    att_dict['name'] = prev_att['name']

    # save and reset indices
    index_names = df.index.names
    if index_names[0]  :
        df.reset_index(inplace=True)

    # prepare selection for numbers
    if api.config.selection_num :
        selection_num_str = api.config.selection_num.replace(" ", "").replace("!=", "!")
        selection_num_str = selection_num_str.replace("==", "=")
        att_dict['config']['selection_num'] = selection_num_str
        sel_num_list = selection_num_str.split(',')

        selected_cols = dict()
        for selection in sel_num_list:
            m = re.match(u'(\w+)([<>=!])(\w+)', selection)
            column = m.group(1)
            comp = m.group(2)
            value = float(m.group(3))
            if comp == '=':
                df = df.loc[df[column] == value]
                selected_cols[column] = ['=',value]
            elif comp == '>':
                df = df.loc[df[column] > value]
                selected_cols[column] = ['>', value]
            elif comp == '<':
                df = df.loc[df[column] < value]
                selected_cols[column] = ['<', value]
            elif comp == '!':
                df = df.loc[df[column] != value]
                selected_cols[column] = ['!=', value]

        # prepare selection statement
    if api.config.selection_list :
        sel_str_str = api.config.selection_list.replace(" ", "").replace("!=", "!").replace("==", "=")
        att_dict['config']['selection_list'] = sel_str_str

        m = re.match(u'(\w+)([=!])(\S+)', sel_str_str)
        column = m.group(1)
        comp = m.group(2)
        values = m.group(3)
        value_list = m.group(3).split(',')

        if comp == '=':
            df = df.loc[df[column].isin(value_list)]
        elif comp == '!':
            df = df.loc[~df[column].isin(value_list)]

    # set  index again
    if index_names[0]  :
        att_dict['indices'] = index_names
        df.set_index(keys = index_names,inplace=True)

    att_dict['memory']['mem_usage'] = df.memory_usage(deep=True).sum() / 1024 ** 2
    att_dict['columns'] = list(df.columns)
    att_dict['number_columns'] = len(att_dict['columns'])
    att_dict['number_rows'] = len(df.index)
    att_dict['example_row_1'] = str(df.iloc[0,:].tolist())

    return  api.Message(attributes = att_dict,body=df)


'''
Mock pipeline engine api to allow testing outside pipeline engine
'''

class test :
    ORDER_HEADERS = 2
    SIMPLE = 0

actual_test = test.ORDER_HEADERS

try:
    api
except NameError:
    class api:

        def set_test(test_scenario):
            print('TEST SCENARIO: ' + str(test_scenario))
            if test_scenario == test.ORDER_HEADERS:
                df = pd.read_csv("/Users/d051079/OneDrive - SAP SE/Datahub-Dev/data/order_headers.csv", sep=';')
                df.set_index(keys='order_id', inplace=True)
            else : #test_scenario == test.SIMPLE
                df = pd.DataFrame(
                    {'icol': [1, 2, 3, 4, 5], 'xcol2': ['A', 'B', 'C', 'D', 'E'], 'xcol3': ['K', 'L', 'M', 'N', 'O']})

            attributes = {'format': 'csv','name':'DF_name'}

            return api.Message(attributes=attributes,body=df)

        def set_config(test_scenario) :
            if test_scenario == test.ORDER_HEADERS:
                api.config.selection_num = 'Year = 2016, Month = 5'  # operators comparisons: <,>,=,!=
                api.config.selection_list = ''  # operators comparisons: <,>,=,!=
            else : # SIMPLE
                api.config.selection_num = 'col1 < 3, col2 > 200 '  # operators comparisons: <,>,=,!=
                api.config.selection_list = ''  # operators comparisons: <,>,=,!=

        class config:
            selection_num = 'order_id < 100000'  # operators comparisons: <,>,=,!=
            selection_list = 'trans_date = 2016-03-03, 2016-02-04 '  # operators comparisons: <,>,=,!=

        class Message:
            def __init__(self,body = None,attributes = ""):
                self.body = body
                self.attributes = attributes

        def send(port, msg):
            #if isinstance(msg,pd.DataFrame) :
            #    print(msg.body.head(1))
            #else :
            #    print(msg)
            pass

        def set_port_callback(port, callback):
            msg = api.set_test(actual_test)
            api.set_config(actual_test)
            print("Call \"" + callback.__name__ + "\"  messages port \"" + port + "\"..")
            callback(msg)

            # called by 'integrated/pipeline-test simulation

        def test_call(msg):
            print('EXTERNAL CALL of module:' + __name__)
            api.set_config(actual_test)
            result = process(msg)
            api.send("outDataFrame", result)
            return result



def interface(msg):
    result = process(msg)
    api.send("outDataFrameMsg", result)
    info_str = json.dumps(result.attributes, indent=4)
    api.send("Info", info_str)


# Triggers the request for every message (the message provides the stock_symbol)
#api.set_port_callback("inDataFrameMsg", interface)


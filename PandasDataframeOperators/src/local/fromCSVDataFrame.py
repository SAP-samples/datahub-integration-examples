import pandas as pd
import io
import json
import re


def downcast(df, data_type, to_type):
    cols = list(df.select_dtypes(include=[data_type]).columns)
    if len(cols) == 0:
        return df, None

    downcast_dict = dict()
    downcast_dict['data_type'] = data_type
    cdtypes = df[cols].dtypes.to_dict()
    downcast_dict['previous_subtypes'] = {col: str(itype) for col, itype in cdtypes.items()}
    downcast_dict['previous_mem_usage'] = df[cols].memory_usage(deep=True).sum() / 1024 ** 2

    df[cols] = df[cols].apply(pd.to_numeric, downcast=to_type)

    int_dtypes2 = df[cols].dtypes.to_dict()
    downcast_dict['subtypes'] = {col: str(itype) for col, itype in int_dtypes2.items()}
    downcast_dict['mem_usage'] = df[cols].memory_usage(deep=True).sum() / 1024 ** 2

    return df, downcast_dict


def process(msg):
    att_dict = dict()
    att_dict['operator'] = 'fromCSVDataFrame'

    att_dict['config'] = dict()
    att_dict['memory'] = dict()

    # json string of attributes already converted to dict
    # att_dict['prev_attributes'] = msg.attributes
    csv_file = msg.attributes["storage.pathInPolledDirectory"]  #: "retail/order_headers.csv"

    # using file name from attributes of ReadFile
    if not api.config.df_name or api.config.df_name == "DataFrame":
        att_dict['name'] = re.match(u'.*/(\S+)\.\w+', "cvf/retail/order_headers.csv").group(1)
    else:
        att_dict['name'] = api.config.df_name

    if isinstance(msg.body, str):
        csv_io = io.StringIO(msg.body)
    elif isinstance(msg.body, bytes):
        csv_io = io.BytesIO(msg.body)
    elif isinstance(msg.body, io.BytesIO):
        csv_io = msg.body
    else:
        raise TypeError('Message body has unsupported type' + str(type(msg.body)))

    if api.config.limit_rows == 0:
        if api.config.use_columns and not api.config.use_columns == 'None':
            use_cols = [x.strip() for x in api.config.use_columns.split(',')]
            att_dict['config']['use_columns'] = str(use_cols)
            df = pd.read_csv(csv_io, api.config.separator, usecols=use_cols, error_bad_lines=False,
                             warn_bad_lines=api.config.error_bad_lines)
        else:
            df = pd.read_csv(csv_io, api.config.separator, error_bad_lines=False,
                             warn_bad_lines=api.config.error_bad_lines)
    else:
        att_dict['config']['limit_rows'] = api.config.limit_rows
        if api.config.use_columns and not api.config.use_columns == 'None':
            use_cols = [x.strip() for x in api.config.use_columns.split(',')]
            att_dict['config']['use_columns'] = str(use_cols)
            df = pd.read_csv(csv_io, api.config.separator, usecols=use_cols, nrows=api.config.limit_rows, \
                             error_bad_lines=False, warn_bad_lines=api.config.error_bad_lines)
        else:
            df = pd.read_csv(csv_io, api.config.separator, nrows=api.config.limit_rows, \
                             error_bad_lines=False, warn_bad_lines=api.config.error_bad_lines)

    att_dict['memory']['previous_columns'] = list(df.columns)
    att_dict['memory']['previous_mem_usage'] = df.memory_usage(deep=True).sum() / 1024 ** 2

    if api.config.downcast_int:
        df, dci = downcast(df, 'int', 'unsigned')
        if dci:
            att_dict['memory']['downcast_int'] = dci
    if api.config.downcast_float:
        df, dcf = downcast(df, 'float', 'float')
        if dcf:
            att_dict['memory']['downcast_float'] = dcf

    # check if index is provided and set
    if api.config.index_cols and not api.config.index_cols == 'None':
        index_list = [x.strip() for x in api.config.index_cols.split(',')]
        att_dict['config']['index_cols'] = str(index_list)
        att_dict['index_cols'] = str(index_list)
        df.set_index(index_list, inplace=True)

    att_dict['mem_usage'] = df.memory_usage(deep=True).sum() / 1024 ** 2
    att_dict['columns'] = list(df.columns)
    att_dict['number_columns'] = len(att_dict['columns'])
    att_dict['number_rows'] = len(df.index)
    att_dict['example_row_1'] = str(df.iloc[0, :].tolist())

    return api.Message(attributes=att_dict, body=df)


'''
Mock pipeline engine api to allow testing outside pipeline engine
'''


class test:
    ORDER_HEADERS = 2
    ORDER_DETAILS = 3
    PRODUCTS_MD = 6
    SIMPLE_BINARY = 0
    SIMPLE_STRING = 1
    ORDER_HEADERS_LIMITED = 4
    ORDER_DETAILS_LIMITED = 5
    PRODUCTS_MD_LIMITED = 7


actual_test = test.ORDER_HEADERS

try:
    api
except NameError:
    class api:

        def set_test(test_scenario):
            print('TEST SCENARIO: ' + str(test_scenario))
            if test_scenario == test.ORDER_HEADERS or test_scenario == test.ORDER_HEADERS_LIMITED:
                f = open("/Users/d051079/OneDrive - SAP SE/Datahub-Dev/data/order_headers.csv", mode='r')
                csv = ''
                for line in f.readlines():
                    csv += line
            elif test_scenario == test.ORDER_DETAILS or test_scenario == test.ORDER_DETAILS_LIMITED:
                f = open("/Users/d051079/OneDrive - SAP SE/Datahub-Dev/data/order_details.csv", mode='r')
                csv = ''
                for line in f.readlines():
                    csv += line
            elif test_scenario == test.PRODUCTS_MD or test_scenario == test.PRODUCTS_MD_LIMITED:
                f = open("/Users/d051079/OneDrive - SAP SE/Datahub-Dev/data/products_md.csv", mode='r')
                csv = ''
                for line in f.readlines():
                    csv += line
            elif test_scenario == test.SIMPLE_STRING:
                csv = """col1;col2;col3
                     1;4.4;99
                     2;4.5;200
                     3;4.7;65
                     4;3.2;140
                     """
            else:  # testdata.BINARY_STRING
                csv = b"""col1;col2;col3
                         1;4.4;99
                         2;4.5;200
                         3;4.7;65
                         4;3.2;140
                         """
            attributes = {'format': 'csv',"storage.pathInPolledDirectory" : 'filename'}

            return api.Message(attributes=attributes, body=csv)

        def set_config(test_scenario):
            if test_scenario == test.ORDER_DETAILS:
                api.config.index_cols = "order_id, product_id"
                api.config.separator = ';'
                api.config.error_bad_lines = False
                api.config.use_columns = 'order_id, product_id'
                api.config.limit_rows = 0
                api.config.downcast_int = True
                api.config.downcast_float = True
                api.config.df_name = 'order_details'
            elif test_scenario == test.ORDER_HEADERS:
                api.config.index_cols = "order_id"
                api.config.separator = ';'
                api.config.error_bad_lines = False
                api.config.use_columns = 'order_id, shopper_id,num_products, w_day, hour,location_id, Year,Month, Week'
                api.config.limit_rows = 0
                api.config.downcast_int = True
                api.config.downcast_float = True
                api.config.df_name = 'order_headers'
            elif test_scenario == test.ORDER_DETAILS_LIMITED:
                api.config.index_cols = "order_id, product_id"
                api.config.separator = ';'
                api.config.error_bad_lines = False
                api.config.use_columns = 'order_id, product_id'
                api.config.limit_rows = 100000
                api.config.downcast_int = True
                api.config.downcast_float = True
                api.config.df_name = 'order_details'
            elif test_scenario == test.ORDER_HEADERS_LIMITED:
                api.config.index_cols = "order_id"
                api.config.separator = ';'
                api.config.error_bad_lines = False
                api.config.use_columns = 'order_id, num_products, total_basket, w_day, hour,location_id, Year,Month, Week'
                api.config.limit_rows = 100000
                api.config.downcast_int = True
                api.config.downcast_float = True
                api.config.df_name = 'order_headers'
            elif test_scenario == test.PRODUCTS_MD:
                api.config.index_cols = "product_id"
                api.config.separator = ';'
                api.config.error_bad_lines = False
                api.config.use_columns = 'product_id,category_id'
                api.config.limit_rows = 0
                api.config.downcast_int = True
                api.config.downcast_float = False
                api.config.df_name = 'products_md'
            else:  # testconfig.NO_INDEX:
                api.config.index_cols = "None"
                api.config.separator = ';'
                api.config.error_bad_lines = False
                api.config.use_columns = ''
                api.config.limit_rows = 0
                api.config.downcast_int = False
                api.config.downcast_float = False
                api.config.df_name = 'test_df'

        class config:
            index_cols = "None"
            separator = ';'
            error_bad_lines = False
            use_columns = ''
            limit_rows = 0
            df_name = 'DataFrame'

        class Message:
            def __init__(self, body=None, attributes=""):
                self.body = body
                self.attributes = attributes

        def send(port, msg):
            if isinstance(msg, pd.DataFrame):
                print(msg.body.head(1))
            else:
                print(msg)
            pass

        # called by 'isolated'-test simulation
        def set_port_callback(port, callback):
            msg = api.set_test(actual_test)
            api.set_config(actual_test)
            print("Call \"" + callback.__name__ + "\"  messages port \"" + port + "\"..")
            callback(msg)

        # called by 'integrated/pipeline-test simulation
        def test_call(test_scenario):
            print('EXTERNAL CALL of module:' + __name__)
            msg = api.set_test(test_scenario)
            api.set_config(test_scenario)
            result = process(msg)
            api.send("DataFrame", result)
            return result


def interface(msg):
    result = process(msg)
    api.send("outDataFrameMsg", result)
    info_str = json.dumps(result.attributes, indent=4)
    api.send("Info", info_str)


# Triggers the request for every message
# to be commented when imported for external 'integration' call
#api.set_port_callback("inCSVMsg", interface)
import pandas as pd
import logging
import datetime
import json

nvchar_len = 255
nvchar_list = {10: 15, 40: 50, 70: 100, 200: 255}
# Not used due to SAC issues
maptypes_direct = {'int8': 'TinyINT', 'int16': 'SMALLINT', 'int32': 'Integer', 'int64': 'BIGINT', 'float32': 'REAL',
                   'float64': 'DOUBLE', 'date': 'DATE', 'str': 'NVARCHAR' + '(' + str(nvchar_len) + ')',
                   'datetime64[ns]': 'TIMESTAMP', 'bool': 'BOOLEAN'}
maptypes_direct2 = {'int8': 'TINYINT', 'int16': 'SMALLINT', 'int32': 'INTEGER', 'int64': 'BIGINT', 'float32': 'FLOAT',
                    'float64': 'DOUBLE', 'date': 'DATE', 'str': 'NVARCHAR',
                    'datetime64[ns]': 'TIMESTAMP', 'bool': 'BOOLEAN'}
maptypes_simple = {'int8': 'Integer', 'int16': 'Integer', 'int32': 'Integer', 'int64': 'BIGINT', 'float32': 'DECIMAL',
                   'float64': 'DECIMAL', 'date': 'DATE', 'str': 'NVARCHAR' + '(' + str(nvchar_len) + ')',
                   'datetime64[ns]': 'TIMESTAMP', 'bool': 'BOOLEAN'}


def map_panda_dtypes(dseries, ist, datetime2date=False, map_dict='D'):
    dt = str(dseries.dtype)
    if dt == 'object':
        dt = 'date' if isinstance(ist, datetime.date) else 'str'
    elif dt == 'datetime64[ns]' and datetime2date:
        dt = 'date'
    if dt is 'str' and not map_dict == 'D2':
        max = dseries.str.len().max()
        for key, value in self.nvchar_list.items():
            if max <= key:
                return 'NVARCHAR' + '(' + str(value) + ')'
    else:
        if map_dict == 'S':
            return maptypes_simple[dt]
        elif map_dict == 'D':
            return maptypes_direct[dt]
        elif map_dict == 'D2':
            return maptypes_direct2[dt]
        else:
            logging.warning("Unknown mapping dict '{}', usind 'D'".format(map_dict))
            return maptypes_direct[dt]


def make_sql(df_msg):

    df = df_msg.body

    if not isinstance(df, pd.DataFrame):
        raise TypeError('Message body is not of type <pandas.DataFrame>')

    key_fields = list(df.index.names)

    sql = "CREATE COLUMN TABLE " + api.config.schema + "." + api.config.table_name + '('
    columnkey = list()
    if key_fields and key_fields[0] is not None and api.config.write_index == False:
        for i in key_fields:
            indexvalues = df.index.get_level_values(i)
            ist = indexvalues[0]
            hanatype = map_panda_dtypes(indexvalues, ist, datetime2date=api.config.datetime2date, map_dict=api.config.map_types)
            ck = '\"' + i.upper() + '\"'
            columnkey.append(ck)
            sql += ' ' + ck + ' ' + hanatype + ' NOT NULL ,'

    for col in df.columns:
        logging.debug("Column for dtype: {}".format(col))
        hanatype = map_panda_dtypes(df[col], df[col].iloc[0], map_dict=api.config.map_types)
        logging.debug("Dtype: {}".format(hanatype))
        column = '\"' + col.upper() + '\"'
        sql += ' ' + column + ' ' + hanatype + ' , '
        ### reformat datetime
        if hanatype == 'TIMESTAMP':
            df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d %H:%M:%S')
    if key_fields and key_fields[0] is not None and api.config.write_index == False:
        sql += " PRIMARY KEY("
        for c, i in enumerate(key_fields):
            sql += columnkey[c] + " , "
        sql = sql[:-2] + ")"
    else:
        sql = sql[:-2]
    sql += ");"

    logging.info("Create Table SQL: "  + sql)
    sql_att = {'sql': sql, 'table': api.config.table_name, 'schema': api.config.schema}
    sql_msg = api.Message(body=sql, attributes=sql_att)

    if api.config.write_index == False :
        df.reset_index(inplace=True)
    df_dict = df.to_dict(orient='records')
    df_j = json.dumps(df_dict)

    df_att = {'data format': 'json'}
    data_msg = api.Message(body=df_j, attributes=df_att)

    return sql_msg, data_msg


'''
Mock pipeline engine api to allow testing outside pipeline engine
'''
try:
    api
except NameError:
    class api:

        class config:
            write_index = False
            table_name = 'table'
            schema = 'schema'
            datetime2date = False
            map_types = 'D2'

        class Message:
            def __init__(self,body = None,attributes = ""):
                self.body = body
                self.attributes = attributes

        def send(port, msg):
            print(msg.body)

        def set_port_callback(port, callback):

            #test input
            df = pd.DataFrame({'icol': [1, 2,3,4,5], 'xcol2': ['A', 'B','C','D','E'],'xcol3': ['K', 'L','M','N','O']})

            att = {'format': 'DataFrame'}
            msg = api.Message(body=df, attributes=att)

            print("Call \"" + callback.__name__ + "\" to simulate behavior when messages arrive at port \"" + port + "\"..")
            callback(msg)



def interface(df_msg):
    sql_msg, data_msg = make_sql(df_msg)
    api.send("sqlMsg", sql_msg)
    api.send("dataMsg",data_msg)


# Triggers the request for every message (the message provides the stock_symbol)
api.set_port_callback("DataFrameMsg", interface)


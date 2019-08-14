import pandas as pd

def merge(left_msg,right_msg):

    left_df = left_msg.body
    right_df = right_msg.body

    if api.config.on_index :
        df = pd.merge(left_df, right_df, how=api.config.how, left_index=True,right_index=True)
    elif api.config.left_on and api.config.right_on :
        left_df.reset_index(inplace=True)
        right_df.reset_index(inplace=True)
        df = pd.merge(left_df, right_df, how=api.config.how, left_on=api.config.left_on,right_on=api.config.right_on)
    else :
        raise ValueError("Config setting: Either <on> or both <left_on> and <right_on> has to be set in order to join the dataframes")

    if api.config.new_indices :
        index_list = [x.strip() for x in api.config.new_indices.split(',')]
        df.set_index(keys = index_list,inplace=True)

    if api.config.drop_columns :
        col_list = [x.strip() for x in api.config.drop_columns.split(',')]
        df.drop(labels = col_list,axis=1,inplace=True)


    return api.Message(attributes={'format':'pandas DataFrame'},body = df)



'''
Mock pipeline engine api to allow testing outside pipeline engine
'''
try:
    api
except NameError:
    class api:

        class config:
            how = "inner"
            on_index = False
            left_on ="xcol2"
            right_on = "ycol2"
            new_index ="icol_x"
            drop_columns = 'icol_y'         # drops columns after merge

        class Message:
            def __init__(self,body = None,attributes = ""):
                self.body = body
                self.attributes = attributes

        def send(port, msg):
            print(msg.body)

        def set_port_callback(port, callback):

            #test input
            dl = pd.DataFrame({'icol': [1, 2,3,4,5], 'xcol2': ['A', 'B','C','D','E'],'xcol3': ['K', 'L','M','N','O']})
            dl.set_index(keys='icol',inplace=True)
            dr = pd.DataFrame({'icol': [3, 4, 5,6,7], 'ycol2': ['C', 'D', 'E','F','G'],'ycol3': ['M','N','O','P','Q']})
            dr.set_index(keys='icol', inplace=True)

            att = {'format': 'pandas'}
            print("Call \"" + callback.__name__ + "\" to simulate behavior when messages arrive at port \"" + ', '.join(port) + "\"..")
            callback(api.Message(body=dl, attributes=att),api.Message(body=dr, attributes=att))


def interface(left_msg,right_msg):
    result_df = merge(left_msg,right_msg)
    api.send("DataFrameMsg", result_df)


# Triggers the request for every message (the message provides the stock_symbol)
api.set_port_callback(["leftDFMsg","rightDFMsg"], interface)


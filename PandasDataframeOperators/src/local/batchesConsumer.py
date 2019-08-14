
import sys
import json

csv_str = ""

def on_input(msg):

    global csv_str

    if not isinstance(msg,api.Message) :
        raise TypeError('Inport data has be of type <api.Message>')

    csv_str += msg.body

    if msg.attributes['counter']+1 == msg.attributes['size'] :
        return api.Message(attributes={'format':'csv','operator':'batchesConsumer'},body=csv_str)
    else :
        return {'format': 'csv','counter':msg.attributes['counter'],'size':msg.attributes['size'],'operator':'batchesConsumer'}


'''
Mock pipeline engine api to allow testing outside pipeline engine
'''


class test:
    SIMPLE_STR = 0
    SIMPLE_BYTE = 1
    ORDER_HEADERS = 2
    SIMPLE_ARRAY = 3


test_scenario = test.ORDER_HEADERS

try:
    api
except NameError:
    class api:
        # input data
        def set_test(test_scenario):
            msg_list = list()
            max = 100
            for i in range(0, max) :
                msg_list.append(api.Message(attributes={'counter':i,'size':max},body = str(i) + '\n'))

            return msg_list

        def set_config(test_scenario):
            pass

        class config:
            nothing = True

        class Message:
            def __init__(self, body=None, attributes=""):
                self.body = body
                self.attributes = attributes

        def send(port, msg):
            if isinstance(msg,api.Message) :
                print('attributes: \n{}'.format(msg.attributes))
                print('body: \n{}'.format(msg.body))
            else :
                print(msg)

        def set_port_callback(port, callback):
            print("Call \"" + callback.__name__ + "\"  messages port \"" + port + "\"..")
            msg_list = api.set_test(test_scenario)
            api.set_config(test_scenario)
            for msg in msg_list :
                callback(msg)

        # called by 'integrated/pipeline-test simulation
        def test_call(msg):
            print('EXTERNAL CALL of module:' + __name__)
            api.set_config(test_scenario)
            result = on_input(msg)
            api.send("outDataFrameMsg", result)
            return result


def interface(msg):
    msg_out = on_input(msg)
    if isinstance(msg_out,api.Message) :
        api.send("outCSVMsg", msg_out)
        info_str = json.dumps(msg_out.attributes, indent=4)
        api.send('Info',info_str)
    else :
        info_str = json.dumps(msg_out, indent=4)
        api.send('Info',info_str)

# Triggers the request for every message (the message provides the stock_symbol)
api.set_port_callback("inCSVMsg", interface)


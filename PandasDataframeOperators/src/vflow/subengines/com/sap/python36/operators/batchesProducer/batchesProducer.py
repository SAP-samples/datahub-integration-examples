
import sys
import json

MAX_MEM = 10000000

def process(msg):

    if isinstance(msg,api.Message) :
        if isinstance(msg.body, str):
            csv_str = msg.body
        elif isinstance(msg.body, bytes):
            csv_str = msg.body.decode("utf-8")
        else:
            raise TypeError('Message body has unsupported type' + str(type(msg.body)))
    else :
        if isinstance(msg,str) :
            csv_str = msg
        else :
            raise TypeError('Inport data has unsupported type' + str(type(msg)))

    max_mem = MAX_MEM if api.config.max_memory == 0 else api.config.max_memory

    mem = sys.getsizeof(csv_str)
    part_size = int(len(csv_str) / (mem / max_mem) ) # size of parts

    #print('Memory: {} - Len of String: {} - Max memory: {}'.format(mem, len(csv_str), max_mem))
    parts = [csv_str[i:i + part_size] for i in range(0, len(csv_str), part_size)]

    # test only - to be commented
    #for p in parts :
    #    print(p)

    return parts


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
            if test_scenario == test.ORDER_HEADERS:
                with open('/Users/d051079/OneDrive - SAP SE/Datahub-Dev/data/order_headers.csv', 'r') as file:
                    csv = file.read()
            elif test_scenario == test.SIMPLE_BYTE :
                csv = b"col1;col2;col3\n" + \
                        b"1;4.4;99\n" + \
                        b"2;4.5;200\n" + \
                        b"3;4.7;65\n" + \
                        b"4;3.2;140"
            elif test_scenario == test.SIMPLE_STR :
                csv = "col1;col2;col3\n" + \
                        "1;4.4;99\n" + \
                        "2;4.5;200\n" + \
                        "3;4.7;65\n" + \
                        "4;3.2;140\n"
            else :
                csv = ''
                for i in range(0, 101) :
                    csv = csv + str(i) + '\n'
                print(csv)
            att_dict = {'format': 'csv', 'name': 'isolated_test'}

            return api.Message(attributes=att_dict, body=csv)

        def set_config(test_scenario):
            if test_scenario == test.ORDER_HEADERS:
                api.config.max_memory = 0
            else:  # SIMPLE
                api.config.max_memory = 13

        class config:
            max_memory = 0  # bytes

        class Message:
            def __init__(self, body=None, attributes=""):
                self.body = body
                self.attributes = attributes

        def send(port, msg):
            if isinstance(msg,api.Message) :
                print('Batch no: {}  of memory size: {}'.format(msg.attributes['counter'],sys.getsizeof(msg.body)))
            else :
                print('Info: {}'.format(msg))

        def set_port_callback(port, callback):
            print("Call \"" + callback.__name__ + "\"  messages port \"" + port + "\"..")
            msg = api.set_test(test_scenario)
            api.set_config(test_scenario)
            callback(msg)

        # called by 'integrated/pipeline-test simulation
        def test_call(msg):
            print('EXTERNAL CALL of module:' + __name__)
            api.set_config(test_scenario)
            result = process(msg)
            api.send("outDataFrameMsg", result)
            return result


def interface(msg):
    batch_array = process(msg)
    for i,b in enumerate(batch_array) :
        att_dict = {'counter': i, 'size': len(batch_array),'memory_batch':sys.getsizeof(b),'memory_total':sys.getsizeof(batch_array),'operator':'batchesProducer'}
        api.send("outCSVMsg", api.Message(attributes=att_dict,body=b))

        info_str = json.dumps(att_dict, indent=4)
        api.send('Info',info_str)


    # for test only  - tbcommented
    #csv_str = ''.join(batch_array)
    #print(csv_str)
    # test to save for a diff test
    #with open("/Users/d051079/OneDrive - SAP SE/Datahub-Dev/data/order_headers2.csv", "w") as text_file:
    #    text_file.write(csv_str)
    #text_file.close()



# Triggers the request for every message (the message provides the stock_symbol)
api.set_port_callback("inCSVMsg", interface)


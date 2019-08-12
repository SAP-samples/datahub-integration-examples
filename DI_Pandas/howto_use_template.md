# Usage of Template

The pandas package provides a wide range of functionalities to process big data. It makes a lot of sense to create simple operators like the ones created in the di_pandas solution that cover procedures often needed in a pipeline. Nevertheless, the existing operators will never be suffice for most pipelines and therefore a guideline and template for implementing new python scripts in a new operator could save a lot of time. In addition some tips how to develop and test them locally might further increase the efficiency. 

For a short tutorial of how to create custom python operators have look to the blog of Jens: https://blogs.sap.com/2018/01/23/sap-data-hub-develop-a-custom-pipeline-operator-with-own-dockerfile-part-3/

As an example for how to use the *di_pandas* operators for preparing a data set for machine learning: 

![Example pipeline: Create POS](images/CreatePOS_pipeline.png)

The template *di_template.py* covers the most simple case of receiving 1 message the inport and sending 1 resulting message to the outport. In order to meddle not too much into the code the following naming conventions are recommended: 

* **inport** : inDataFrameMsg, 
	* data type: message
		* body: reference to DataFrame
		* attributes: dictionary with DataFrame profile
* **outport** : 
	* outDataFrameMsg
		* data type: message
			* body: reference to DataFrame
			* attributes: dictionary with DataFrame profile	
	* Info 
		* data type: string, containing at least the string converted attributes but could be enhanced with further instructive debugging information. 
		

## Core elements
The core elements are mandatory for a custom python operator
* **process** (name of the function could freely be chosen) contains the core data manipulation script
* **interface** Gets the data from the inport(s), calls the main processing function and finally sends the result to the outport(s)
* **api.set_port_callback** Connects the interface function with the inport. 

### process
The data manipulation is placed in the process function. Firstly it checks if the body actually contains a reference to a DataFrame type. This follows by the script, e.g. creating a sample of the data in the DataFrame using the configuration paramaters *sample_size* and *random_seed*. Finally some basic DataFrame characteristics are stored in the attributes.  

```python
def process(msg):

    # test if body refers to a DataFrame type
    df = msg.body
    if not isinstance(df,pd.DataFrame) :
        raise TypeError(‘Message body does not contain a pandas DataFrame’)

    #####################
    #  pd operations
    #####################
    #example
    df = df.sample(n = api.config.sample_size,random_state=api.config.random_state)

    #####################
    #  final infos to attributes and info message
    #####################
    prev_att = msg.attributes
    att_dict = dict()
    att_dict[‘config’] = dict()

    # df from body
    att_dict[‘operator’] = ‘template’ # name of operator
    att_dict[‘mem_usage’] = df.memory_usage(deep=True).sum() / 1024 ** 2
    att_dict[‘name’] = prev_att[‘name’]
    att_dict[‘columns’] = list(df.columns)
    att_dict[‘number_columns’] = len(att_dict[‘columns’])
    att_dict[‘number_rows’] = len(df.index)
    att_dict[‘example_row_1’] = str(df.iloc[0, :].tolist())

    return api.Message(attributes=att_dict,body = df)
```
    
### interface
The gateway that gets the data from the inport(s) and sents the result to the outport(s). If more than one inport is defined the arguments needs to be extended accordingly. If you stick to the naming conventions and the number of inport and outports do not change, nothing has to modified.  

```python
def interface(msg):  # interface(msg1, msg2)
    result = process(msg)  #  result = process(msg1, msg2)
    api.send(“outDataFrameMsg”, result)
    info_str = json.dumps(result.attributes, indent=4)
    api.send(“Info”, info_str)
```

### api.set_port_callback
Connects the interface function with the inport. If more than one inport is necessary a list of inports has to be provided. If you stick to the naming conventions and the number of inport and outports do not change, nothing has to modified.  

```python
api.set_port_callback(“inDataFrameMsg”, interface) 
#api.set_port_callback([“DFMsg1”,”DFMsg2”], interface)
```

## Elements for local development 
For being able to develop, debug and test the script locally the module structure of **api.config* and **api.Message** has to be emulated as well as the functions **api.send** called by interface and the definition of **api.set_port_callback**. 
The **config** structure needs to reflect the variable names specified in the later operator configuration. This needs to be adapted for each new operator. For all other definitions you are free depending only on how and what you like to test.  

```python
class api:
	# fake definition of api.Message
	class config : 
        random_state = 1  # integer
        sample_size = 2  # integer

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
            print(msg.body)
        
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
```

For keeping this code segment when uploading the script to a DI instance and later avoid naming conflicts you need to capsulate it by the following 

```python
try:
    api
except NameError:
```
Only if the package api is not known the ```class api``` is interpreted. 

## Testing locally
Even for small scripts it is always a good practise to define a couple of test cases that could be run whenever the code has been changed to preserve the healthiness of the code. 
I am doing this by defining a class with speaking variable names as integers and then assigning them to the variable *test_scenario*:

```python
class test :
    BIGDATA = 1
    SIMPLE = 0

test_scenario = test.SIMPLE
```

These test scenarios I have to implement and assign. A straightforward way is to define the functions ```set_config``` for setting the configuration and ```set_test``` for creating the input data and implementing all test cases. 

```python
	# input data - only used for isolated testing
   def set_test(test_scenario):
       if test_scenario == test.BIGDATA :
           df = pd.read_csv("/Users/madmax/big_data/test1.csv",sep=';')
           df.set_index(keys='index', inplace=True)

       else :
           df = pd.DataFrame({'icol': [1, 2, 3, 4, 5], 'xcol2': ['A', 'B', 'C', 'D', 'E'], 'xcol3': ['K', 'L', 'M', 'N', 'O']})
           df.set_index(keys='icol', inplace=True)

            # input data
            att = {'format': 'pandas','name':'test'}

            return api.Message(attributes=att,body=df)

    # setting test config data
    def set_config (test_scenario) :
        if test_scenario == test.BIGDATA :
            random_state = 1 # integer
            sample_size = 2000 # integer
        else :  # test_scenario == test.SIMPLE:
            random_state = 3 # integer
            sample_size = 2 # integer
```

## Integration test
If you like to test a kind of integrated scenario you need to define another function that can be called by a pipeline.py script. Be aware when importing the modules you need to comment out the function call ```api.set_port_callback``` otherwise it will be excuted when been imported. Please let me know if you know a less error-prone approach because after your successful 'integration'-test you always forget to remove the '#' in all the modules. 

```python
	# called by 'integrated/pipeline-test simulation
   def test_call(msg):
        print('EXTERNAL CALL of module:' + __name__)
        api.set_config(test_scenario)
        result = process(msg)
        # because when called locally via this function, 'api.set_port_callback' and 'interface' are not called
        api.send("DataFrame",result)
        return result
```    

The pipeline.py script could like the following. 

```python
import fromCSVDataFrame as fromcsv
import joinDataFrames as joindf
import toCSVDataFrame as tocsv
import selectDataFrame as selectdf

import json


msg_oh  = fromcsv.api.test_call(fromcsv.test.ORDER_HEADERS)
info_str = json.dumps(msg_oh.attributes, indent=4)
print(info_str)

msg_od  = fromcsv.api.test_call(fromcsv.test.ORDER_DETAILS)
info_str = json.dumps(msg_od.attributes, indent=4)
print(info_str)

msg = joindf.api.test_call(msg_oh,msg_od)
info_str = json.dumps(msg.attributes, indent=4)
print(info_str)

msg = selectdf.api.test_call(msg)
info_str = json.dumps(msg.attributes, indent=4)
print(info_str)

csv = tocsv.api.test_call(msg)
with open(r"/Users/d051079/Downloads/test.txt", 'w') as fd:
    if isinstance(csv.body,list) :
        for s in csv.body :
            fd.write(s)
    else :
        fd.write(csv.body)
fd.close()
```


## Final template

```python
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
api.set_port_callback("inDataFrameMsg", interface)


``



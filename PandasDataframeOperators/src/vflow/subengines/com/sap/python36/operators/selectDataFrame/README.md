#selectDataFrame
Selecting data records based on column data restrictions (= SELECT * FROM ... WHERE COLX = x AND ...) of numeric types and lists of data. 

## Input
* **inDataFrame**

## Output
* **outDataFrame**
* **Info**

## Config
* **selection_num** -string- Selection criteria for numerical columns. Comparison operators: ['=', '>', '<', '!' or '!=' ]. Example: 'order_id < 100000'  

* **selection_list** -string- Inclusion or exclusion list of values for numerical and string column.  Comparison operators: ['=', '!' or '!=' ]. Example: 'trans_date = 2016-03-03, 2016-02-04 '  

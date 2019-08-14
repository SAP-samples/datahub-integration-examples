# joinDataFrame
Joining 2 DataFrames using either the indices of both or on specified columns. Setting the new index ist necessary. 

## Input
* **leftDFMsg**
* **rightDFMsg**

## Output
* **outDataFrame**
* **Info**

## Config
* **how** -string-  possible values: ‘left’, ‘right’, ‘outer’, ‘inner’
* **on_index** -boolean-- If true the 2 DataFrames are joined using the indices (not tested yet with multiple indices)
* **left_on** -string-  Name of column of leftDF that is joined with name of column of rightDF
* **right_on** -string-
* **new_indices** -string- New index or multiple indices for the joined DataFrame
* **drop_columns** -string- List of columns of the joined DataFrame that could be dropped. 

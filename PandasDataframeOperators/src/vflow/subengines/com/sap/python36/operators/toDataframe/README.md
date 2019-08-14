# fromCSVDataFrame
Creating a DataFrame with csv-data passed through inport. 

## Input
**inCSVMsg* (message) providing the string or byte-code of csv data structure. Operator tests the data type. 

## Output
* **outDataFrameMsg** -message- 
* **Info** -string-

## Config
* **index_cols** -string-  the index of the DataFrame
* **separator** -string- separator of the csv data (default = ; )
* **error_bad_lines** -boolean- When True raises error on bad lines
* **use_columns** -string- list of column names that should be used. All other columns are dropped
* **limit_rows** -integer- limits the number of read rows. Useful for the development phase 
* **downcast_int** -boolean- downcasts the (default) int64 data type of columns to minimum possible based on the values in the column. CAUTION: if later in the pipeline process appended data needs types with bigger memory footprint, an error is raised
* **downcast_float** -boolean- downcasts the (default) float64 data type of columns to float32 if permitted by the values in the column. CAUTION: if later in the pipeline process appended data needs types with bigger memory footprint, an error is raised
* **df_name** -string- name of the DataFrame for monitoring or saving purpose. WARNING: the name 'DataFrame' is overwritten when a filename is passed in the attributes.  
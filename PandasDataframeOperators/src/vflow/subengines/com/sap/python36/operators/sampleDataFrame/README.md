# sampleDataFrame
## Input
* **inDataFrameMsg**

## Output
* **outDataFrame**
* **Info**

## Config#
* **sample_size** -integer- size of sample
* **random_state** - integer- initializing random number generator
* **invariant_column** -string- Column that values should be kept and not split in a sample, e.g. all records of a customer should be in a sample, basically sampling over customers. Because not all the values of the invariant_columns have the same number of records the average is taken to approximate the sample_size. 
	

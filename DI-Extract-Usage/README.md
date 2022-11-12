# Extract DI Pipeline Usage
This is the source code for the blog post: [Analyzing SAP Data Intelligence Pipeline Usage: From REST API to SAC](url)
![b1-3](https://user-images.githubusercontent.com/109061211/201470709-b608038c-c9e7-49dd-8ddf-61d5417bf8a4.png)

## Contents
**1. Custom operators**
  - **Get Users**: fetch the user list of a DI tenant with DI API endpoint ‘/auth/v2/user’.
  - **Get Runtime Graphs**: retrieve executed pipeline details such as graph name, status, and substitutions with DI API endpoint ‘/v1/runtime/graphsquery’.
  - **Get Graph Data sources**: fetch information about target data sources set in operators in a pipeline with DI API endpoint ‘/v1/runtime/graphdescriptions/{handle}’.
  - **Get Datasource Pairs**: generate pairs of data sources that were used together in each pipeline.

**2. Graph** 
  - **Extract Pipeline Usage**: extract DI pipeline usage of users in a DI tenant and store the data in DWC

**3. Vtypes**: represent a structure for connectionID and tables for user and graph information


## How to Run
1. Import extract.pipeline.usage-1.0.0.zip via `SAP Data Intelligence System Management` -> `Files` -> `Import Solution`
2. Open a graph `Extract Pipeline Usage` in `Modeler`
3. Configure the connectionID in `Get User` and target tables in `Table Producer`.
4. Start the graph and check the target tables once the graph is completed.

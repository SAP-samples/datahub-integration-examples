# datahub-integration-examples
This repository contains example operators, pipelines and dockerfiles for [SAP Data Hub](https://www.sap.com/products/data-hub.html)  showing how to connect to different sources or how to perform certain tasks.

## Requirements

In order to be able to deploy and run the examples, the following requirements need to be fulfilled:

- SAP Data Hub On-Premise or Cloud edition

## Run examples

....

## Examples

1. [HANA_exposed_via_OpenAPIServer](/HANA_exposed_via_OpenAPIServer): Expose an SAP HANA database through an OpenAPI server operator
2. [HiveOperator](/HiveOperator): Provides functionality to query a Hive Metastore server using a HiveQL string 
3. [JavaProcessExecutor](/JavaProcessExecutor): Run a Java Application and pass custom configuration paramaters using a Process Executor Operator
4. [ParquetWriterOperator](/ParquetWriterOperator): This custom operator creates a file in Parquet format from an input message

## How to get support
If you need help please post your questions to ???.
In case you found a bug please open a [Github Issue](https://github.com/SAP/datahub-integration-examples/issues).

## License

[LICENSE file](LICENSE).

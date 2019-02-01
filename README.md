# datahub-integration-examples
This repository contains example operators, pipelines and dockerfiles for [SAP Data Hub](https://www.sap.com/products/data-hub.html)  showing how to connect to different sources or how to perform certain tasks.

## Requirements

In order to be able to deploy and run the examples, the following requirements need to be fulfilled:

- SAP Data Hub 2.3 or later installed on a supported [platform](https://support.sap.com/content/dam/launchpad/en_us/pam/pam-essentials/SAP_Data_Hub_2_PAM.pdf)

or

- SAP Data Hub, [trial edition 2.3](https://blogs.sap.com/2018/04/26/sap-data-hub-trial-edition/)

## Run examples

The source codes required for building and running the examples are contained in the `src/` folder within each example. Moreover, a solution archive is available within the `solution/` folder of each example. A [solution](https://blogs.sap.com/2018/12/05/building-sap-data-hub-solutions-aka-vsolutions/) is a self-contained archive that includes all artefacts that are required to build and run an example. The solutions can be imported via `SAP Data Hub System Management` -> `Files` -> `Import Solution`. Please refer to the `README.md` of the respective examples how to run the example after the solution has been imported successfully.

## Examples

1. [HANA_exposed_via_OpenAPIServer](/HANA_exposed_via_OpenAPIServer): Expose an SAP HANA database through an OpenAPI server operator
2. [HiveOperator](/HiveOperator): Provides functionality to query a Hive Metastore server using a HiveQL string 
3. [JavaProcessExecutor](/JavaProcessExecutor): Run a Java Application using a Process Executor Operator
4. [ParquetWriterOperator](/ParquetWriterOperator): This custom operator creates a file in Parquet format from an input message

## How to get support
If you need help please post your questions to ???.
In case you found a bug please open a [Github Issue](https://github.com/SAP/datahub-integration-examples/issues).

## License

[LICENSE file](LICENSE).

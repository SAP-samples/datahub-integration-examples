# SAP Data Hub Integration Examples

## Description

This repository contains example operators, pipelines and dockerfiles for [SAP Data Hub](https://www.sap.com/products/data-hub.html)  showing how to connect to different sources or how to perform certain tasks.

## Requirements

In order to be able to deploy and run the examples, the following requirements need to be fulfilled:

- SAP Data Hub 2.3 or later installed on a supported [platform](https://support.sap.com/content/dam/launchpad/en_us/pam/pam-essentials/SAP_Data_Hub_2_PAM.pdf) or SAP Data Hub, [trial edition 2.3](https://blogs.sap.com/2018/04/26/sap-data-hub-trial-edition/)

## Download and Installation

To download and use the examples just clone this repository via e.g. `git clone https://github.com/SAP/datahub-integration-examples` or
 download the complete repository as ZIP file from [here](https://github.com/SAP/datahub-integration-examples/archive/master.zip).

After cloning or downloading the repository, navigate into the desired example folder (for example `HiveOperator/`). Each example comes with a solution archive within the folder `solution/`. A [solution](https://blogs.sap.com/2018/12/05/building-sap-data-hub-solutions-aka-vsolutions/) is a self-contained archive that includes all artefacts that are required to run the example. The solutions can be imported into SAP Data Hub via `SAP Data Hub System Management` -> `Files` -> `Import Solution`.

For details on how to configure and run the examples after the solution has been imported, please refer to the `README.md` in the corresponding example directory.

## Examples

1. [HANA_exposed_via_OpenAPIServer](/HANA_exposed_via_OpenAPIServer): Expose an SAP HANA database through an OpenAPI server operator
2. [HiveOperator](/HiveOperator): Provides functionality to query a Hive Metastore server using a HiveQL string 
3. [JavaProcessExecutor](/JavaProcessExecutor): Run a Java Application using a Process Executor Operator
4. [ParquetWriterOperator](/ParquetWriterOperator): This custom operator creates a file in Parquet format from an input message

## Known Issues

- In cases where errors appear after importing the solutions archive of an example, please try to re-create your Modeler Instance.

## How to get support

If you need help or in case you found a bug please open a [Github Issue](https://github.com/SAP/datahub-integration-examples/issues).

## License

Copyright (c) 2019 SAP SE or an SAP affiliate company. All rights reserved.
This project is licensed under the SAP Sample Code License except as noted otherwise in the [LICENSE file](LICENSE).

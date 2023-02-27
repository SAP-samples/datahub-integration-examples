[![REUSE status](https://api.reuse.software/badge/github.com/SAP-samples/datahub-integration-examples)](https://api.reuse.software/info/github.com/SAP-samples/datahub-integration-examples)

# SAP Data Hub & Intelligence Integration Examples

## Description

This repository contains example operators, pipelines, dockerfiles, and best practice guides for [SAP Data Hub](https://www.sap.com/products/data-hub.html)
and [SAP Data Intelligence](https://www.sap.com/products/data-intelligence.html). Amongst others, they show how to integrate with different systems, implement custom operators, and employ best coding practices.

Before you start with the examples, please make sure that:

- You are familiar with the basic concepts of SAP Data Hub/Intelligence Modeling such Pipelines (Graphs), Operators and Dockerfiles.  For more information, you may refer to the Modeling Guide for SAP Data Hub/Intelligence that is available on the SAP Help Portal (https://help.sap.com/viewer/p/SAP_DATA_HUB, https://help.sap.com/viewer/product/SAP_DATA_INTELLIGENCE/Cloud/en-US).
- You are familiar with the basic concepts of Docker (https://docs.docker.com/get-started/) and Kubernetes (https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/).

## Requirements

In order to be able to deploy and run the examples, the following requirements need to be fulfilled:

- SAP Data Hub 2.3 or later installed on a supported [platform](https://support.sap.com/content/dam/launchpad/en_us/pam/pam-essentials/SAP_Data_Hub_2_PAM.pdf) or SAP Data Hub, [trial edition 2.3](https://blogs.sap.com/2018/04/26/sap-data-hub-trial-edition/)

- SAP Data Intelligence 3.0 or later (either cloud or on-premise version)

Please refer to each sub-project for specific platform requirements.

## Download and Installation

To download the examples just download the complete repository as ZIP file from [here](https://github.com/SAP/datahub-integration-examples/archive/master.zip).

After downloading, extract the ZIP file and navigate into the desired example folder (for example `HiveOperator/`). Each example comes with a solution archive within the folder `solution/`. A [solution](https://blogs.sap.com/2018/12/05/building-sap-data-hub-solutions-aka-vsolutions/) is a self-contained archive that includes all artefacts that are required to run the example. The solution archives can be imported into SAP Data Hub via `SAP Data Hub System Management` -> `Files` -> `Import Solution`.

For details on how to configure and run the examples after the solution has been imported, please refer to the `README.md` in the corresponding example directory.


## Examples

| Name                                                              | Description                                                |
|-------------------------------------------------------------------|------------------------------------------------------------|
| [Application Integration Example Scenario](/AppIntegrationExample)| Exemplifies how to extract, store, transform, and analyse data from several SAP applications for 360° customer view. |
| [Git Workflow and CI/CD Process](./GitWorkflow)                    | Shows how to develop solutions using Git and implement a CI/CD Process |
| [HANA_exposed_via_OpenAPIServer](/HANA_exposed_via_OpenAPIServer) | Expose an SAP HANA database through an OpenAPI server operator |
| [HiveOperator](/HiveOperator)                                     | Provides functionality to query a Hive Metastore server using a HiveQL string |
| [JavaProcessExecutor](/JavaProcessExecutor)                       | Run a Java Application using a Process Executor Operator |
| [ParquetWriterOperator](/ParquetWriterOperator)                   | This custom operator creates a file in Parquet format from an input message |
| [Qualtrics Survey integration](/QualtricsIntegration)                   | Custom operators to extract survey responses from Qualtrics |
| [Parallelisation Method Examples](/ParallelisationGuideExamples)                   | Example Graphs showing different possible parallelisation methods in SAP Data Intelligence |

## Known Issues

- In cases where errors appear after importing the solutions archive of an example, please try to re-create your Modeler Instance.

## How to get support

If you need help or in case you found a bug please open a [Github Issue](https://github.com/SAP/datahub-integration-examples/issues).

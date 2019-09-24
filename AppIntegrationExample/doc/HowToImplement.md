# Implementing the scenario

## Requirements

In order to set up and run the complete scenario in your landscape you need

- [SAP Data Hub](https://www.sap.com/products/data-hub.html)
- [SAP HANA](https://www.sap.com/products/hana.html)
- [SAP Analytics Cloud](https://www.sap.com/products/cloud-analytics.html)
- [SAP Marketing Cloud](https://www.sap.com/products/crm/marketing.html)
- [SAP Cloud for Customer](https://www.sap.com/products/cloud-customer-engagement.html)
- [SAP S/4 HANA](https://www.sap.com/products/s4hana-erp.html)
- [Amazon S3](https://aws.amazon.com/s3)

Depending on your requirements you may want to use only parts of the scenario; only SAP Data Hub is mandatory.

## Implementation

Implement the scenario by

1. [importing the solution](#importing-the-solution) containing the scenario in SAP Data Hub,
2. [setting up the connections](#setting-up-connections) from SAP Data Hub to the source and target systems,
3. [connecting SAP Analytics Cloud](#connecting-sap-analytics-cloud-to-sap-hana) to SAP HANA
4. running the pipelines to [extract](HowToExtract.md) and [transform](HowToTransform.md) the data,
5. using SAP Analytics Cloud to [analyse](HowToAnalyse.md) the data.

### Importing the solution

Once you have downloaded or cloned the [data-integration-examples](https://github.com/SAP/datahub-integration-examples) repository import the Application Integration Example solution into SAP Data Hub as described [here](https://github.com/SAP/datahub-integration-examples#download-and-installation). Alternatively you can download the solution archive [here](/solution).

#### Content

1. Graphs for extracting data from SAP Cloud for Customer into SAP HANA:<br> [/src/content/files/vflow/graphs/com/appInt/odata2hana/c4c](/src/content/files/vflow/graphs/com/appInt/odata2hana/c4c)
2. Graphs for extracting data from SAP Marketing Cloud into SAP HANA:<br> [/src/content/files/vflow/graphs/com/appInt/odata2hana/mc](/src/content/files/vflow/graphs/com/appInt/odata2hana/mc)
3. Graphs for extracting data from SAP S/4 HANA into SAP HANA:<br> [/src/content/files/vflow/graphs/com/appInt/odata2hana/s4](/src/content/files/vflow/graphs/com/appInt/odata2hana/s4)
4. Graphs for extracting data from SAP Cloud for Customer into Amazon S3:<br> [/src/content/files/vflow/graphs/com/appInt/odata2s3/c4c](/src/content/files/vflow/graphs/com/appInt/odata2s3/c4c)
5. Graphs for extracting data from SAP Marketing Cloud into Amazon S3:<br> [/src/content/files/vflow/graphs/com/appInt/odata2s3/mc](/src/content/files/vflow/graphs/com/appInt/odata2s3/mc)
6. Graphs for extracting data from SAP S/4 HANA into Amazon S3:<br> [/src/content/files/vflow/graphs/com/appInt/odata2s3/s4](/src/content/files/vflow/graphs/com/appInt/odata2s3/s4)
7. Graphs for working with file data in Amazon S3:<br> [/src/content/files/vflow/graphs/com/appInt/odata2s3/util](/src/content/files/vflow/graphs/com/appInt/odata2s3/util)

### Setting up connections

Download [this file](/src/connections/connections.json) and import the connections in SAP Data Hub `Connection Management`. During import you will need to provide the appropriate connection credentials and to prefix the OData endpoints with the appropriate host URLs in your system landscape. This will create the following connections:

Connection Id | Description | Type | OData endpoint
--------------|-------------|------|---------------
APPINT_C4C | SAP Cloud for Customer Generic API | ODATA | [/sap/c4c/odata/v1/c4codataapi/](https://help.sap.com/viewer/1364b70b9cbb417ea5e2d80e966d4f49/1908/en-US/6c0a463cc9ca450cbd01a9a5057ce682.html)
APPINT_MC_CONTACTS | SAP Marketing Cloud Interaction Contacts | ODATA | [/sap/opu/odata/sap/API_MKT_INTERACTION_CONTACT_SRV/](https://api.sap.com/api/API_MKT_INTERACTION_CONTACT_SRV/overview)
APPINT_MC_INTERACT | SAP Marketing Cloud Interactions | ODATA | [/sap/opu/odata/sap/API_MKT_INTERACTION_SRV/](https://api.sap.com/api/API_MKT_INTERACTION_SRV/overview)
APPINT_S4_BUPA | SAP S/4 HANA Business Partners  | ODATA | [/sap/opu/odata/sap/API_BUSINESS_PARTNER/](https://api.sap.com/api/API_BUSINESS_PARTNER/overview)
APPINT_S4_CUSTRET | SAP S/4 HANA Customer Returns | ODATA | [/sap/opu/odata/sap/API_CUSTOMER_RETURN_SRV/](https://api.sap.com/api/API_CUSTOMER_RETURN_SRV/overview)
APPINT_DH_VORA | SAP Data Hub built-in VORA Database | VORA | n/a
APPINT_HANA | SAP HANA Database | HANA_DB | n/a
APPINT_S3 | Amazon S3 File Storage | S3 | n/a

Again, you may want to use only parts of the scenario. In this case, of course, you only need to import the connections that are relevant for your requirements.

### Connecting SAP Analytics Cloud to SAP HANA

The connection from SAP Analytics Cloud to SAP HANA requires the storage of certificates for both SAP HANA as well as SAP Analytics Cloud in your SAP HANA instance.
  
The following pre-requisites for HANA Live connection have to be fulfilled:
- https://www.sapanalytics.cloud/wp-content/uploads/2017/10/SAP-HANA.pdf
- https://assets.sapanalytics.cloud/production/help/help-release/en/58c890e1c89d41e69b2cec31bac2d95f.html
    

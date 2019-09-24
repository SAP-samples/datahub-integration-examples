# MC Contcts to S3

## Description

This graph extracts SAP Marketing Cloud contact data and stores them in ORC format into Amazon S3. 

The graph is composed of the following components:
- OData Query Consumer: Reads contact data from the Odata endpoint exposed by SAP Marketing Cloud.
- Flowagent File Producer: Writes the data in ORC format into Amazon S3.
- 3-1 Multiplexer & Terminal: Shows results of the data ingestion.

## Prerequisites

- For this graph to run you will need the following:
    - Configured connection to the SAP Marketing Cloud interactions contacts OData endpoint with ID `APPINT_MC_CONTACTS`
    - Configured connection to Amazon S3 with ID `APPINT_S3`
        - Remark: you can also use corresponding object store solutions from Microsoft Azure or Google Cloud Platform.

## Configure and Run the Graph

1. Adapt the OData query in the OData Query Consumer as required. The default configuration looks like this:<br>
`InteractionContactOriginData?$orderby=CreationDateTime&$filter=InteractionContactOrigin eq 'SAP_C4C_BUPA' or InteractionContactOrigin eq 'SAP_ERP_CUSTOMER' or InteractionContactOrigin eq 'SAP_FILE_IMPORT' or InteractionContactOrigin eq 'SAP_HYBRIS_CONSUMER'`
2. Adapt the target location in S3 for the generated file. Default location is:
   `/sdl/landing_zone/appInt/mc/Contacts.orc`
3. Save and run the graph. 
4. Use the Terminal operator to view the status of the Pipeline during execution. Press `Enter` on the Terminal console to complete the graph.

<br>
<div class="footer">
   &copy; 2019 SAP SE or an SAP affiliate company. All rights reserved.
</div>

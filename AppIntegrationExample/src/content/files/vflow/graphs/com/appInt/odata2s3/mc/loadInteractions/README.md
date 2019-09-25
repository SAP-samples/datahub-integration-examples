# MC Interact. to S3

## Description

This graph extracts SAP Marketing Cloud interaction data and stores them in ORC format into Amazon S3.

The graph is composed of the following components:
- OData Query Consumer: Reads interactions data from the Odata endpoint exposed by SAP Marketing Cloud.
- Flowagent File Producer: Writes the data in ORC format into Amazon S3.
- 3-1 Multiplexer & Terminal: Shows results of the data ingestion.

## Prerequisites

- For this graph to run you will need the following:
    - Configured connection to the SAP Marketing Cloud interactions OData endpoint with ID `APPINT_MC_INTERACT`
    - Configured connection to Amazon S3 with ID `APPINT_S3`
        - Remark: you can also use corresponding object store solutions from Microsoft Azure or Google Cloud Platform.

## Configure and Run the Graph

1. Adapt the OData query in the OData Query Consumer as required. The default configuration looks like this:<br>
`Interactions?$orderby=InteractionTimeStampUTC&$filter=InteractionType eq 'COMPLAINTS' or InteractionType eq 'EMAIL_COMPLAINT' or InteractionType eq 'OPPORTUNITY' or InteractionType eq 'C4C_OPPORTUNITY' or InteractionType eq 'CRM_OPPORTUNITY'`
2. Adapt the target location in S3 for the generated file. Default location is:
   `/sdl/landing_zone/appInt/mc/Interactions.orc`
3. Save and run the graph. 
4. Use the Terminal operator to view the status of the Pipeline during execution. Press `Enter` on the Terminal console to complete the graph.

<br>
<div class="footer">
   &copy; 2019 SAP SE or an SAP affiliate company. All rights reserved.
</div>

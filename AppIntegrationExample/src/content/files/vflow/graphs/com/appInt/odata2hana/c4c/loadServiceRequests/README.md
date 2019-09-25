# C4C SrvRq. to HANA

## Description

This graph extracts SAP Cloud for Customer service requests and stores them directly to HANA.

The graph is composed of the following components:
- OData Query Consumer: Reads contact data from the Odata endpoint exposed by C4C.
- Flowagent Table Producer: Writes the data into HANA.
- 3-1 Multiplexer & Terminal: Shows results of the data ingestion.

## Prerequisites

- For this graph to run you will need the following:
    - Configured connection to the SAP Cloud for Customer Odata endpoint with ID `APPINT_C4C`        
    - Configured connection to SAP HANA with ID `APPINT_HANA`
    - Existing SAP HANA schema and table
        - Please create the `com_sap_appint_c4c_serviceRequests` table in the `DH_INPUT` schema.

## Configure and Run the Graph

1. Adapt the OData query in the OData Query Consumer as required. The default configuration looks like this:<br>
`/ServiceRequestCollection?$select=ObjectID,ID,UUID,Name,ProductRecipientPartyID,ProductRecipientPartyUUID,ProductRecipientPartyName,IncidentServiceIssueCategoryID,EscalationStatusCode,EscalationStatusCodeText,ServicePriorityCode,ServicePriorityCodeText,RequestedFulfillmentPeriodStartDateTime,RequestedFulfillmentPeriodEndDateTime,RequestedTotalProcessingDuration,RequestedTotalRequestorDuration,RequestInitialReceiptdatetimecontent,RequestCloseddatetimeContent,SalesOrganisationID,SalesUnitPartyID,BuyerPartyID,WarrantyGoodwillCode,EscalationTimePointDateTime,ResolutionDueDateTime,SalesTerritoryID,SalesUnitPartyName,BuyerPartyName,BuyerPartyUUID,WarrantyID,ServiceIssueCategoryID,ServiceRequestClassificationCode,ServiceRequestClassificationCodeText,CreationDateTime`
2. Save and run the graph. 
3. Use the Terminal operator to view the status of the Pipeline during execution. Press `Enter` on the Terminal console to complete the graph.

<br>
<div class="footer">
   &copy; 2019 SAP SE or an SAP affiliate company. All rights reserved.
</div>

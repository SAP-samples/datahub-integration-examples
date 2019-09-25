# MC Contcts to HANA

## Description

This graph extracts SAP Marketing Cloud interaction contact origin data and stores them directly to HANA.

The graph is composed of the following components:

- OData Query Consumer: Reads contact data from the Odata endpoint exposed by SAP Marketing Cloud.
- Flowagent Table Producer: Writes the data into HANA.
- 3-1 Multiplexer & Terminal: Shows results of the data ingestion.

## Prerequisites

- For this graph to run you will need the following:
    - Configured connection to the SAP Marketing Cloud interactions contacts OData endpoint with ID `APPINT_MC_CONTACTS`
    - Configured connection to SAP HANA with ID `APPINT_HANA`
    - Existing SAP HANA schema and table
        - Please create the `com_sap_appint_mc_interactionContactOriginData` table in the `DH_INPUT` schema.

## Configure and Run the Graph

1. Adapt the OData query in the OData Query Consumer as required. The default configuration looks like this:<br>
`/InteractionContactOriginData?$filter=InteractionContactOrigin eq 'SAP_C4C_BUPA' or InteractionContactOrigin eq 'SAP_ERP_CUSTOMER' or InteractionContactOrigin eq 'SAP_FILE_IMPORT' or InteractionContactOrigin eq 'SAP_HYBRIS_CONSUMER'&$select=InteractionContactOrigin,InteractionContactID,IsEndOfPurposeBlocked,TrackingID,OriginDataLastChgUTCDateTime,LastChangeDateTime,LastChangedByUser,WebSiteURL,CreationDateTime,InteractionContactImageURL,CreatedByUser,InteractionContactType,InteractionContactUUID,Latitude,Longitude,FullName,SpatialReferenceSystem,CityName,StreetName,AddressHouseNumber,Language,LanguageName,EmailAddress,PhoneNumber,MobileNumber,FaxNumber,HasMktgPermissionForDirectMail,Country,CountryName,AddressRegion,RegionName,ContactPostalCode,Industry,IndustryName,IsObsolete`
2. Save and run the graph. 
3. Use the Terminal operator to view the status of the Pipeline during execution. Press `Enter` on the Terminal console to complete the graph.

<br>
<div class="footer">
   &copy; 2019 SAP SE or an SAP affiliate company. All rights reserved.
</div>

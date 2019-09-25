# S4 BuPa to HANA

## Description

This graph extracts business partners from S/4 HANA and stores them directly to HANA.

The graph is composed of the following components:
- OData Query Consumer: Reads contact data from the Odata endpoint exposed by S4.
- Flowagent Table Producer: Writes the data into HANA.
- 3-1 Multiplexer & Terminal: Shows results of the data ingestion.

## Prerequisites

- For this graph to run you will need the following:
    - Configured connection to the S/4 HANA business partner OData endpoint with ID `APPINT_S4_BUPA`
    - Configured connection to SAP HANA with ID `APPINT_HANA`
    - Existing SAP HANA schema and table
        - Please create the `com_sap_appint_s4_businessPartners` table in the `DH_INPUT` schema.

## Configure and Run the Graph

1. Adapt the OData query in the OData Query Consumer as required. The default configuration looks like this:<br>
`/A_BusinessPartner?$select=BusinessPartner,Customer,Supplier,AcademicTitle,AuthorizationGroup,BusinessPartnerCategory,BusinessPartnerFullName,BusinessPartnerGrouping,BusinessPartnerName,BusinessPartnerUUID,CorrespondenceLanguage,CreatedByUser,CreationDate,CreationTime,FirstName,FormOfAddress,Industry,InternationalLocationNumber1,InternationalLocationNumber2,IsFemale,IsMale,IsNaturalPerson,IsSexUnknown,Language,LastChangeDate,LastChangeTime,LastChangedByUser,LastName,LegalForm,OrganizationBPName1,OrganizationBPName2,OrganizationBPName3,OrganizationBPName4,OrganizationFoundationDate,OrganizationLiquidationDate,SearchTerm1,AdditionalLastName,BirthDate,BusinessPartnerIsBlocked,BusinessPartnerType,ETag,GroupBusinessPartnerName1,GroupBusinessPartnerName2,IndependentAddressID,InternationalLocationNumber3,MiddleName,NameCountry,NameFormat,PersonFullName,PersonNumber,IsMarkedForArchiving,BusinessPartnerIDByExtSystem,TradingPartner`
2. Save and run the graph. 
3. Use the Terminal operator to view the status of the Pipeline during execution. Press `Enter` on the Terminal console to complete the graph.

<br>
<div class="footer">
   &copy; 2019 SAP SE or an SAP affiliate company. All rights reserved.
</div>

# OData to HANA

## Description
This graph orchestrates all pipelines required to load the following data into SAP HANA:
- SAP Cloud for Customer corporate accounts, customer orders, and service requests
- SAP Marketing Cloud contacts and interactions
- SAP S/4 HANA business partners and customer returns

## Prerequisites
For this graph to run you need to configure the following graphs:
- `com.appInt.odata2hana.c4c.loadCorporateAccounts` - "C4C Accts. to HANA"
- `com.appInt.odata2hana.c4c.loadCustomerOrders` - "C4C CustOr to HANA"
- `com.appInt.odata2hana.c4c.loadServiceRequests` - "C4C SrvRq. to HANA"
- `com.appInt.odata2hana.mc.loadContactOriginData` - "MC Contcts to HANA"
- `com.appInt.odata2hana.mc.loadInteractions` - "MC Interact. to HANA"
- `com.appInt.odata2hana.s4.loadBusinessPartners` - "S4 BuPa to HANA"
- `com.appInt.odata2hana.s4.loadCustomerReturns` - "S4 CustRet. to HANA"

## Configure and Run the Graph
There is no configuration for this graph. Use the Terminal operator to check for errors occurring during execution. The graph terminates after all data has been loaded succesfully. Otherwise press `Enter` on the Terminal console to complete the graph.

<br>
<div class="footer">
   &copy; 2019 SAP SE or an SAP affiliate company. All rights reserved.
</div>

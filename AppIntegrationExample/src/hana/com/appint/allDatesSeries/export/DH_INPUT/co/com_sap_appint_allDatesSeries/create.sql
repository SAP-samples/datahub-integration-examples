CREATE VIEW "DH_INPUT"."com_sap_appint_allDatesSeries" ( "BusinessPartnerUID", "mcInteractionContactOrigin", "mcInteractionContactID", "mcInteractionContactUUID", "c4cAccountId", "s4BusinessPartner", "Matches", "isContact", "isCorporateAccount", "isBusinessPartner", "Name", "Country", "City", "Date", "Currency", "c4cOrders", "c4cOrdersTotal", "c4cServiceRequest", "mcComplaints", "mcComplaintsTotal", "mcOpportunities", "mcOpportunitiesTotal", "s4CustomerReturns", "s4CustomerReturnsTotal" ) AS SELECT 

dateSeries."BusinessPartnerUID",
dateSeries."mcInteractionContactOrigin",
dateSeries."mcInteractionContactID",
dateSeries."mcInteractionContactUUID",
dateSeries."c4cAccountId",
dateSeries."s4BusinessPartner",
dateSeries."Matches",
dateSeries."isContact",
dateSeries."isCorporateAccount",
dateSeries."isBusinessPartner",
dateSeries."Name",
dateSeries."Country",
dateSeries."City",
dateSeries."Date",
dateCurrSeries."Currency",


IFNULL(IFNULL(dateCurrSeries."c4cOrders",dateSeries."c4cOrders"),0) AS "c4cOrders",
dateCurrSeries."c4cOrdersTotal",
dateSeries."c4cServiceRequest",

IFNULL(IFNULL(dateCurrSeries."mcComplaints",dateSeries."mcComplaints"),0)  AS "mcComplaints",
dateCurrSeries."mcComplaintsTotal",

IFNULL(IFNULL(dateCurrSeries."mcOpportunities",dateSeries."mcOpportunities"),0)  AS "mcOpportunities",
dateCurrSeries."mcOpportunitiesTotal",

IFNULL(IFNULL(dateCurrSeries."s4CustomerReturns",dateSeries."s4CustomerReturns"),0)  AS "s4CustomerReturns",
dateCurrSeries."s4CustomerReturnsTotal"

FROM "DH_INPUT"."com_sap_appint_dateSeries"  AS dateSeries
LEFT OUTER JOIN "DH_INPUT"."com_sap_appint_dateCurrencySeries" AS dateCurrSeries
ON dateCurrSeries."Date" = dateSeries."Date"
AND dateCurrSeries."BusinessPartnerUID" = dateSeries."BusinessPartnerUID" WITH READ ONLY
CREATE VIEW "DH_INPUT"."com_sap_appint_dateCurrencySeries" ( "BusinessPartnerUID", "mcInteractionContactOrigin", "mcInteractionContactID", "mcInteractionContactUUID", "c4cAccountId", "s4BusinessPartner", "Matches", "isContact", "isCorporateAcTotal", "isBusinessPartner", "Name", "Country", "City", "Date", "Currency", "c4cOrders", "c4cOrdersTotal", "mcComplaints", "mcComplaintsTotal", "mcOpportunities", "mcOpportunitiesTotal", "s4CustomerReturns", "s4CustomerReturnsTotal" ) AS SELECT
	 bupa."UID" AS "BusinessPartnerUID",
	 bupa."mcInteractionContactOrigin" ,
	 bupa."mcInteractionContactID" ,
	 bupa."mcInteractionContactUUID" ,
	 bupa."c4cAccountId" ,
	 bupa."s4BusinessPartner" ,
	 bupa."Matches" ,
	 bupa."isContact" ,
	 bupa."isCorporateAccount" ,
	 bupa."isBusinessPartner" ,
	 bupa."Name" ,
	 bupa."Country",
	 bupa."City",
	 LEFT(TO_NVARCHAR(dates."Date",'YYYY-MM-DD'),10) AS "Date" ,
	 dates."Currency",
	 IFNULL (custOrd."Count",
	 0) AS "c4cOrders" ,
	 IFNULL (custOrd."Total",
	 0) AS "c4cOrdersTotal" ,
	 IFNULL (compl."Count",
	 0) AS "mcComplaints" ,
	 IFNULL (compl."Total",
	 0) AS "mcComplaintsTotal" ,
	 IFNULL (opp."Count",
	 0) AS "mcOpportunities",
	 IFNULL (opp."Total",
	 0) AS "mcOpportunitiesTotal" ,
	 IFNULL (cr."Count",
	 0) AS "s4CustomerReturns",
	 IFNULL (cr."Total",
	 0) AS "s4CustomerReturnsTotal" 
FROM "DH_INPUT"."com_sap_appint_datesAndCurrencies" AS dates 
INNER JOIN "DH_INPUT"."com_sap_appint_businesPartnerMapping" AS bupa on bupa."UID" = dates."BusinessPartnerUID" 
LEFT OUTER JOIN "DH_INPUT"."com_sap_appint_c4c_customerOrdersTotal" AS custOrd ON custord."UID" = dates."BusinessPartnerUID" 
AND custord."Date" = dates."Date" 
AND custord."Currency" = dates."Currency" 
LEFT OUTER JOIN "DH_INPUT"."com_sap_appint_mc_complaintInteractionsTotal" AS compl ON compl."UID" = dates."BusinessPartnerUID" 
AND compl."InteractionDate" = dates."Date" 
AND compl."InteractionCurrency" = dates."Currency" 
LEFT OUTER JOIN "DH_INPUT"."com_sap_appint_mc_opportunityInteractionsTotal" AS opp ON opp."UID" = dates."BusinessPartnerUID" 
AND opp."InteractionDate" = dates."Date" 
AND opp."InteractionCurrency" = dates."Currency" 
LEFT OUTER JOIN "DH_INPUT"."com_sap_appint_s4_customerReturnsTotal" AS cr ON cr."UID" = dates."BusinessPartnerUID" 
AND cr."Date" = dates."Date" 
AND cr."Currency" = dates."Currency" ORDER BY bupa."UID",
	 "Date" WITH READ ONLY
CREATE VIEW "DH_INPUT"."com_sap_appint_dateSeries" ( "BusinessPartnerUID", "mcInteractionContactOrigin", "mcInteractionContactID", "mcInteractionContactUUID", "c4cAccountId", "s4BusinessPartner", "Matches", "isContact", "isCorporateAccount", "isBusinessPartner", "Name", "Country", "City", "Date", "c4cOrders", "c4cServiceRequest", "mcComplaints", "mcOpportunities", "s4CustomerReturns" ) AS SELECT
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
	 IFNULL (custOrd."Count",
	 0) AS "c4cOrders" ,
	 IFNULL (servrq."Count",
	 0) AS "c4cServiceRequests" ,
	 IFNULL (compl."Count",
	 0) AS "mcComplaints" ,
	 IFNULL (opp."Count",
	 0) AS "mcOpportunities",
	 IFNULL (cr."Count",
	 0) AS "s4CustomerReturns" 
FROM "DH_INPUT"."com_sap_appint_dates" AS dates 
INNER JOIN "DH_INPUT"."com_sap_appint_businesPartnerMapping" AS bupa on bupa."UID" = dates."BusinessPartnerUID" 
LEFT OUTER JOIN "DH_INPUT"."com_sap_appint_c4c_customerOrdersCount" AS custOrd ON custord."UID" = dates."BusinessPartnerUID" 
AND custord."Date" = dates."Date" 
LEFT OUTER JOIN "DH_INPUT"."com_sap_appint_c4c_serviceRequestsCount" AS servrq ON servrq."UID" = dates."BusinessPartnerUID" 
AND servrq."Date" = dates."Date" 
LEFT OUTER JOIN "DH_INPUT"."com_sap_appint_mc_complaintInteractionsCount" AS compl ON compl."UID" = dates."BusinessPartnerUID" 
AND compl."InteractionDate" = dates."Date" 
LEFT OUTER JOIN "DH_INPUT"."com_sap_appint_mc_opportunityInteractionsCount" AS opp ON opp."UID" = dates."BusinessPartnerUID" 
AND opp."InteractionDate" = dates."Date" 
LEFT OUTER JOIN "DH_INPUT"."com_sap_appint_s4_customerReturnsCount" AS cr ON cr."UID" = dates."BusinessPartnerUID" 
AND cr."Date" = dates."Date" ORDER BY bupa."UID",
	 "Date" WITH READ ONLY
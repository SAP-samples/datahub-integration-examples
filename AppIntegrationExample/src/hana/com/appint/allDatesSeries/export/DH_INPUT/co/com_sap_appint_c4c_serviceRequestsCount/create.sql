CREATE VIEW "DH_INPUT"."com_sap_appint_c4c_serviceRequestsCount" ( "UID", "AccountId", "Date", "Count" ) AS SELECT
	 bupa."UID",
	 serv."BuyerPartyID" AS "AccountId",
	 TO_DATE(serv."CreationDateTime") AS "Date",
	 COUNT(serv."ObjectID") AS "Count" 
FROM "DH_INPUT"."com_sap_appint_c4c_serviceRequests" AS serv 
INNER JOIN "DH_INPUT"."com_sap_appint_businesPartnerMapping" AS bupa ON bupa."c4cAccountId" = serv."BuyerPartyID" 
GROUP BY bupa."UID",
	serv."BuyerPartyID",
	 TO_DATE(serv."CreationDateTime") WITH READ ONLY
CREATE VIEW "DH_INPUT"."com_sap_appint_c4c_customerOrdersCount" ( "UID", "AccountId", "Date", "Count" ) AS SELECT
	 bupa."UID",
	 ord."BuyerPartyID" AS "AccountId",
	 TO_DATE(ord."DateTime") AS "Date",
	 COUNT(ord."ObjectID") AS "Count" 
FROM "DH_INPUT"."com_sap_appint_c4c_customerOrders" AS ord 
INNER JOIN "DH_INPUT"."com_sap_appint_businesPartnerMapping" AS bupa ON bupa."c4cAccountId" = ord."BuyerPartyID" 
GROUP BY bupa."UID",
	ord."BuyerPartyID",
	TO_DATE( ord."DateTime" ) WITH READ ONLY
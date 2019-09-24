CREATE VIEW "DH_INPUT"."com_sap_appint_c4c_customerOrdersTotal" ( "UID", "AccountId", "Date", "Currency", "Total", "Count" ) AS SELECT
	 bupa."UID",
	 ord."BuyerPartyID" AS "AccountId",
	 TO_DATE(ord."DateTime") AS "Date",
	 ord."NetAmountCurrencyCode" AS "Currency",
	 SUM(ord."NetAmount") AS "Total",
	 COUNT(ord."ObjectID") AS "Count" 
FROM "DH_INPUT"."com_sap_appint_c4c_customerOrders" AS ord
INNER JOIN "DH_INPUT"."com_sap_appint_businesPartnerMapping" AS bupa 
   ON bupa."c4cAccountId" = ord."BuyerPartyID" 
WHERE ord."NetAmountCurrencyCode" IS NOT NULL 
AND ord."NetAmount" IS NOT NULL 
GROUP BY 
	bupa."UID",
	ord."BuyerPartyID",
	TO_DATE(ord."DateTime"),
	ord."NetAmountCurrencyCode" WITH READ ONLY
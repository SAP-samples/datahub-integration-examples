CREATE VIEW "DH_INPUT"."com_sap_appint_s4_customerReturnsTotal" ( "UID", "BusinessPartner", "Date", "Currency", "Total", "Count" ) AS SELECT
	 bupa."UID",
	 cr."SoldToParty" AS "BusinessPartner",
	 TO_DATE(cr."CustomerReturnDate") AS "Date",
	 cr."TransactionCurrency" AS "Currency",
	 SUM(cr."TotalNetAmount") AS "Total",
	 COUNT(cr."CustomerReturn") AS "Count" 
FROM "DH_INPUT"."com_sap_appint_s4_customerReturns" AS cr 
INNER JOIN "DH_INPUT"."com_sap_appint_businesPartnerMapping" AS bupa 
	ON bupa."s4BusinessPartner" = cr."SoldToParty" 
WHERE cr."TransactionCurrency" IS NOT NULL 
AND cr."TotalNetAmount" IS NOT NULL 
GROUP BY bupa."UID",
	 cr."SoldToParty",
	 TO_DATE(cr."CustomerReturnDate"),
	 cr."TransactionCurrency" WITH READ ONLY
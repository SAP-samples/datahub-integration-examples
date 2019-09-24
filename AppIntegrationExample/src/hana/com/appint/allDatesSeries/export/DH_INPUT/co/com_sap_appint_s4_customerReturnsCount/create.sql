CREATE VIEW "DH_INPUT"."com_sap_appint_s4_customerReturnsCount" ( "UID", "BusinessPartner", "Date", "Count" ) AS SELECT
	 bupa."UID",
	 cr."SoldToParty" AS "BusinessPartner",
	 TO_DATE(cr."CustomerReturnDate") AS "Date",
	 COUNT(cr."CustomerReturn") AS "Count" 
FROM "DH_INPUT"."com_sap_appint_s4_customerReturns" AS cr 
LEFT OUTER  JOIN "DH_INPUT"."com_sap_appint_businesPartnerMapping" AS bupa 
	ON bupa."s4BusinessPartner" = cr."SoldToParty" 
GROUP BY bupa."UID",
	 cr."SoldToParty",
	 TO_DATE(cr."CustomerReturnDate") WITH READ ONLY
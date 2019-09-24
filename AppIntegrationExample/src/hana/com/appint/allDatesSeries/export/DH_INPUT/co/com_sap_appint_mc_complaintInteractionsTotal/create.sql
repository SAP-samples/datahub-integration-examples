CREATE VIEW "DH_INPUT"."com_sap_appint_mc_complaintInteractionsTotal" ( "UID", "ContactUUID", "InteractionDate", "InteractionCurrency", "Total", "Count" ) AS SELECT
	 bupa."UID",
	 compl."InteractionContactUUID" AS "ContactUUID",
	 TO_DATE(compl."InteractionTimeStampUTC") AS "InteractionDate",
	 compl."InteractionCurrency" AS "InteractionCurrency",
	 SUM(compl."InteractionAmount") AS "Total",
	 COUNT(compl."InteractionUUID") AS "Count" 
FROM "DH_INPUT"."com_sap_appint_mc_interactions" AS compl 
INNER JOIN "DH_INPUT"."com_sap_appint_businesPartnerMapping" AS bupa ON bupa."mcInteractionContactUUID" = compl."InteractionContactUUID" 
WHERE compl."InteractionCurrency" IS NOT NULL 
AND (compl."InteractionType" = 'COMPLAINTS' 
	OR compl."InteractionType" = 'EMAIL_COMPLAINT') 
GROUP BY bupa."UID",
	 compl."InteractionContactUUID",
	 TO_DATE(compl."InteractionTimeStampUTC"),
	 compl."InteractionCurrency" WITH READ ONLY
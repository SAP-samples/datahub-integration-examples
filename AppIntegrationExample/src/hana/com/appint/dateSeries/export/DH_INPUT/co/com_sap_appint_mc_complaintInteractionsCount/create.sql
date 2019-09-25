CREATE VIEW "DH_INPUT"."com_sap_appint_mc_complaintInteractionsCount" ( "UID", "ContactUID", "InteractionDate", "Count" ) AS SELECT
	 bupa."UID",
	 compl."InteractionContactUUID" AS "ContactUUID",
	 TO_DATE(compl."InteractionTimeStampUTC") AS "InteractionDate",
	 COUNT(compl."InteractionUUID") AS "Count" 
FROM "DH_INPUT"."com_sap_appint_mc_interactions" AS compl 
INNER JOIN "DH_INPUT"."com_sap_appint_businesPartnerMapping" AS bupa ON bupa."mcInteractionContactUUID" = compl."InteractionContactUUID" 
WHERE ("InteractionType" = 'COMPLAINTS' 
	OR "InteractionType" = 'EMAIL_COMPLAINT') 
GROUP BY bupa."UID",
	 compl."InteractionContactUUID",
	 TO_DATE(compl."InteractionTimeStampUTC") WITH READ ONLY
CREATE VIEW "DH_INPUT"."com_sap_appint_mc_opportunityInteractionsCount" ( "UID", "ContactUID", "InteractionDate", "Count" ) AS SELECT
	 bupa."UID",
	 opp."InteractionContactUUID" AS "ContactUUID",
	 TO_DATE(opp."InteractionTimeStampUTC") AS "InteractionDate",
	 COUNT(opp."InteractionUUID") AS "Count" 
FROM "DH_INPUT"."com_sap_appint_mc_interactions" AS opp 
INNER JOIN "DH_INPUT"."com_sap_appint_businesPartnerMapping" AS bupa ON bupa."mcInteractionContactUUID" = opp."InteractionContactUUID" 
WHERE (opp."InteractionType" = 'OPPORTUNITY' 
	OR opp."InteractionType" = 'C4C_OPPORTUNITY' 
	OR opp."InteractionType" = 'CRM_OPPORTUNITY') 
GROUP BY bupa."UID",
	 opp."InteractionContactUUID",
	 TO_DATE(opp."InteractionTimeStampUTC") WITH READ ONLY
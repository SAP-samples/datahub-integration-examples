CREATE VIEW "DH_INPUT"."com_sap_appint_mc_opportunityInteractionsTotal" ( "UID", "ContactUUID", "InteractionDate", "InteractionCurrency", "Total", "Count" ) AS SELECT
	 bupa."UID",
	 opp."InteractionContactUUID" AS "ContactUUID",
	 TO_DATE(opp."InteractionTimeStampUTC") AS "InteractionDate",
	 opp."InteractionCurrency" AS "InteractionCurrency",
	 SUM(opp."InteractionAmount") AS "Total",
	 COUNT(opp."InteractionUUID") AS "Count" 
FROM "DH_INPUT"."com_sap_appint_mc_interactions" AS opp 
INNER JOIN "DH_INPUT"."com_sap_appint_businesPartnerMapping" AS bupa ON bupa."mcInteractionContactUUID" = opp."InteractionContactUUID" 
WHERE opp."InteractionCurrency" IS NOT NULL 
AND (opp."InteractionType" = 'OPPORTUNITY' 
	OR opp."InteractionType" = 'C4C_OPPORTUNITY' 
	OR opp."InteractionType" = 'CRM_OPPORTUNITY') 
GROUP BY bupa."UID",
	 opp."InteractionContactUUID",
	 TO_DATE(opp."InteractionTimeStampUTC") ,
	 opp."InteractionCurrency" WITH READ ONLY
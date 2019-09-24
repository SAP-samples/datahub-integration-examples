CREATE VIEW "DH_INPUT"."com_sap_appint_dates" ( "Date", "BusinessPartnerUID" ) AS SELECT
	 DISTINCT "Date",
	"BusinessPartnerUID" 
FROM ( SELECT
	 "UID" AS "BusinessPartnerUID",
	 "Date" 
	FROM "DH_INPUT"."com_sap_appint_c4c_serviceRequestsCount" 
	UNION ALL SELECT
	 "UID" AS "BusinessPartnerUID",
	 "Date" 
	FROM "DH_INPUT"."com_sap_appint_c4c_customerOrdersCount" 
	UNION ALL SELECT
	 "UID" AS "BusinessPartnerUID",
	 "InteractionDate" AS "Date" 
	FROM "DH_INPUT"."com_sap_appint_mc_complaintInteractionsCount" 
	UNION ALL SELECT
	 "UID" AS "BusinessPartnerUID",
	 "InteractionDate" AS "Date" 
	FROM "DH_INPUT"."com_sap_appint_mc_opportunityInteractionsCount" 
	UNION ALL SELECT
	 "UID" AS "BusinessPartnerUID",
	 "Date" AS "Date" 
	FROM "DH_INPUT"."com_sap_appint_s4_customerReturnsCount" ) ORDER BY "Date",
	"BusinessPartnerUID" WITH READ ONLY
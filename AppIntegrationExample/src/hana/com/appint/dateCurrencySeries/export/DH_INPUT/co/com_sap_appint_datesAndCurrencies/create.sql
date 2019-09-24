CREATE VIEW "DH_INPUT"."com_sap_appint_datesAndCurrencies" ( "BusinessPartnerUID", "Date", "Currency" ) AS SELECT
	 DISTINCT "BusinessPartnerUID",
	"Date",
	 "Currency" 
FROM ( SELECT
	 "UID" AS "BusinessPartnerUID",
	 "Date",
	 "Currency" 
	FROM "DH_INPUT"."com_sap_appint_c4c_customerOrdersTotal" 
	UNION ALL SELECT
	 "UID" AS "BusinessPartnerUID",
	 "InteractionDate" AS "Date",
	 "InteractionCurrency" AS "Currency" 
	FROM "DH_INPUT"."com_sap_appint_mc_complaintInteractionsTotal" 
	UNION ALL SELECT
	 "UID" AS "BusinessPartnerUID",
	 "InteractionDate" AS "Date",
	 "InteractionCurrency" AS "Currency" 
	FROM "DH_INPUT"."com_sap_appint_mc_opportunityInteractionsTotal" 
	UNION ALL SELECT
	 "UID" AS "BusinessPartnerUID",
	 "Date" AS "Date", 
	 "Currency"
	FROM "DH_INPUT"."com_sap_appint_s4_customerReturnsTotal" 
	
	) WITH READ ONLY
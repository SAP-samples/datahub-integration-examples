CREATE VIEW "DH_INPUT"."com_sap_appint_businesPartnerMapping" ( "UID", "mcInteractionContactOrigin", "mcInteractionContactID", "mcInteractionContactUUID", "c4cAccountId", "s4BusinessPartner", "Matches", "isContact", "isCorporateAccount", "isBusinessPartner", "Name", "Country", "City" ) AS SELECT
	 DISTINCT NEWUID() AS "UID",
	 "InteractionContactOrigin" AS "mcInteractionContactOrigin",
	 "InteractionContactID" AS "mcInteractionContactID",
	 "InteractionContactUUID" AS "mcInteractionContactUUID",
	 "AccountID" AS "c4cAccountId",
	 "BusinessPartner" AS "s4BusinessPartner",
	 "Matches",
	 "isContact",
	 "isCorporateAccount",
	 "isBusinessPartner",
	 "Name",
	 "Country",
	 "City" 
FROM ( SELECT
	 bupa."BusinessPartner",
	 con."InteractionContactOrigin",
	 con."InteractionContactID",
	 con."InteractionContactUUID",
	 coac."AccountID",
	 2 AS "Matches",
	 'X' AS "isContact",
	 'X' AS "isBusinessPartner",
	 'X' AS "isCorporateAccount",
	 bupa."BusinessPartnerFullName" AS "Name", 
	 con."CountryName" AS "Country",
	 con."CityName" AS "City"
	FROM "DH_INPUT"."com_sap_appint_mc_interactionContactOriginData" AS con 
	INNER JOIN "DH_INPUT"."com_sap_appint_c4c_corporateAccounts" AS coac ON coac."AccountID" = con."InteractionContactID" 
	AND con."InteractionContactOrigin" = 'SAP_C4C_BUPA' 
	AND coac."Name" = con."FullName" 
	INNER JOIN "DH_INPUT"."com_sap_appint_s4_businessPartners" AS bupa ON coac."AccountID" = bupa."BusinessPartner" 
	AND coac."Name" = bupa."BusinessPartnerFullName" 
	UNION ALL SELECT
	 NULL AS "BusinessPartner",
	 con."InteractionContactOrigin",
	 con."InteractionContactID",
	 con."InteractionContactUUID",
	 coac."AccountID",
	 1 AS "Matches",
	 'X' AS "isContact",
	 '-' AS "isBusinessPartner",
	 'X' AS "isCorporateAccount",
	 coac."Name" AS "Name", 
	 con."CountryName" AS "Country",
	 con."CityName" AS "City"
	FROM "DH_INPUT"."com_sap_appint_mc_interactionContactOriginData" AS con 
	INNER JOIN "DH_INPUT"."com_sap_appint_c4c_corporateAccounts" AS coac ON coac."AccountID" = con."InteractionContactID" 
	AND con."InteractionContactOrigin" = 'SAP_C4C_BUPA' 
	AND coac."Name" = con."FullName" 
	AND coac."AccountID" NOT IN (SELECT
	 "BusinessPartner" 
		FROM "DH_INPUT"."com_sap_appint_s4_businessPartners" ) 
	UNION ALL SELECT
	 bupa."BusinessPartner",
	 con."InteractionContactOrigin",
	 con."InteractionContactID",
	 con."InteractionContactUUID",
	 NULL AS "AccountId",
	 1 AS "Matches",
	 'X' AS "isContact",
	 'X' AS "isBusinessPartner",
	 '-' AS "isCorporateAccount",
	 con."FullName" AS "Name",
	 con."CountryName" AS "Country",
	 con."CityName" AS "City" 
	FROM "DH_INPUT"."com_sap_appint_s4_businessPartners" AS bupa 
	INNER JOIN "DH_INPUT"."com_sap_appint_mc_interactionContactOriginData" AS con ON con."InteractionContactID" = bupa."BusinessPartner" 
	AND con."FullName" = bupa."BusinessPartnerFullName" 
	AND con."InteractionContactID" NOT IN (SELECT
	 "AccountID" 
		FROM "DH_INPUT"."com_sap_appint_c4c_corporateAccounts" ) 
	UNION ALL SELECT
	 bupa."BusinessPartner",
	 NULL AS "InteractionContactOrigin",
	 NULL AS "InteractionContactID",
	 NULL AS "InteractionContactUUID",
	 coac."AccountID",
	 1 AS "Matches",
	 '-' AS "isContact",
	 'X' AS "isBusinessPartner",
	 'X' AS "isCorporateAccount",
	 coac."Name" AS "Name",
	 NULL AS "Country",
	 coac."City" AS "City" 
	FROM "DH_INPUT"."com_sap_appint_s4_businessPartners" AS bupa 
	INNER JOIN "DH_INPUT"."com_sap_appint_c4c_corporateAccounts" coac ON coac."AccountID" = bupa."BusinessPartner" 
	AND coac."Name" = bupa."BusinessPartnerFullName" 
	AND bupa."BusinessPartner" NOT IN (SELECT
	 "InteractionContactID" 
		FROM "DH_INPUT"."com_sap_appint_mc_interactionContactOriginData" ) 
	
		
	UNION ALL SELECT
	 NULL AS "BusinessPartner",
	 con."InteractionContactOrigin",
	 con."InteractionContactID",
	 NULL AS "InteractionContactUUID",
	 NULL AS "AccountId",
	 0 AS "Matches",
	 'X' AS "isContact",
	 '-' AS "isBusinessPartner",
	 '-' AS "isCorporateAccount",
	 con."FullName" AS "Name",
	 con."CountryName" AS "Country",
	 con."CityName" AS "City" 
	FROM "DH_INPUT"."com_sap_appint_mc_interactionContactOriginData" AS con 
	WHERE con."InteractionContactID" NOT IN (SELECT
	 "InteractionContactID" 
		FROM "DH_INPUT"."com_sap_appint_mc_interactionContactOriginData" ) 
	AND con."InteractionContactID" NOT IN (SELECT
	 "AccountID" 
		FROM "DH_INPUT"."com_sap_appint_c4c_corporateAccounts" ) 
	UNION ALL SELECT
	 NULL AS "BusinessPartner",
	 NULL AS "InteractionContactOrigin",
	 NULL AS "InteractionContactID",
	 NULL AS "InteractionContactUUID",
	 coac."AccountID",
	 0 AS "Matches",
	 '-' AS "isContact",
	 '-' AS "isBusinessPartner",
	 'X' AS "isCorporateAccount",
	 coac."Name" AS "Name",
	 NULL AS "Country",
	 coac."City" AS "City" 
	FROM "DH_INPUT"."com_sap_appint_c4c_corporateAccounts" coac 
	WHERE coac."AccountID" NOT IN (SELECT
	 "InteractionContactID" 
		FROM "DH_INPUT"."com_sap_appint_mc_interactionContactOriginData" ) 
	AND coac."AccountID" NOT IN (SELECT
	 "BusinessPartner" 
		FROM "DH_INPUT"."com_sap_appint_s4_businessPartners" ) 
	UNION ALL 
	
	SELECT
	 "BusinessPartner",
	 NULL AS "InteractionContactOrigin",
	 NULL AS "InteractionContactID",
	 NULL AS "InteractionContactUUID",
	 NULL AS "AccountID",
	 0 AS "Matches",
	 '-' AS "isContact",
	 'X' AS "isBusinessPartner",
	 '-' AS "isCorporateAccount",
	 bupa."BusinessPartnerFullName" AS "Name",
	 NULL AS "Country",
	 NULL AS "City"  
	FROM "DH_INPUT"."com_sap_appint_s4_businessPartners" bupa 
	WHERE bupa."BusinessPartner" NOT IN (SELECT
	 "InteractionContactID" 
		FROM "DH_INPUT"."com_sap_appint_mc_interactionContactOriginData" ) 
	AND bupa."BusinessPartner" NOT IN (SELECT
	 "AccountID" 
		FROM "DH_INPUT"."com_sap_appint_c4c_corporateAccounts" 
		
		) ) ORDER BY "Matches" DESC,
	 "InteractionContactOrigin",
	 "InteractionContactID",
	 "BusinessPartner",
	 "AccountID" WITH READ ONLY
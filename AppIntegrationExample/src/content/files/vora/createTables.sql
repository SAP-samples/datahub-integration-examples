-- c4c Accounts - CSV ---------------------------------------------------------
drop table "com_appInt_c4c_Accounts_CSV";

create table "com_appInt_c4c_Accounts_CSV" (
	"AccountID" NVARCHAR(10),
	"UUID" NVARCHAR(36),
	"ExternalID" NVARCHAR(100),
	"RoleCode" NVARCHAR(6),
	"RoleCodeText" NVARCHAR(5000),
	"Name" NVARCHAR(40),
	"HouseNumber" NVARCHAR(10),
	"Street" NVARCHAR(60),
	"City" NVARCHAR(40),
	"CreationOn" TIMESTAMP(7),
	"ChangedOn" TIMESTAMP(7)
) with type datasource engine 'FILES';

alter table "com_appInt_c4c_Accounts_CSV"
    add datasource csv(S3('/sdl/landing_zone/appInt/c4c/Accounts.csv')) 
    using connection 'APPINT_S3'
    delimited by ';' skip 1;

load table "com_appInt_c4c_Accounts_CSV" reload all;

-- c4c CustomerOrders - CSV ---------------------------------------------------
drop table "com_appInt_c4c_CustomerOrders_CSV";

create table "com_appInt_c4c_CustomerOrders_CSV" (
	"ObjectID" NVARCHAR(70),
	"ClassificationCode" NVARCHAR(3),
	"ClassificationCodeText" NVARCHAR(5000),
	"BuyerID" NVARCHAR(35),
	"ID" NVARCHAR(35),
	"LastChangeDate" DATE,
	"Name" NVARCHAR(255),
	"ItemListCancellationStatusCode" NVARCHAR(2),
	"ItemListCancellationStatusCodeText" NVARCHAR(5000),
	"ApprovalStatusCode" NVARCHAR(2),
	"SalesOrganisationID" NVARCHAR(20),
	"BuyerPartyID" NVARCHAR(60),
	"BuyerPartyName" NVARCHAR(480),
	"ProductRecipientPartyID" NVARCHAR(60),
	"ProductRecipientPartyName" NVARCHAR(480),
	"SalesUnitPartyID" NVARCHAR(60),
	"DateTime" TIMESTAMP(7),
	"NetAmount" DECIMAL(28, 6),
	"NetAmountCurrencyCode" NVARCHAR(3),
	"SetAsCompleted" NVARCHAR(5)
) with type datasource engine 'FILES';

alter table "com_appInt_c4c_CustomerOrders_CSV"
    add datasource csv(S3('/sdl/landing_zone/appInt/c4c/CustomerOrders.csv')) 
    using connection 'APPINT_S3'
    delimited by ';' skip 1;

load table "com_appInt_c4c_CustomerOrders_CSV" reload all;

-- c4c ServiceRequests - Parquet ----------------------------------------------
drop table "com_appInt_c4c_ServiceRequests_Parquet";

create table "com_appInt_c4c_ServiceRequests_Parquet" (
	"ObjectID" NVARCHAR(70),
	"ProductRecipientPartyID" NVARCHAR(60),
	"ProductRecipientPartyUUID" NVARCHAR(36),
	"ProductRecipientPartyName" NVARCHAR(480),
	"IncidentServiceIssueCategoryID" NVARCHAR(25),
	"ID" NVARCHAR(35),
	"UUID" NVARCHAR(36),
	"Name" NVARCHAR(255),
	"EscalationStatusCode" NVARCHAR(2),
	"EscalationStatusCodeText" NVARCHAR(5000),
	"ServicePriorityCode" NVARCHAR(1),
	"ServicePriorityCodeText" NVARCHAR(5000),
	"RequestedFulfillmentPeriodStartDateTime" NVARCHAR(33),
	"RequestedFulfillmentPeriodEndDateTime" NVARCHAR(33),
	"RequestedTotalProcessingDuration" NVARCHAR(20),
	"RequestedTotalRequestorDuration" NVARCHAR(20),
	"RequestInitialReceiptdatetimecontent" NVARCHAR(33),
	"RequestCloseddatetimeContent" NVARCHAR(33),
	"SalesOrganisationID" NVARCHAR(20),
	"SalesUnitPartyID" NVARCHAR(60),
	"BuyerPartyID" NVARCHAR(60),
	"WarrantyGoodwillCode" NVARCHAR(2),
	"EscalationTimePointDateTime" NVARCHAR(33),
	"ResolutionDueDateTime" NVARCHAR(33),
	"SalesTerritoryID" NVARCHAR(6),
	"SalesUnitPartyName" NVARCHAR(480),
	"BuyerPartyName" NVARCHAR(480),
	"BuyerPartyUUID" NVARCHAR(36),
	"WarrantyID" NVARCHAR(60),
	"ServiceIssueCategoryID" NVARCHAR(25),
	"ServiceRequestClassificationCode" NVARCHAR(1),
	"ServiceRequestClassificationCodeText" NVARCHAR(5000),
	"CreationDateTime" TIMESTAMP(7)
) with type datasource engine 'FILES';

alter table "com_appInt_c4c_ServiceRequests_Parquet"
    add datasource parquet(S3('/sdl/landing_zone/appInt/c4c/ServiceRequests.parquet')) 
    using connection 'APPINT_S3';

load table "com_appInt_c4c_ServiceRequests_Parquet" reload all;

-- mc Interactions - ORC ------------------------------------------------------
drop table "com_appInt_mc_Interactions_ORC";

create table "com_appInt_mc_Interactions_ORC" (
	"InteractionUUID" NVARCHAR(36),
	"InteractionContactOrigin" NVARCHAR(20),
	"InteractionContactId" NVARCHAR(255),
	"CommunicationMedium" NVARCHAR(20),
	"InteractionType" NVARCHAR(20),
	"InteractionTimeStampUTC" TIMESTAMP(7) WITHOUT TIME ZONE,
	"InteractionSourceObjectType" NVARCHAR(30),
	"InteractionSourceObject" NVARCHAR(50),
	"MarketingArea" NVARCHAR(40),
	"CampaignID" NVARCHAR(10),
	"MarketingLocationOrigin" NVARCHAR(30),
	"MarketingLocation" NVARCHAR(50),
	"DigitalAccountType" NVARCHAR(10),
	"DigitalAccount" NVARCHAR(40),
	"MKT_AgreementOrigin" NVARCHAR(30),
	"MKT_AgreementExternalID" NVARCHAR(80),
	"CampaignContent" INTEGER,
	"InteractionWeightingFactor" INTEGER,
	"InteractionSentimentValue" INTEGER,
	"InteractionStatus" NVARCHAR(2),
	"InteractionReason" NVARCHAR(40),
	"InteractionLanguage" NVARCHAR(2),
	"InteractionIsAnonymous" NVARCHAR(5),
	"InteractionAmount" DECIMAL(31,14),
	"InteractionCurrency" NVARCHAR(3),
	"InteractionLatitude" DECIMAL(21,10),
	"InteractionLongitude" DECIMAL(21,10),
	"SpatialReferenceSystem" NVARCHAR(10),
	"DeviceType" NVARCHAR(60),
	"InteractionDeviceName" NVARCHAR(80),
	"PrecedingInteractionUUID" NVARCHAR(36),
	"SourceSystemType" NVARCHAR(20),
	"SourceSystem" NVARCHAR(255),
	"InteractionSourceObjectAddlID" NVARCHAR(50),
	"InteractionSourceObjectStatus" NVARCHAR(10),
	"InteractionSourceDataURL" NVARCHAR(5000),
	"InteractionSourceTimeStampUTC" TIMESTAMP(7) WITHOUT TIME ZONE,
	"CampaignContentLinkURL" NVARCHAR(5000),
	"CampaignContentLinkName" NVARCHAR(255),
	"ReferralSource" NVARCHAR(255),
	"ReferralSourceCategory" NVARCHAR(50),
	"InteractionContactUUID" NVARCHAR(36),
	"InteractionLastChangedDateTime" TIMESTAMP(7) WITHOUT TIME ZONE,
	"InteractionLastChangedByUser" NVARCHAR(12),
	"InteractionContentSubject" NVARCHAR(255),
	"InteractionContent" NVARCHAR(5000)
) with type datasource engine 'FILES';

alter table "com_appInt_mc_Interactions_ORC"
    add datasource orc(S3('/sdl/landing_zone/appInt/mc/Interactions.orc')) 
    using connection 'APPINT_S3';

load table "com_appInt_mc_Interactions_ORC" reload all;

-- mc Contacts - ORC ----------------------------------------------------------
drop table "com_appInt_mc_Contacts_ORC";

create table "com_appInt_mc_Contacts_ORC" (
	"InteractionContactOrigin" NVARCHAR(20),
	"InteractionContactID" NVARCHAR(255),
	"IsEndOfPurposeBlocked" NVARCHAR(5),
	"TrackingID" NVARCHAR(255),
	"OriginDataLastChgUTCDateTime" TIMESTAMP(7) WITHOUT TIME ZONE,
	"LastChangeDateTime" TIMESTAMP(7) WITHOUT TIME ZONE,
	"LastChangedByUser" NVARCHAR(12),
	"WebSiteURL" NVARCHAR(1000),
	"CreationDateTime" TIMESTAMP(7) WITHOUT TIME ZONE,
	"InteractionContactImageURL" NVARCHAR(1000),
	"CreatedByUser" NVARCHAR(12),
	"InteractionContactType" NVARCHAR(2),
	"InteractionContactUUID" NVARCHAR(36),
	"Latitude" DECIMAL(20,10),
	"Longitude" DECIMAL(20,10),
	"FullName" NVARCHAR(80),
	"SpatialReferenceSystem" NVARCHAR(10),
	"CityName" NVARCHAR(40),
	"StreetName" NVARCHAR(60),
	"AddressHouseNumber" NVARCHAR(10),
	"Language" NVARCHAR(2),
	"LanguageName" NVARCHAR(16),
	"EmailAddress" NVARCHAR(241),
	"PhoneNumber" NVARCHAR(30),
	"MobileNumber" NVARCHAR(30),
	"FaxNumber" NVARCHAR(30),
	"HasMktgPermissionForDirectMail" NVARCHAR(1),
	"Country" NVARCHAR(3),
	"CountryName" NVARCHAR(50),
	"AddressRegion" NVARCHAR(3),
	"RegionName" NVARCHAR(40),
	"ContactPostalCode" NVARCHAR(10),
	"Industry" NVARCHAR(4),
	"IndustryName" NVARCHAR(40),
	"IsObsolete" NVARCHAR(5)
) with type datasource engine 'FILES';

alter table "com_appInt_mc_Contacts_ORC"
    add datasource orc(S3('/sdl/landing_zone/appInt/mc/Contacts.orc')) 
    using connection 'APPINT_S3';

load table "com_appInt_mc_Contacts_ORC" reload all;

-- s4 BusinessPartners - Parquet ----------------------------------------------
drop table "com_appInt_s4_BusinessPartners_Parquet";

create table "com_appInt_s4_BusinessPartners_Parquet" (
	"BusinessPartner" NVARCHAR(10),
	"Customer" NVARCHAR(10),
	"Supplier" NVARCHAR(10),
	"AcademicTitle" NVARCHAR(4),
	"AuthorizationGroup" NVARCHAR(4),
	"BusinessPartnerCategory" NVARCHAR(1),
	"BusinessPartnerFullName" NVARCHAR(81),
	"BusinessPartnerGrouping" NVARCHAR(4),
	"BusinessPartnerName" NVARCHAR(81),
	"BusinessPartnerUUID" NVARCHAR(36),
	"CorrespondenceLanguage" NVARCHAR(2),
	"CreatedByUser" NVARCHAR(12),
	"CreationDate" TIMESTAMP,
	"CreationTime" TIMESTAMP,
	"FirstName" NVARCHAR(40),
	"FormOfAddress" NVARCHAR(4),
	"Industry" NVARCHAR(10),
	"InternationalLocationNumber1" NVARCHAR(7),
	"InternationalLocationNumber2" NVARCHAR(5),
	"IsFemale" NVARCHAR(5),
	"IsMale" NVARCHAR(5),
	"IsNaturalPerson" NVARCHAR(1),
	"IsSexUnknown" NVARCHAR(5),
	"Language" NVARCHAR(2),
	"LastChangeDate" TIMESTAMP,
	"LastChangeTime" TIMESTAMP,
	"LastChangedByUser" NVARCHAR(12),
	"LastName" NVARCHAR(40),
	"LegalForm" NVARCHAR(2),
	"OrganizationBPName1" NVARCHAR(40),
	"OrganizationBPName2" NVARCHAR(40),
	"OrganizationBPName3" NVARCHAR(40),
	"OrganizationBPName4" NVARCHAR(40),
	"OrganizationFoundationDate" TIMESTAMP,
	"OrganizationLiquidationDate" TIMESTAMP,
	"SearchTerm1" NVARCHAR(20),
	"AdditionalLastName" NVARCHAR(40),
	"BirthDate" TIMESTAMP,
	"BusinessPartnerIsBlocked" NVARCHAR(5),
	"BusinessPartnerType" NVARCHAR(4),
	"ETag" NVARCHAR(26),
	"GroupBusinessPartnerName1" NVARCHAR(40),
	"GroupBusinessPartnerName2" NVARCHAR(40),
	"IndependentAddressID" NVARCHAR(10),
	"InternationalLocationNumber3" NVARCHAR(1),
	"MiddleName" NVARCHAR(40),
	"NameCountry" NVARCHAR(3),
	"NameFormat" NVARCHAR(2),
	"PersonFullName" NVARCHAR(80),
	"PersonNumber" NVARCHAR(10),
	"IsMarkedForArchiving" NVARCHAR(5),
	"BusinessPartnerIDByExtSystem" NVARCHAR(20),
	"TradingPartner" NVARCHAR(6)
) with type datasource engine 'FILES';

alter table "com_appInt_s4_BusinessPartners_Parquet"
    add datasource parquet(S3('/sdl/landing_zone/appInt/s4/BusinessPartners.parquet')) 
    using connection 'APPINT_S3';

load table "com_appInt_s4_BusinessPartners_Parquet" reload all;

-- s4 CustomerReturns - CSV ---------------------------------------------------
drop table "com_appInt_s4_CustomerReturns_CSV";

create table "com_appInt_s4_CustomerReturns_CSV" (
	"CustomerReturn" NVARCHAR(10),
	"CustomerReturnType" NVARCHAR(4),
	"SalesOrganization" NVARCHAR(4),
	"DistributionChannel" NVARCHAR(2),
	"OrganizationDivision" NVARCHAR(2),
	"SalesGroup" NVARCHAR(3),
	"SalesOffice" NVARCHAR(4),
	"SalesDistrict" NVARCHAR(6),
	"SoldToParty" NVARCHAR(10),
	"CreationDate" DATE,
	"CreatedByUser" NVARCHAR(12),
	"LastChangeDate" DATE,
	"LastChangeDateTime" TIMESTAMP(7),
	"PurchaseOrderByCustomer" NVARCHAR(35),
	"CustomerPurchaseOrderType" NVARCHAR(4),
	"CustomerPurchaseOrderDate" DATE,
	"CustomerReturnDate" DATE,
	"TotalNetAmount" DECIMAL(16,3),
	"TransactionCurrency" NVARCHAR(5),
	"SDDocumentReason" NVARCHAR(3),
	"PricingDate" DATE,
	"RequestedDeliveryDate" DATE,
	"HeaderBillingBlockReason" NVARCHAR(2),
	"DeliveryBlockReason" NVARCHAR(2),
	"IncotermsClassification" NVARCHAR(3),
	"IncotermsTransferLocation" NVARCHAR(28),
	"IncotermsLocation1" NVARCHAR(70),
	"IncotermsLocation2" NVARCHAR(70),
	"IncotermsVersion" NVARCHAR(4),
	"CustomerPaymentTerms" NVARCHAR(4),
	"PaymentMethod" NVARCHAR(1),
	"RetsMgmtProcess" NVARCHAR(10),
	"ReferenceSDDocument" NVARCHAR(10),
	"ReferenceSDDocumentCategory" NVARCHAR(4),
	"RetsMgmtLogProcgStatus" NVARCHAR(1),
	"RetsMgmtCompnProcgStatus" NVARCHAR(1),
	"RetsMgmtProcessingStatus" NVARCHAR(1),
	"OverallSDProcessStatus" NVARCHAR(1),
	"TotalCreditCheckStatus" NVARCHAR(1),
	"OverallSDDocumentRejectionSts" NVARCHAR(1)
) with type datasource engine 'FILES';

alter table "com_appInt_s4_CustomerReturns_CSV"
    add datasource csv(S3('/sdl/landing_zone/appInt/s4/CustomerReturns.csv')) 
    using connection 'APPINT_S3'
    delimited by ';' skip 1;

load table "com_appInt_s4_CustomerReturns_CSV" reload all;

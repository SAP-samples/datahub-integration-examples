## Views in HANA for extracting the extracted data
The application integration scenario example contains some views that build a holistic perspective on the data that were extracted by the pipelines and that can be used to visualize the extracted data for instance in a SAC cockpit.

These views are:

### Business Partner Mapping

![](/doc/images/createHanaViews.businessPartnerMapping.png)

The view `com_sap_appint_businesPartnerMapping` unifies all business partners that were received from the SAP Marketing Cloud as `interaction contacts`, SAP Cloud for Customer as `corporate accounts` and S/4 HANA as `business partners`. The view tries to map the the business partners from these cloud systems by a simple id and name mapping. 

If the mapping was successfull the mapped instances of the different systems are shown in the same row as one `Business Partner`. If a business partner entry of one of the cloud systems could not be mapped with one of the other systes this entry is listed as a separate `Business Partner`.
Please regard that only a successful mapping between the business partners of the different cloud system enables you to compare the data of different cloud systems for one single `Business Partner`.

The mapping is done by the following properties:
* ID
    * SAP Marketing Cloud: `InteractionContactID` with `InteractionContactOrigin` 'SAP_C4C_BUPA'
    * SAP Cloud for Customer: `AccountId` of the corporate account 
    * S/4 HANA: `BusinessPartner` property of the extracted business partners
* Name
    * SAP Marketing Cloud: property `FullName`.
    * SAP Cloud for Customer: property `Name`.
    * S/4 HANA: property `BusinessPartnerFullName`.

For every entry of the unified `Business Partner` list a UID is created by the view to which the subsequent views refer to uniquely identify the related `Business Partner` 

### Date Series

![](/doc/images/createHanaViews.dateSeries.png)

The view `com_sap_appint_dateSeries` is a time series that shows the count of the business transactions extracted from the cloud systems per date of transaction and `Business Partner`.
Currently the count of the following business transactions is shown :
* SAP Cloud for Customer `Customer Orders`
* SAP Cloud for Customer `Service Requests`
* SAP Marketing Cloud `Complaint Interactions`
* SAP Marketing Cloud `Opportunities`
* S/4 HANA `Customer Returns`

### Date Currency Series

![](/doc/images/createHanaViews.dateCurrencySeries.png)

The view `com_sap_appint_dateCurrencySeries` is a time series that shows the count and the total amount in transaction currency of the business transactios extracted from the cloud systems per occuring date of transaction, currency, and `Business Partner`.
Currently the count and total amount of the following business transactions is shown per date, currency, and `Business Partner`:
* SAP Cloud for Customer `Customer Orders`
* SAP Cloud for Customer `Service Requests`
* SAP Marketing Cloud `Complaint Interactions`
* SAP Marketing Cloud `Opportunities`
* S/4 HANA `Customer Returns`


### All Dates Series

![](/doc/images/createHanaViews.allDatesSeries.png)

The view `com_sap_appint_allDatesSeries` is a time series that shows for all occuring dates the count and if given the total amount in transaction currency of the business transactios extracted from the cloud systems per occuring date of transaction, potentially currency, and `Business Partner`.  
In contrast to the view `com_sap_appint_dateCurrencySeries` which only shows dates at which amounts were informed by the source systems this view reports all dates at which transactions took place and shows the total amounts per currency for those dates if amounts were informed. 
Currently the count and possibly total amount of the following business transactions is shown per date, possibly currency, and `Business Partner`:
* SAP Cloud for Customer `Customer Orders` (count and total amount)
* SAP Cloud for Customer `Service Requests` (count only)
* SAP Marketing Cloud `Complaint Interactions` (count and possibly total amount )
* SAP Marketing Cloud `Opportunities` (count and possibly total amount)
* S/4 HANA `Customer Returns` (count and possibly total amount)

## How to import the Date Series View
Find below instructions for an automatical creation of the above views. Druing this automatic creation further views are created automatically that form intermediate steps for the final views.

### Prerequisites :

* your user has the privileges for the creation of views.
* a schema called `DH_INPUT` exists in your HANA system.
* you have copied the repository to a (local) folder which you can access to to select the sources to be imported. 

### Select the repository folder and import the tables:

In the navigation bar select the `File` and then `Import...` .

![](/doc/images/createHanaViews.FileMenu.png)

In the import popup select the import source `SAP HANA` and there select `Catalog Objects`. Then push `Next`.

![](/doc/images/createHanaViews.ImportSelectCatalogObjects.png)

Select the system that you want to import the tables into. Then push `Next`.

![](/doc/images/createHanaViews.SelectSystem.png)

Select the option `import catalog objects from current client` and push `Browse`.

![](/doc/images/createHanaViews.SpecifiyLocation.png)

Navigate to your copy of the reposistory and there select the folder `dateSeries` at path `scr/hana/com/appint`.
Push `ok`. Then push `Next`.

![](/doc/images/createHanaViews.SpecifyLocation_SelectDateSeries.png)

In the `Matchting Items` area select the tables that you want to create (possibly all) and push `Add`. Now the `Selected Catalog Objects` area is filled. Then push `Next`.

![](/doc/images/createHanaViews.SelectCatalogObjectsForImport.png)

In the `Options for Catalog Object Import` set the option `Replace existing catalog object`.
(As the same intermediate views occur both for the date series and the date currency series this option avoids that you run into trouble when you import both views)Then push `Finish`.

![](/doc/images/createHanaViews.OptionsForCatalogObjectImport.png)

Now the date series view and all implied views are created as you can see when you check folder `Views` in  `DH_INPUT`.


## How to import the Date Currency Series View

Proceed in the same way as described for the Date Series above.
When you specify the location from which the view definition is copied select `dateCurrencySeries`  instead of `dateSeries`.

![](/doc/images/createHanaViews.SpecifyLocation_SelectDateCurrencySeries.png)


## How to import the All Dates Series View

Proceed in the same way as described for the Date Series above.
When you specify the location from which the view definition is copied select `allDatesSeries`  instead of `dateSeries`.

![](/doc/images/createHanaViews.SpecifyLocation_SelectAllDatesSeries.png)

Finally the following views should be present in your HANA system when you have created the Date Series and the Date Currency Series views (check folder `Views` in  `DH_INPUT`):

![](/doc/images/createHanaViews.ViewsOverview.png)


## How to publish the views to SAC

For the consumption of the above views by SAC your HANA system must provide calculation views for those views. Such calculations views for the above described views are part of the current solution.

The instructions below refer to SAP HANA Studio (Version: 2.2.12.) in the SAP HANA modeler perspective.

In order to create those calculation views in your HANA system preceed as follows:

### Prerequisites :

* your user has the privileges for the creation calculation views.
* a content folder `DH_E2E` exists in your HANA system.
* you have already imported the delivered data base views as described in the two chapters before.
* you have copied the repository to a (local) folder which you can access to to select the sources to be imported. 

### Select the repository folder and import the calculation views:

In the navigation bar select the `File`and then `Import...` .

![](/doc/images/createCalcViews.FileMenu.png)

As import source select the `SAP HANA Content`and there `Developper Mode` . Then push `Next`.

![](/doc/images/createCalcViews.SelectHANAContent.png)

Select the system that you want to import the tables into. Then push `Next`.

![](/doc/images/createCalcViews.TargetSystem.png)

In the `Select System Folder` popup set option `Overwrite Existing Objects`. Then push `Browse` for the source location. 


![](/doc/images/createCalcViews.SelectSystemFolder_empty.png)

Navigate to your copy of the reposistory and there select the folder `hanaContent` at path `scr/hana/com/appint`.
Push `ok`.

![](/doc/images/createCalcViews.SelectSystemFolder.png)

In the `Objects For Import` area expand the `Content` folder and there the `DH_E2` folder so that folder `calculation views` is visible. Mark the `calculation views` folder and then push `add`. Now, at the right area 3 calcualtion views should appear. Push `Finish` so that the calculation views will be created.

![](/doc/images/createCalcViews.SelectSystemFolder_addObjects.png)

When the creation was successfull in the content folder `DH_E2E` the following calculation views should appear:

![](/doc/images/createCalcViews.Overview.png)

The imported calculation view definitions are not yet activated. For the activation do a right-click on one of the imported calculation views. In the popup push `Activate`.

![](/doc/images/createCalcViews.Activate.png)

Now a pupup appears that contains the newly imported calculation views in the `Available` area. Select the imported calculation views then push `Add` so that the calculation views appear now in the `Selected` area.
Then push `Activate`.

![](/doc/images/createCalcViews.ActivateSelect.png)

Now the calculation views are active and ready for consumption by SAC.



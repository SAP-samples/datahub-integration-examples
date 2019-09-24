## How to create the tables in the HANA system that are the target tables of the pipelines
Find below instructions for an automatical creation of the target tables that are filled when you run the HANA pipelines. Each table corresponds to exactly one pipeline that fills it. Depending on the pipelines that you want to use you may select the tables that will be created. 

* Note: If you want to make use of the views that are contained in the template to transform the imported data you must import all tables mentioned below regardless of whether they will be filled or not. Otherwhise the import of the views will fail.  

The instructions below refer to SAP HANA Studio (Version: 2.2.12.) in the SAP HANA modeler perspective.

If you want to run all pipelines the set of tables to be created in the HANA system is as you can see here: 

![](/doc/images/createHanaTables.ImportedTables.png)


### Prerequisites :

* your user has the privileges for the creation of tables.
* a schema called `DH_INPUT` exists in your HANA system.
* you have copied the repository to a (local) folder which you can access to to select the sources to be imported. 

### Select the repository folder and import the tables:

Open the HANA studio and logon to the system to which you want to import the table definitions.

In the navigation bar select the `File`and then `Import...` .

![](/doc/images/createHanaTables.FileMenu.png)

In the import popup select the import source `SAP HANA` and there select `Catalog Objects`. Then push `Next`.

![](/doc/images/createHanaTables.ImportSelect.png)

Select the system that you want to import the table definitions into. Then push `Next`.

![](/doc/images/createHanaTables.ImportSelect_2.png)

Select the option `import catalog objects from current client` and push `Browse`.

![](/doc/images/createHanaTables.ImportSelect_3.png)

Navigate to your copy of the reposistory and there select the folder `tables` at path `scr/hana/com/appint`.
Push `ok` and then `next`.

![](/doc/images/createHanaTables.ImportSelect_4.png)

In the `Matchting Items` area select the tables that you want to create (possibly all) and push `Add`. Now the `Selected Catalog Objects` area is filled. Push `next`.

![](/doc/images/createHanaTables.SelectCatalogObjects.png)

In the `Options for Catalog Object Import` leave the check boxes empty.

* Note: Do not set the check box `Replace existing catalog object`. Otherwhise existing data may be lost ! Push `finish`.

![](/doc/images/createHanaTables.OptionsForImport.png)

Now the tables are created. Check folder `Tables` in  `DH_INPUT` for all selected table definitions.

## What to do when some target tables already exist:
It could happen that target tables already exist in the hana system. In order to prevent loss of data you should not overwrite the existing tables by this import but exclude them from the import list.

If you did not check the existing tables before the import and if a table already exists you get an error message after you have selected the hana tables and started the import. Then proceed as follows.

![](/doc/images/createHanaTables.ImportError.png)

In the above popup push the `back` button which leads you again to the `Select Catalog Objects for Import` popup:

![](/doc/images/createHanaTables.RemoveCatalogObject.png)

Mark the table(s) that already exists in the `Selected Catalog Objects` area. Then push the `Remove` button.
After this action the duplicate table(s) do no longer appear in the right list:

![](/doc/images/createHanaTables.NewCatalogObjectSelection.png)

Now, continue as described above in order to create the remaining tables automatically.







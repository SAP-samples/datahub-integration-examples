# Create Vora Tables

## Description

This graph creates the set of tables in the SAP Data Hub Vora database that will be needed when using the SQL-on-File feature of SAP Data Hub. 

The graph is composed of the following components:
- Read File: Reads a file that contains Vora database table metadata (incl. the attachment of Amazon S3 files) in the form of SQL statements (mainly `CREATE TABLE`). (Note that these data will be evaluated only when executing a query; they will never actually be loaded into the database tables.)
- Vora Client: Executes the SQL statements read from the file.
- Terminal: Shows results of the operation.

## Prerequisites

- For this graph to run you will need the following:
    - Have executed the other example graphs to produce extracted data as files in Amazon S3
    - Configured connection to Amazon S3 with ID `APPINT_S3`
        - Remark: you can also use corresponding object store solutions from Microsoft Azure or Google Cloud Platform.

## Configure and Run the Graph

If you are implementin the complete Application Integration Example scenario as is there is no need to configure this graph. 

If you want to use only parts of, or modify, the scenario you will need to change the file containing the Vora table metadata using `System Management` -> `Files`. The file is located at `/vrep/vora/createTables.sql`. Alternatively, you can use your own file. In this case you need to adapt the configuration of the `Read SQL File` operator accordingly.

<br>
<div class="footer">
   &copy; 2019 SAP SE or an SAP affiliate company. All rights reserved.
</div>

# SQL-on-File Demo

## Description

This graph demonstrates how to access the data located in Amazon S3 via SQl-on-files. In this case the goal is to join two tables - both are based on CSV files in Amazon S3 and are exposed via Vora SQL-on-file - and write the result in CSV format into Amazon S3.

The graph is composed of the following components:
- Terminal: show the resulting filename of the created CSV file.
- Constant Generator: create the required SQL statement.
- SAP Vora Client: send the SQL command to Vora SQL-on-file. The output port will be filled with the result of the SQL command, in this case a join between two tables
- Format Converter: converts the result of the SQL query to CSV format
- WriteFile: writes the resulting CSV into Amazon S3

## Prerequisites

- For this graph to run you will need the following:
    - Configured connection to Amazon S3 with ID `APPINT_S3`
        - Remark: you can also use corresponding object store solutions from Microsoft Azure or Google Cloud Platform.
    - Configured connection to Vora with ID `APPINT_VORA`
        

## Configure and Run the Graph

1. Adapt the SQL command in the `Content` config of the `Constant Generator` operator as required.
2. Adapt the target location in S3 for the generated file. Default location is:
`/sdl/data_zone/appInt/mc_interactionsWithContactData.csv`
3. Save and run the graph. 
4. Use the `Terminal` operator to validate the successful execution.

<br>
<div class="footer">
   &copy; 2019 SAP SE or an SAP affiliate company. All rights reserved.
</div>

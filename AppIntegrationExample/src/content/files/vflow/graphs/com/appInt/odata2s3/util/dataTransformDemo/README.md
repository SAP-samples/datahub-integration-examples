# Data Transf. Demo

## Description

This graph demonstrates how to join the data in Amazon S3 using the Data Transform operators. This is an essential concept since it allows to combine extracted data from multiple applications. The same is done in this scenario as well in HANA with the Calculation Views. This graph shows how the same can be achieved directly on Amazon S3. The core technology to achieve this goal is the Data Transform capability. In this concrete example Interactions and Contacts will be joined.

The graph is composed of the following components:
- Data Transform: This is a complex operator able to visually model the join between the involved data sources. Double-click the operator to go to the details screen.
- Terminal: Shows results of the operation.

## Prerequisites

- For this graph to run you will need the following:
    - Have executed the other example graphs to produce extracted data as files in Amazon S3
    - Configured connection to Amazon S3 with ID `APPINT_S3`
        - Remark: you can also use corresponding object store solutions from Microsoft Azure or Google Cloud Platform.

## Configure and Run the Graph

1. Double-click on the Data Transform operator
2. Double-click on Interactions and check the first file (representing extracted interactions). Default is:
   `/sdl/landing_zone/appInt/mc/Interactions.orc`
3. Double-click on Contacts and check the second file (representing extracted contacts). Default is:
   `/sdl/landing_zone/appInt/mc/Contacts.orc`
4. Double-click on ComplainsWithContacts and check the third file. This file will contain the result of the join. Default is:
   `/sdl/data_zone/appInt/transformedInteractionsWithContactData.csv`
5. Double-click on the join-operator itself and valide the join conditions.
6. Leave the detail screen of the Data Transform operator.
7. Save and run the graph. 
8. Use the Terminal operator to view the status of the Pipeline during execution.

<br>
<div class="footer">
   &copy; 2019 SAP SE or an SAP affiliate company. All rights reserved.
</div>

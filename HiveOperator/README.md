HiveOperator [(Source code)](https://github.com/SAP/datahub-integration-examples/blob/master/HiveOperator/src/vrep/vflow/subengines/com/sap/python27/operators/examples/HiveOperator/script.py)
------------

Test

This operator provides functionality to query a Hive Metastore server using a HiveQL string and returns a response in the format of a delimited string.

The operator runs on a custom Docker images that extends the SAP-deliver docker image `com.sap.python2.7` and uses the Kerberos client binary `krb5-user` as well as `libsasl2` for Ubuntu. The PyHive python module is developed and maintained by Dropbox: https://github.com/dropbox/PyHive

![alt text](./graph.jpg "Graph")

[(Graph source code)](https://github.com/SAP/datahub-integration-examples/blob/master/HiveOperator/src/vrep/vflow/graphs/HiveOperator_test/graph.json)

![alt text](./Hive_Sql.jpg "Hive SQL example")

## Requirements
Before you start using the example, please make sure that:

- Hive Metastore server, such as one hosted on Ambari Hortonworks or Cloudera.
- You are familiar with the basic concepts of SAP Data Hub Modeling such Pipelines (Graphs), Operators and Dockerfiles.  For more information, you may refer to the Modeling Guide for SAP Data Hub that is available on the SAP Help Portal (https://help.sap.com/viewer/p/SAP_DATA_HUB).
- You are familiar with the basic concepts of Docker (https://docs.docker.com/get-started/) and Kubernetes (https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/).


## Content
**1. Dockerfile**
  - Extends the SAP-delivered Dockerfile com.sap.python27
  - Imports the python library `pyhive`
  - Install Kerberos client libraries

**2. Custom operator 'HiveOperator'**
  - Derived from Pythin20Operator
  - Uses image tags `python27:""` and `pyhive:pip2`
  - **input port `inSql` of type string:** expects a single HiveQL-compliant string without a semicolon
  - **output port `output` of type string:** outputs the response from the Hive Metastore server, columns are delimited by a comma (default) but can be overriden using the `delimiter` configuration parameter (See description below)

**3. Sample graph HiveOperator_test**
  - Provides an interactive terminal to query a Hive Metastore server and display the results. Note, the HiveOperator can only process one HiveQL statement at a time.


## How to run
  - Import [solution/HiveOperator-1.0.tgz](solution/HiveOperator-1.0.tgz) via `SAP Data Hub System Management` -> `Files` -> `Import Solution`
  - Run the `Graph` -> `examples.HiveOperator_test`
  
**Operator configuration parameters**

	database:                 Specify which database in Hive metastore to connect to
	delimiter:		  Used to separate columns in HiveOperator output e.g. 1.34;Hello;World;
	hive_hostname:		  Hostname or IP address to Hive Metastore server
	hive_port:		  Port used by Hive Metastore server
	http_mode:		  If hive.server2.transport.mode is set to http, set this parameter to true
	kerberos_enabled:	  If Hive cluster is kerberized set to true and read additional notes below
	kerberos_keytab_filename: The file name of the uploaded keytab file (case sensetive)
	kerberos_principal: 	  Kerberos principal used with uploaded keytab file
	kerberos_realm: 	  Kerberos realm used with principal and keytab file
	username: 		  Username for plain authentication
	password: 		  Password for plain authentication

**Kerberos configuration**
(Optional) Upload .keytab and krb5.conf file via the HiveOperator designer. These will be copied into the docker container at runtime. Remember to specify the kerberos realm and principal name in the operator's configuration section when designing your graph.

![alt text](./upload.gif "Upload")

**Troubleshooting**

For detailed errors messages check the failing vflow pod's log.
Note: Bad HiveQL syntax will cause the graph to terminate. HiveQL statements must not include a semicolon.

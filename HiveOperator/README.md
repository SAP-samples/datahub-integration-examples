HiveOperator
------------
This operator querying a Hive Metastore server and using a HiveQL string and returns a response in the format of a delimited string.

The operator runs on a custom Docker images that extends the SAP-deliver docker image `com.sap.python2.7` and uses the Kerberos client binary `krb5-user` as well as `libsasl2` for Ubuntu. The PyHive python module is developed and maintained by Dropbox: https://github.com/dropbox/PyHive

![alt text](./graph.jpg "Graph")
![alt text](./Hive_Sql.jpg "Hive SQL example")

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
(Optional) Upload .keytab and krb5.conf file via the HiveOperator designer. These will be copied into the docker container at runtime.

![alt text](./upload.gif "Upload")

**Troubleshooting**
For detailed errors messages check the failing vflow pod's log.
Note: Bad HiveQL syntax will cause the graph to terminate. HiveQL statements must not include a semicolon.

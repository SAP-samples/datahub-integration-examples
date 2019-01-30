from pyhive import hive
from subprocess import call
import base64 
from thrift.transport.THttpClient import THttpClient 

hostname = api.config.hive_hostname 
port = api.config.port
user = api.config.username
password = api.config.password
database= api.config.database
kerberos_enabled = api.config.kerberos_enabled
kerberos_keytab = "/keytabs/" + api.config.kerberos_keytab_filename
kerberos_principal = api.config.kerberos_principal + "@" + api.config.kerberos_realm
http_enabled = api.config.http_mode

if(kerberos_enabled):
    call(["cp","/vrep/vflow/subengines/com/sap/python27/operators/examples/HiveOperator/"+api.config.kerberos_keytab_filename,"/keytabs"])
    call(["cp","/vrep/vflow/subengines/com/sap/python27/operators/examples/HiveOperator/krb5.conf","/etc"])
    call(["/usr/bin/kinit","-kt",kerberos_keytab, kerberos_principal])

def on_input(inSql):
   
    hiveconnection(inSql)

def add_http_mode_support(username=user, password=password, port=port, httpPath="/cliservice", host=hostname, transportMode="http"):
    ap = "%s:%s" % (username, password)
    _transport = THttpClient(host,port=port,path=httpPath)
    _transport.setCustomHeaders({"Authorization": "Basic "+base64.b64encode(ap).strip()})
    return _transport
    
def hiveconnection(inSql):
    if(kerberos_enabled):
        auth = "KERBEROS"
        kerberos_service_name = "hive"
        password = None
    else:
        password = api.config.password
        auth = 'CUSTOM'
        kerberos_service_name = None

    if(http_enabled):
        conn = hive.connect(thrift_transport=add_http_mode_support()) 
    else:
        conn = hive.Connection(host=hostname, port=port, username=user,password=password,database=database, auth=auth,kerberos_service_name=kerberos_service_name)
    
    cur = conn.cursor()
    cur.execute(inSql)
    resultList = cur.fetchall()

    string = ""
    for x in resultList:
        for y in x:
            string = string + str(y) + api.config.delimiter ## Delimiter to separate Hive columns in output
        string = string + "\n"

    api.send("output",string)



api.set_port_callback("inSql", on_input)
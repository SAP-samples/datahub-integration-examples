
import os
import requests
import pandas as pd


#
# get all users
#
def get_users(connection):
    restapi = "/auth/v2/user"
    url = connection['url'] + restapi
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    resp = requests.get(url, headers=headers, auth=connection['auth'], verify=True)

    users = resp.json()

    return users


#
# Callback of operator
#
def gen():
    host = api.config.connection_id['connectionProperties']['host']
    user = api.config.connection_id['connectionProperties']['user']
    pwd = api.config.connection_id['connectionProperties']['password']
    tenant = os.environ.get('VSYSTEM_TENANT')

    if not tenant:
        api.logger.warning("No system variable \'VSYSTEM_TENANT\' set.")
        tenant = 'default'
    connection = {'url': host, 'auth': (tenant + '\\' + user, pwd)}

    # process
    users = get_users(connection)

    df = pd.DataFrame(users)
    df = df.loc[:, ['tenant', 'username']]
    df = df[['tenant', 'username']]

    # output
    header = {"com.sap.headers.batch": [0, True, 1, 0, ""],
              "extract.connection_http": [host, user, pwd, '', tenant]}


    tbl1 = api.Table(df.values.tolist(), 'extract.users')
    api.outputs.output.publish(tbl1, header=header)


api.set_prestart(gen)
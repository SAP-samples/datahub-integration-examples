import fromCSVDataFrame as fromcsv
import sampleDataFrame as sampledf
import joinDataFrames as joindf
import toCSVDataFrame as tocsv
import selectDataFrame as selectdf

import json


msg_oh  = fromcsv.api.test_call(fromcsv.test.ORDER_HEADERS)
info_str = json.dumps(msg_oh.attributes, indent=4)
print(info_str)

msg_oh = sampledf.api.test_call(msg_oh,sampledf.test.BIGDATA)
info_str = json.dumps(msg_oh.attributes, indent=4)
print(info_str)

msg_od  = fromcsv.api.test_call(fromcsv.test.ORDER_DETAILS)
info_str = json.dumps(msg_od.attributes, indent=4)
print(info_str)

msg = joindf.api.test_call(msg_oh,msg_od,joindf.test.ORDER_HEADER_DETAIL)
info_str = json.dumps(msg.attributes, indent=4)
print(info_str)

#msg = selectdf.api.test_call(msg)
#info_str = json.dumps(msg.attributes, indent=4)
#print(info_str)

msg_pmd  = fromcsv.api.test_call(fromcsv.test.PRODUCTS_MD)
info_str = json.dumps(msg_pmd.attributes, indent=4)
print(info_str)

msg = joindf.api.test_call(msg,msg_pmd,joindf.test.ORDER_PRODUCT_MD)
info_str = json.dumps(msg.attributes, indent=4)
print(info_str)

csv = tocsv.api.test_call(msg)
with open(r"/Users/d051079/OneDrive - SAP SE/Datahub-Dev/data/sample_pos.csv", 'w') as fd:
    if isinstance(csv.body,list) :
        for s in csv.body :
            fd.write(s)
    else :
        fd.write(csv.body)
fd.close()

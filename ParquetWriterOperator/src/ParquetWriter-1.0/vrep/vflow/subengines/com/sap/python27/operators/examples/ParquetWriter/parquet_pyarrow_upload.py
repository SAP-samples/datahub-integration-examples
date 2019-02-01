import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def on_input(data):
    
    #create pandas data frame from Data section (=query result from HANA Client)
    body = data.body
    df = pd.read_json(json.dumps(body))
    
    # use pyarrow to write dataframe into buffer
    pt = pa.Table.from_pandas(df)
    output = pa.BufferOutputStream()
    pq.write_table(pt, output)
    buf = output.getvalue()

    # send output to next operator
    api.send("output", api.Message(str(buf.to_pybytes()), None))

api.set_port_callback("input", on_input)

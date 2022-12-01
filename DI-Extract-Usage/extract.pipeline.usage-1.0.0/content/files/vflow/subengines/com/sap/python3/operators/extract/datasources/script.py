# For more information about the Python3Operator, drag it to the graph canvas,
# right click on it, and click on "Open Documentation".

# To uncomment the snippets below you can highlight the relevant lines and
# press Ctrl+/ on Windows and Linux or Cmd+/ on Mac.

# # Basic Example 1: Count inputs so far and send on output port (port type
# com.sap.core.string)
# # When using the snippet below make sure you create an output port of type
# #string
# counter = 0
#
# def on_input(msg_id, header, body):
#     global counter
#     counter += 1
#     api.outputs.output.publish(str(counter))
#
# api.set_port_callback("input", on_input)


# # Basic Example 2: Read incoming table as stream and send it
# as stream as well to the output port (any table port type),
# # When using the snippet below make sure you create an input and output
# # port of table type
#
# import threading
# chunk_size = 10
# 
# # Since this is run in a different thread, exceptions on it will not
# # trigger any action. Alternatives are using `api.propagate_exception
# # or sending through a queue to the operator main thread (the callback one).
# def process_batch(body):
#     try:
#         reader = body.get_reader()
#         # These two line is needed if the output port is of type-id "*" (dynamic)
#         # It specifies the type of the dynamic table output which is
#         # in this case the type of the given input table
#         table = reader.read(chunk_size)
#         api.outputs.output.set_dynamic_type(table.type_ref)
#         try:
#           # This allows creating one output stream per thread,
#           # each being able to send data in parallel.
#           msg_id, writer = api.outputs.output.with_writer()
#           # Send the first chunk before running the while loop
#           writer.write(table)
#           while True:
#               table = reader.read(chunk_size)
#               # When the stream is closed, len(table) < expected.
#               # If -1 was passed, read would wait for stream to close
#               if len(table) <= 0:
#                   api.logger.info('End of table')
#                   break
#              
#               writer.write(table)
#         finally:
#           writer.close()
#     except Exception as ex:
#         api.propagate_exception(ex)
# 
# def on_input(msg_id, header, body):
#     # Since each input thriggers a thread, it is possible to have
#     # multiple actions happening in parallel.
#     threading.Thread(target=process_batch, args=[body]).start()
# 
# api.set_port_callback("input", on_input)


# # Basic Example 3: Snapshot support, more details at the operator
# # documentation.
# # This operator will accumulate all the numeric values it gets on the input
# # and it will recover when the graph crashes with the accumulated value stored as state of this operator
# # When using the snippet below make sure you create input of the com.sap.core.int64
# # and output port of the com.sap.core.string type.
# # You can use Basic Example 4 as a generator operator for the integer inputs of this example
# # Also make sure to start the graph with State Management enabled (via Run As..)
#
# # Statemanagement needs to be only implemented for operators which need to store a state
# # that influences the processing of the input messages (like in this example adding the accumulated value to the output).
# # If you can process the input message independently of any state variable
# # (e.g. the output is always the same for the same input message after a graph recovery)
# # then you don't need to implement these methods as your operator is considered stateless.
# import pickle
# import random
# import time
#
# # Internal operator state
# acc = 0
#
# def on_input(msg_id, header, body):
#     global acc
#     v = body.get()
#     acc += v
#     if random.randint(1,101) % 100 == 0:
#         # Enforce a crash with 1% chance to enforce a recovery restart
#         # But sleep 10 seconds to ensure that you can view the results of the output
#         time.sleep(10)
#         raise Exception("crashed with 1% chance. Feel free to adjust the chance based on your needs.")
#     api.outputs.output.publish("%d: %d" % (v, acc))
#
# api.set_port_callback("input", on_input)
#
# # It is required to have `is_stateful` set, but since this operator
# # script does not define a generator no information about output port is passed.
# # More details in the operator documentation.
#
# api.set_initial_snapshot_info(api.InitialProcessInfo(is_stateful=True))
#
# def serialize(epoch):
#     return pickle.dumps(acc)
#
# api.set_serialize_callback(serialize)
#
# def restore(epoch, state_bytes):
#     global acc
#     acc = pickle.loads(state_bytes)
#
# api.set_restore_callback(restore)
#
# def complete_callback(epoch):
#     api.logger.info(f"epoch {epoch} is completed!!!")
#
# api.set_epoch_complete_callback(complete_callback)
# 
# # Basic Example 4: Prestart
# # When using the snippet below make sure you create an output port of type
# # com.sap.core.int64
# counter = 0
#
# def gen():
#     global counter
#     for i in range(10000):
#         api.outputs.output.publish(counter)
#         counter += 1
#
# api.set_prestart(gen)

# # Basic Example 5: Timer
# # When using the snippet below make sure you create an output port of type
# # com.sap.core.binary
# import os
# from io import BytesIO
# import datetime
#
# # Function called when operator handling mode is set to `retry`
# # (more details at the operator documentation)
# def custom_response_callback(msg_id, ex):
#     if ex:
#         api.logger.error("Error when publishing %s: %s" % (str(msg_id), str(ex)))
#
#
# def time_callback():
#     dummy_bytes = os.urandom(20)
#     dummy_binary = BytesIO(dummy_bytes)
#     dummy_headers = {
#         # header (structure) type-id: api.Record([list of structure fields])
#         "com.sap.headers.file": api.Record([
#             "dummyConnection", # connection
#             "dummy/Path", # path
#             len(dummy_bytes), # size
#             False, #isDir
#             datetime.datetime.now().isoformat() # modTime
#         ])
#     }
#     # Send all binary data at once to the output, if only the first
#     # 10 bytes were to be sent, `n` = 10
#     msg_id = api.outputs.output.publish(dummy_binary, -1,
#                                         header=dummy_headers,
#                                         response_callback=custom_response_callback)
#     # Controls the time until the next call to time_callback
#     return 1
#
# api.add_timer(time_callback)

# # Basic Example 6: Shutdown
# # The shutdown function will be called when the operator receives a stop signal
# # In this example it prints a simple information in the trace logs with the current message counter
# # When using the snippet below make sure you create an input port of an arbitrary type and stop the graph
# # You can check the graph diagnostics / traces of the graph for the shutdown message when the graph stopped.
# counter = 0
#
# def on_input(msg_id, header, body):
#     global counter
#     counter += 1
#
# api.set_port_callback("input", on_input)
#
# def shutdown():
#     api.logger.info("shutdown: %d" % counter)
#
# api.set_shutdown(shutdown)

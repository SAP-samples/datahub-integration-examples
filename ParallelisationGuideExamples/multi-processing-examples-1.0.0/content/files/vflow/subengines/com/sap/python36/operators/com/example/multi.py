import time


# Used for Master-Slave Pattern
def parallel_fun(q_in, q_out):
    while True:
        shutdown, x = q_in.get()
        if shutdown is True:
            break
        time.sleep(1)
        q_out.put(("done"))


# Used for spawned Daemon Processes Example
def parallel_fun2(message, q_out):
    time.sleep(1)
    q_out.put((message))


# Used for Process Pools Example
def parallel_fun3(message):
    time.sleep(1)
    return message
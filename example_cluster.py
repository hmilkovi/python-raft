import time
import uuid
import sys

from src.raft import RaftKv


raft = RaftKv()

while True:
    if sys.argv[1] == 'write':
        print("start insert 10 key values individual")
        start_time = time.time()
        for i in range(10):
            uuid_str = str(uuid.uuid4())
            print(f"Write {i}:{uuid_str}")
            raft.set(i, uuid_str)
        print("--- %s seconds ---" % (time.time() - start_time))
        time.sleep(1)
        print("start insert 10 key values batch")
        start_time = time.time()
        data = {}
        for i in range(10):
            data[i] = str(uuid.uuid4())
            print(f"Prepare for batch {i}:{data[i]}")
        raft.set_many(data)
        print("--- %s seconds ---" % (time.time() - start_time))
        time.sleep(10)
    else:
        print("start read key values")
        start_time = time.time()
        for i in range(10):
            print(f"Read {i}:{raft.get(i)}")
        print("--- %s seconds ---" % (time.time() - start_time))
        time.sleep(2)
    print(f"Is connected: {raft.is_connected_to_others()}")
    print(f"Has quorum: {raft.has_quorum()}")
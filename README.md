# Python-Raft
This is built so it can be used directly in code so we can avoid adding Redis, Etcd or smililar to the stack.

Main features:
- KV based on diskcache python lib that is replicated via Raft supports set, get, set_many, delete and expire of keys
- Disributed lock via built in lock inside PySyncObj
- Resistance on disk via diskcache and also presistant Raft

Use cases:
- Distributed web application server side sessions
- Distributed locking
- Distributed processing of data
- Distributed cache


# Built on top
This lib si built on top:
- https://github.com/bakwc/PySyncObj
- https://github.com/grantjenks/python-diskcache

# Run example cluster
```
RAFT_DATA=raft1.kv RAFT_SELF=127.0.0.1:6000 RAFT_OTHER_NODES=127.0.0.1:6001,127.0.0.1:6002 RAFT_JOURNAL_FILE=journal1.bin RAFT_FULL_DUMP_FILE=fulldump1.bin  python example_cluster.py write
RAFT_DATA=raft2.kv RAFT_SELF=127.0.0.1:6001 RAFT_OTHER_NODES=127.0.0.1:6000,127.0.0.1:6002 RAFT_JOURNAL_FILE=journal2.bin RAFT_FULL_DUMP_FILE=fulldump2.bin  python example_cluster.py read
RAFT_DATA=raft3.kv RAFT_SELF=127.0.0.1:6002 RAFT_OTHER_NODES=127.0.0.1:6001,127.0.0.1:6000 RAFT_JOURNAL_FILE=journal3.bin RAFT_FULL_DUMP_FILE=fulldump3.bin  python example_cluster.py read
```
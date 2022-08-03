# python-raft
This lib uses https://github.com/bakwc/PySyncObj for Raft kv with lock features to be used in Python (please star it if you star this project)

# Run example cluster
```
RAFT_DATA=raft1.kv RAFT_SELF=127.0.0.1:6000 RAFT_OTHER_NODES=127.0.0.1:6001,127.0.0.1:6002 RAFT_JOURNAL_FILE=journal1.bin RAFT_FULL_DUMP_FILE=fulldump1.bin  python example_cluster.py write
RAFT_DATA=raft2.kv RAFT_SELF=127.0.0.1:6001 RAFT_OTHER_NODES=127.0.0.1:6000,127.0.0.1:6002 RAFT_JOURNAL_FILE=journal2.bin RAFT_FULL_DUMP_FILE=fulldump2.bin  python example_cluster.py read
RAFT_DATA=raft3.kv RAFT_SELF=127.0.0.1:6002 RAFT_OTHER_NODES=127.0.0.1:6001,127.0.0.1:6000 RAFT_JOURNAL_FILE=journal3.bin RAFT_FULL_DUMP_FILE=fulldump3.bin  python example_cluster.py read
```
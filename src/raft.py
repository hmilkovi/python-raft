import os

from pysyncobj import SyncObj, SyncObjConf, replicated
from pysyncobj.batteries import ReplLockManager

from .storage import KvDriver


class RaftKv(SyncObj):

    def __init__(self):
        raft_data_path: str = os.environ.get('RAFT_DATA', 'raft.kv').rstrip("/")
        jorunal_file: str = os.environ.get('RAFT_JOURNAL_FILE', 'journal.bin')
        dull_dump_file = os.environ.get('RAFT_FULL_DUMP_FILE', 'fulldump.bin')
        conf = SyncObjConf(
            dynamicMembershipChange=True,
            password=os.environ.get('RAFT_PASSWORD', None),
            journalFile=f"{raft_data_path}/{jorunal_file}",
            fullDumpFile=f"{raft_data_path}/{dull_dump_file}",
            serializer=self.__serialize,
            deserializer=self.__deserialize
        )
        conf.logCompactionMinTime = os.environ.get('RAFT_LOG_COMPATCTION_MIN_TIME', 10)
        conf.logCompactionMinEntries = os.environ.get('RAFT_LOG_COMPATCTION_MIN_ENTRIES', 5000)

        selfNodeAddr = os.environ.get('RAFT_SELF', '127.0.0.1:6000')
        otherNodeAddrs = [x.strip() for x in os.environ.get('RAFT_OTHER_NODES', '127.0.0.1:6001,127.0.0.1:6002').split(',')]
        self.__driver = KvDriver(db_path=raft_data_path)
        self.lock = ReplLockManager(autoUnlockTime=os.environ.get('RAFT_LOCK_AUTO_UNLOCK_TIME', 30))

        SyncObj.__init__(self, selfNodeAddr, otherNodeAddrs, conf, consumers=[self.lock])

    def __serialize(self, fileName, raftData):
        self.__driver.serialize(fileName, raftData)

    def __deserialize(self, fileName):
        return self.__driver.deserialize(fileName)

    def is_leader(self):
        return self.is_leader()

    def has_quorum(self):
        return self.hasQuorum
    
    def is_connected_to_others(self):
        for node in self.otherNodes:
            if not self.isNodeConnected(node):
                return False
        return True
    
    def status(self):
        return self.getStatus()

    @replicated
    def set(self, key, value, expire: float = None):
        try:
            return (self.__driver.set(key, value, expire), None)
        except Exception as e:
            return (False, str(e))

    @replicated
    def set_many(self, mapping, expire: float = None):
        try:
            self.__driver.set_many(mapping, expire)
            return (True, None)
        except Exception as e:
            return (False, str(e))


    def get(self, key):
        return self.__driver.get(key)

    @replicated
    def delete(self, key):
        try:
            self.__driver.delete(key)
            return (True, None)
        except Exception as e:
            return (False, str(e))
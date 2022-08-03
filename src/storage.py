import os
import threading
import pickle
import zipfile

from diskcache import Cache


class KvDriver(object):

	def __init__(self, db_path: str):
		self._db_path = db_path

		self.__conn: Cache = Cache(directory=self._db_path, timeout=os.environ.get('KV_TIMEOUT', 10))
		self.__lock = threading.RLock()

	def serialize(self, fileName, raftData):
		raftData = pickle.dumps(raftData)
		with self.__lock:
			self.__conn.close()
			try:
				with zipfile.ZipFile(fileName, 'w', zipfile.ZIP_DEFLATED) as f:
					f.writestr(f"raft.bin", raftData)
					f.write(f"{self._db_path}/cache.db", 'kv.bin')
			except:
				raise

	def deserialize(self, fileName):
		with self.__lock:
			self.__conn.close()
			with zipfile.ZipFile(fileName, 'r') as archiveFile:
				raftData = pickle.loads(archiveFile.read("raft.bin"))
				with open(f"{self._db_path}/cache.db", 'wb') as sqlDstFile:
					with archiveFile.open('kv.bin', 'r') as src_file:
						while True:
							data = src_file.read(2 ** 21)
							if not data:
								break
							sqlDstFile.write(data)
				return raftData

	def set(self, key, value):
		with self.__lock:
			self.__conn[key] = value

	def set_many(self, mapping):
		with self.__conn.transact():
			for key, value in mapping.items():
				self.__conn[key] = value

	def get(self, key):
		with self.__lock:
			return self.__conn.get(key)

	def delete(self, key):
		with self.__lock:
			del self.__conn[key]
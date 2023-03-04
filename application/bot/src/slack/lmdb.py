import lmdb


class LMDB:
    def __init__(self, db_name):
        # Set db to 50MB
        self.env = lmdb.open(db_name, map_size=50000000)

    def put(self, key, value):
        with self.env.begin(write=True) as txn:
            try:
                txn.put(key.encode('utf-8'), value.encode('utf-8'))
            except lmdb.MapFullError:
                print("Database is full and cannot write to it.")

    def get(self, key):
        with self.env.begin() as txn:
            value = txn.get(key.encode('utf-8'))
            if value is not None:
                value = value.decode('utf-8')
        return value

    def delete(self, key):
        with self.env.begin(write=True) as txn:
            try:
                txn.delete(key.encode('utf-8'))
            except lmdb.NotFoundError:
                print(f"Key {key} not found in database. Key was not cached")

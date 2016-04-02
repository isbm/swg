import ZODB
import ZODB.FileStorage
import transaction
import BTrees.OOBTree


class Places(object):
    '''
    Database of the places.
    '''
    def __init__(self, dbfile):
        self._db = ZODB.DB(ZODB.FileStorage.FileStorage(dbfile))
        self._db_conn = self._db.open()
        self._root = self._db_conn.root()
        self._root['apartments'] = BTrees.OOBTree.OOBTree()
        self.apartments = self._root['apartments']

    def add_apartment(self, apartment):
        '''
        Add an apartment to the object database.

        :param apartment:
        :return:
        '''
        if apartment.hash() not in self.apartments:
            self.apartments[apartment.hash()] = apartment
        return self.apartments[apartment.hash()]

    def list_apartments(self):
        return self.apartments.values()

    def commit(self):
        transaction.commit()
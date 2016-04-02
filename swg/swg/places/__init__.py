import ZODB
import ZODB.FileStorage
import transaction
import BTrees.OOBTree


def make_connection(dbfile):
    return ZODB.DB(ZODB.FileStorage.FileStorage(dbfile)).open()


class Places(object):
    '''
    Database of the places.
    '''
    def __init__(self, connection=None):
        self._db_conn = connection is None and make_connection() or connection
        self._root = self._db_conn.root()
        if 'apartments' not in self._root:
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
        return self

    def list_apartments(self):
        return self.apartments.values()

    def commit(self):
        transaction.commit()

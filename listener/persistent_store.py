import sqlite3
import json


class PersistentStore:
    def __init__(self, db_name):
        self._db = sqlite3.connect(db_name)
        self._cursor = self._db.cursor()
        self._database_check_required = False

    def get_paths(self, tracked_files_db, client):
        paths = list(self._cursor.execute('select paths from {} where ip={}'
                                          .format(tracked_files_db, client)))
        if len(paths) == 1:
            try:
                paths = json.loads(paths[0][0])['paths']
            except ValueError:
                print 'Error. See if the "paths" in database is using '\
                  'double-quotes in JSON. This is a possible reason for error'

        return paths

    def drop_table(self, table_name):
        self._cursor.execute('drop table {};'.format(table_name))

    def set_paths(self, paths, tracked_files_db, client):
        self._drop_table(tracked_files_db)
        self._cursor.execute('create table {} (ip TEXT, paths TEXT);'
                             .format(tracked_files_db))
        paths = json.dumps({"paths": paths})
        self._cursor.execute('insert into {} values ({}, {});'
                             .format(tracked_files_db, client, paths))
        

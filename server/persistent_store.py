import sqlite3
import json


class PersistentStore:
    def __init__(self, db_name):
        self._db = sqlite3.connect(db_name)
        self._cursor = self._db.cursor()
        self._database_check_required = False

    def get_paths(self, tracked_files_table, client):
        paths = list(self._cursor.execute('select paths from {} where ip="{}"'
                                          .format(tracked_files_table, client)))
        if len(paths) == 1:
            try:
                paths = json.loads(paths[0][0])['paths']
            except ValueError:
                print 'Error. See if the "paths" in database is using '\
                  'double-quotes in JSON. This is a possible reason for error'

        return paths

    def get_clients_and_usernames(self, client_table):
        clients_and_usernames = list(self._cursor.execute("select ip, username"\
                                                          " from {};"
                                                          .format(client_table)))
        return clients_and_usernames

    def set_paths(self, tracked_files_table, client, paths):
        self._drop_table(tracked_files_table)
        self._cursor.execute('create table {} (ip TEXT, paths TEXT);'
                             .format(tracked_files_table))
        self._db.commit()
        paths = json.dumps({"paths": paths})
        self._insert(tracked_files_table, client, paths)

    def set_client_and_username(self, client_table, client_ip, username):
        """
        Accept tuples of format; (client_ip, username)
        """
        self._drop_table(client_table)
        self._cursor.execute('create table {} (ip TEXT, username TEXT);'
                             .format(client_table))
        self._insert(client_table, client_ip, username)

    # Private methods used inside the class
    def _drop_table(self, table_name):
        self._cursor.execute('drop table {};'.format(table_name))
        self._db.commit()

    def _quote_string(self, string):
        return "'{}'".format(string)

    def _insert(self, table_name, *values):
        if values:
            # Make string of format 'value1,value2,value3'
            values = [self._quote_string(value) for value in values]

            query = 'insert into {} values('.format(table_name)
            for value in values:
                query += value + ','
            query = (query[:-1] if query[-1] == ',' else query) + ');'
            
            self._cursor.execute(query)
            self._db.commit()


def set_critical_settings(file_name, **kwargs):
    output = ""
    for key, value in kwargs.items():
        output += "{}={}\n".format(key, value)
    with open(file_name, 'w') as f:
        f.write(output)


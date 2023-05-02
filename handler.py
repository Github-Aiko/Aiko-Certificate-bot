import pymysql
import re
import pandas as pd
from dbutils.pooled_db import PooledDB
import bot
db_cfg = bot.config['cert_bot']['database']

class MysqlUtils(object):
    def __init__(self, ip: str = None, port: int = None, db=None, user=None, password=None):
        self.__mysql_ip = db_cfg['ip'] if ip is None else ip
        self.__mysql_port = bot.port if port is None else port
        self.__mysql_db = db_cfg['name'] if db is None else db
        self.__username = db_cfg['user'] if user is None else user
        self.__password = db_cfg['pass'] if password is None else password
        self.conn = None
        self.cur = None
        try:
            self.conn = PooledDB(pymysql, maxcached=50, host=self.__mysql_ip, port=self.__mysql_port,
                                 user=self.__username,
                                 password=self.__password, db=self.__mysql_db).connection()
            if self.conn:
                self.cur = self.conn.cursor()
                print("Database: {} is connected successfully!".format(
                    self.__mysql_db))
            else:
                print("Database: {} is not connected, please try it again!".format(
                    self.__mysql_db))
        except Exception as e:
            print('Connection Error: ', e)

    def cursor(self):
        return self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()
            print('Connection has been closed!')
        else:
            print('Error: can not close the connection which is None Type !')

    def execute_sql(self, sql=' '):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            error = 'MySQL execute failed! ERROR (%s): %s' % (
                e.args[0], e.args[1])
            print(error)
            return error

    def is_exist_table(self, table_name):
        sql = "SELECT COUNT(*) From {}".format(table_name)
        result = self.execute_sql(sql)
        if result is None:
            return True
        else:
            if re.search("doesn't exist", result):
                return False
            else:
                return True

    def create_table(self, tablename, attrdict, constraint):
        if self.is_exist_table(tablename):
            print('Error: can not create {} which exists in {}! '.format(
                tablename, self.__mysql_db))
            return
        sql = ''
        sql_mid = '`id` bigint(11) NOT NULL AUTO_INCREMENT,'
        for attr, value in attrdict.items():
            sql_mid = sql_mid + '`' + attr + '`' + ' ' + value + ','
        sql = sql + 'CREATE TABLE IF NOT EXISTS %s (' % tablename
        sql = sql + sql_mid
        sql = sql + constraint
        sql = sql + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'
        # ENGINE=InnoDB/MyISAM, InnoDB is recommended.
        print('creatTable:' + sql)
        self.execute_sql(sql)

    @property
    def get_version(self):
        self.cur.execute("SELECT VERSION()")
        return self.fetch_one_data()[0]

    def fetch_one_data(self):
        data = self.cur.fetchone()
        return data

    def insert_one(self, table_name, params):
        key = []
        value = []
        for tmp_key, tmp_value in params.items():
            key.append(tmp_key)
            if isinstance(tmp_value, str):
                value.append("\'" + tmp_value + "\'")
            else:
                value.append(tmp_value)
        attrs_sql = '(' + ','.join(key) + ')'
        values_sql = ' values(' + ','.join(value) + ')'
        sql = 'insert into %s' % table_name
        sql = sql + attrs_sql + values_sql
        print('Insert One:' + sql)
        self.execute_sql(sql)

    def update_one(self, table_name: str, params: dict, conditions: dict):
        update_sql = [k + '=' + "\'" +
                      str(v) + "\'" for k, v in params.items()]
        print(update_sql)
        if conditions:
            conditions_sql = [k + '=' + "\'" +
                              str(v) + "\'" for k, v in conditions.items()]
            sql = 'update ' + table_name + ' set ' + \
                ','.join(update_sql) + ' where ' + ','.join(conditions_sql)
        else:
            sql = 'update ' + table_name + ' set ' + ','.join(update_sql)
        print('Update One:', sql)
        self.execute_sql(sql)

    def insert_many(self, table: str, attrs: list, values: list):
        values_sql = ['%s' for v in attrs]
        attrs_sql = '(' + ','.join(attrs) + ')'
        values_sql = ' values(' + ','.join(values_sql) + ')'
        sql = 'insert into %s' % table
        sql = sql + attrs_sql + values_sql
        print('insertMany:' + sql)
        try:
            for i in range(0, len(values), 20000):
                self.cur.executemany(sql, values[i:i + 20000])
                self.conn.commit()
        except pymysql.Error as e:
            self.conn.rollback()
            error = 'insertMany executemany failed! ERROR (%s): %s' % (
                e.args[0], e.args[1])
            print(error)

    def count_sql_query(self, sql_table, sql_condition=''):
        sql = "SELECT count(*) FROM " + sql_table + ' ' + sql_condition
        print(sql)
        self.cur.execute(sql)
        return list(self.cur.fetchall())[0][0]

    def sql_query(self, sql, df_header: list = None):
        print(sql)
        self.cur.execute(sql)
        if not df_header:
            return self.cur.fetchall()
        else:
            result = self.cur.fetchall()
            df = pd.DataFrame(list(result), columns=df_header)
            return df

    def truncate_table(self, sql_table):
        sql = "TRUNCATE table " + sql_table
        print(sql)
        self.cur.execute(sql)
        self.conn.commit()

    def delete_table(self, table, conditions=''):
        sql = "DELETE FROM " + table + ' ' + conditions
        print("sql=", sql)
        self.cur.execute(sql)
        self.conn.commit()

    def drop_table(self, table, flag=False):
        if flag:
            sql = "DROP TABLE " + table
            print("Warning: " + sql)
            self.cur.execute(sql)
            self.conn.commit()

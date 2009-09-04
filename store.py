# Copyright (c) WisdomTap Solutions (I) Pvt Ltd. All rights reserved.
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import MySQLdb

class Store:
    def __init__(self, user, passwd, db, host = 'localhost'):
        self.params = [user, passwd, db, host]
        self.no_cache_conn = False
        self.in_trans = False
        self.log = False
        self.log_only = False
        self.conn = None
        
    def get_conn(self):
        if self.conn:
            return self.conn
        
        return self.__get_conn()
    
    def __get_conn(self):
        if self.no_cache_conn:
            self.close()
        if not self.conn:
            self.conn = MySQLdb.connect(user = self.params[0],
                                        passwd = self.params[1],
                                        db = self.params[2],
                                        host = self.params[3],
                                        charset = 'utf8',
                                        use_unicode = True)
            
        return self.conn

    def close(self):
        '''close the connection, if open'''
        if self.conn:
            self.conn.close()
            self.conn = None
            
    def execute(self, stmt, params = None):
        if self.log or self.log_only:
            print stmt
        if self.log_only:
            return 0
        
        if not self.in_trans:
            self.conn = self.__get_conn()
        
        c = self.conn.cursor()
        if params:
            c.execute(stmt, params)
        else:
            c.execute(stmt)
        last = c.lastrowid
        c.close()
        if not self.in_trans:
            self.conn.commit()
        return last
        
    def select(self, stmt, params = None):
        if self.log or self.log_only:
            print stmt
        if self.log_only:
            return 0
        if not self.in_trans:
            self.conn = self.__get_conn()
        
        c = self.conn.cursor()
        if params:
            c.execute(stmt, params)
        else:
            c.execute(stmt)
        rs = c.fetchall()
        if rs and len(rs[0]) == 1:
            rs = [x[0] for x in rs]
        c.close()
        return rs
    
    def begin(self):
        if self.log or self.log_only:
            print "BEGIN TRANSACTION"
        if self.log_only: return 0
        if self.in_trans:
            self.conn.rollback()
            self.close()
            
        self.conn = self.__get_conn()
        self.conn.autocommit(False)
        self.in_trans = True

    def end(self, commit = True):
        if self.log or self.log_only:
            print "END TRANSACTION"
        if self.log_only: return 0
        if not self.in_trans:
            return
        if commit:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.close()
        self.in_trans = False

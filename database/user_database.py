import sqlite3
import json

import sys
sys.path.insert(1, 'C:\\Users\\user\\Desktop\\mstr_bot\\git\\mstr-chat-bot')

from log.create_loggers import database_logger


class DB:
    """
    # Можно выполнять кастомные запросы через cursor.execute
    a.cursor.execute(
            '''
            select * from users
            '''
        )
    print(a.cursor.fetchall())
    """
    
    '''a={
            'Idотчета1':{
                        'selector1':['значениеселектора', 'значениеселектора'],
                        'selector2':['значениеселектора']
                        },
            'id_отчета2':{
                        'sel4': ['знач1'],
                        'sel5': ['знач2', 'знач5', 'знач6']
                        }
    }'''

    def __init__(self, path: str):
        self.connect = sqlite3.connect(path)
        self.connect.row_factory = sqlite3.Row
        self.cursor = self.connect.cursor()
        database_logger.info(f'Create connection to database: {path}')

    def insert_new_user(self, user_id: int):
        users = self.get_users()
        if user_id in users:
            return
        try:
            self.cursor.execute(
                '''
                SELECT name from sqlite_master where type= "table"
                '''
            )
            tables = self.cursor.fetchall()
            for i in tables:
                self.cursor.execute(
                    f'''
                    insert into {i['name']} (ID) values (:user_id);
                    ''',
                    {"user_id": user_id}
                )
        except sqlite3.DatabaseError as err:
            database_logger.exception(f'\tuser_ID:{user_id}')
        else:
            self.connect.commit()

    def get_users(self):
        try:
            self.cursor.execute(
                '''
                select ID from users
                '''
            )
        except sqlite3.DatabaseError as err:
            database_logger.exception('')
        else:
            users_list = []
            for row in self.cursor.fetchall():
                users_list.append(row[0])
            return users_list

    def get_triggers(self):
        try:
            self.cursor.execute(
                '''
                select distinct trigger_name from trigger_scheduler
                '''
            )
        except sqlite3.DatabaseError as err:
            database_logger.exception('')
        else:
            triggers_list = []
            for row in self.cursor.fetchall():
                triggers_list.append(row[0])
            return triggers_list

    def get_user_triggers(self, user_id):
        try:
            self.cursor.execute(
                '''
                select ID, document_name from trigger_scheduler where user_id == (:user_id)
                ''',
                {"user_id": user_id}
            )
        except sqlite3.DatabaseError as err:
            database_logger.exception('')
        else:
            documents_list = {}
            for row in self.cursor.fetchall():
                documents_list[row[0]] = row[1]
            return documents_list

    def get_truggers_by_id(self, ID):
        try:
            self.cursor.execute(
                '''
                select * from trigger_scheduler where ID == (:ID)
                ''',
                {"ID": ID}
            )
        except sqlite3.DatabaseError as err:
            database_logger.exception('')
        else:
            return self.cursor.fetchone()

    def insert_trigger_scheduler(self, trigger_name, user_id, document_id, document_filters, document_name):
        try:
            document_filters = json.dumps(document_filters)

            self.cursor.execute(
                    '''
                    insert into trigger_scheduler (trigger_name, user_id, document_id, document_filters, document_name)  values (:trigger_name, :user_id, :document_id, :document_filters, :document_name);
                    ''',
                    {"trigger_name": trigger_name, "user_id": user_id, "document_id": document_id, "document_filters": document_filters, "document_name": document_name}
                )
        except sqlite3.DatabaseError as err:
            database_logger.exception('')
        else:
            self.connect.commit()

    def delete_trigger_scheduler(self, trigger_id):
        try:
            self.cursor.execute(
                    '''
                    delete from trigger_scheduler where ID = (:ID);
                    ''',
                    {"ID": trigger_id}
                )
        except sqlite3.DatabaseError as err:
            database_logger.exception('')
        else:
            self.connect.commit()
# tmp = self.cursor.fetchone()[0]
#             return None if tmp == None else json.loads(tmp)

    def insert_security(self, user_id: int, security: str):
        try:
            self.cursor.execute(
                '''
                UPDATE users SET security = :security WHERE ID = :user_id
                ''',
                {"user_id": user_id, "security": security}
            )
        except sqlite3.DatabaseError as err:
            database_logger.exception(f'\tuser_ID:{user_id}')
        else:
            self.connect.commit()

    def insert_favorite(self, user_id: int, favorite: dict):
        try:
            favorite = json.dumps(favorite)
            self.cursor.execute(
                '''
                UPDATE favorite SET favorite = :favorite WHERE ID = :user_id
                ''',
                {"user_id": user_id, "favorite": favorite}
            )
        except sqlite3.DatabaseError as err:
            database_logger.exception(f'\tuser_ID:{user_id}')
        else:
            self.connect.commit()

    def insert_subscription(self, user_id: int, subscription: dict):
        try:
            self.cursor.execute(
                '''
                select * from subscription LIMIT 1
                '''
            )
            z = self.cursor.fetchone()
            for i in z.keys()[1:]:
                self.cursor.execute(
                    f'''
                    UPDATE subscription SET {i} = :subs WHERE ID = :user_id;
                    ''',
                    {"user_id": user_id, "subs": subscription.get(i, None)}
                )
        except sqlite3.DatabaseError as err:
            database_logger.exception(f'\tuser_ID:{user_id}')
        else:
            self.connect.commit()

    def insert_language(self, user_id: int, language: str):
        try:
            self.cursor.execute(
                '''
                UPDATE users SET language = :language WHERE ID = :user_id
                ''',
                {"user_id": user_id, "language": language}
            )
        except sqlite3.DatabaseError as err:
            database_logger.exception(f'\tuser_ID:{user_id}')
        else:
            self.connect.commit()

    def concat_security(self, user_id: int, security: str):
        try:
            self.cursor.execute(
                '''
                select security from users WHERE ID = :user_id
                ''',
                {"user_id": user_id}
            )
            tmp = self.cursor.fetchall()[0][0]
            if (tmp == None or tmp == 'null'):
                tmp = security
            else:
                tmp = f'{tmp};{security}'

            self.cursor.execute(
                '''
                UPDATE users SET security = :security WHERE ID = :user_id
                ''',
                {"user_id": user_id, "security": f"{tmp}"}
            )
        except sqlite3.DatabaseError as err:
            database_logger.exception(f'\tuser_ID:{user_id}')
        else:
            self.connect.commit()

    def concat_favorite(self, user_id: int, favorite: dict):
        try:
            self.cursor.execute(
                '''
                select favorite from favorite WHERE ID = :user_id
                ''',
                {"user_id": user_id}
            )
            tmp = self.cursor.fetchall()[0][0]
            if (tmp == None or tmp == 'null'):
                tmp = favorite
            else:
                cur_favorite = json.loads(tmp)
                tmp = {**cur_favorite, **favorite}

            tmp = json.dumps(tmp)

            self.cursor.execute(
                '''
                UPDATE favorite SET favorite = :favorite WHERE ID = :user_id
                ''',
                {"user_id": user_id, "favorite": f"{tmp}"}
            )
        except sqlite3.DatabaseError as err:
            database_logger.exception(f'\tuser_ID:{user_id}')
        else:
            self.connect.commit()

    def concat_subscription(self, user_id: int, subscription: dict):
        try:
            self.cursor.execute(
                '''
                select * from subscription LIMIT 1
                '''
            )
            z = self.cursor.fetchone()
            for i in z.keys()[1:]:
                self.cursor.execute(
                    f'''
                    select {i} from subscription WHERE ID = :user_id
                    ''',
                    {"user_id": user_id}
                )
                tmp = self.cursor.fetchone()[0]
                self.cursor.execute(
                    f'''
                    UPDATE subscription SET {i} = :subs WHERE ID = :user_id;
                    ''',
                    {"user_id": user_id, "subs": f'{tmp};{subscription.get(i, None)}'}
                )
        except sqlite3.DatabaseError as err:
            database_logger.exception(f'\tuser_ID:{user_id}')
        else:
            self.connect.commit()

    def get_security(self, user_id: int):
        try:
            self.cursor.execute(
                '''
                select security from users WHERE ID = :user_id
                ''',
                {"user_id": user_id}
            )
        except sqlite3.DatabaseError as err:
            database_logger.exception(f'\tuser_ID:{user_id}')
        else:
            
            z = self.cursor.fetchone()[0]
            if z:
                return z.split(';')
            else:
                return z

    def get_favorite(self, user_id: int):
        try:
            self.cursor.execute(
                '''
                select favorite from favorite WHERE ID = :user_id
                ''',
                {"user_id": user_id}
            )
        except sqlite3.DatabaseError as err:
            database_logger.exception(f'\tuser_ID:{user_id}')
        else:
            tmp = self.cursor.fetchone()[0]
            return None if tmp == None else json.loads(tmp)

    def get_subscription(self, user_id: int):
        try:
            self.cursor.execute(
                '''
                select indicator_change, company_events, time_events from subscription WHERE ID = :user_id;
                ''',
                {"user_id": user_id}
            )
        except sqlite3.DatabaseError as err:
            database_logger.exception(f'\tuser_ID:{user_id}')
        else:
            return self.cursor.fetchone()

    def get_language(self, user_id: int):
        if user_id not in self.get_users():
            return None
        try:
            self.cursor.execute(
                '''
                select language from users WHERE ID = :user_id
                ''',
                {"user_id": user_id}
            )
        except sqlite3.DatabaseError as err:
            database_logger.exception(f'\tuser_ID:{user_id}')
        else:
            z = self.cursor.fetchone()[0]
            return z

    def delete_favorite(self, user_id: int, documentID: str):
        try:
            self.cursor.execute(
                '''
                select favorite from favorite WHERE ID = :user_id
                ''',
                {"user_id": user_id}
            )
            tmp = self.cursor.fetchall()[0][0]
            cur_favorite = json.loads(tmp)
            cur_favorite.pop(documentID, None)
            tmp = json.dumps(cur_favorite)

            self.cursor.execute(
                '''
                UPDATE favorite SET favorite = :favorite WHERE ID = :user_id
                ''',
                {"user_id": user_id, "favorite": f"{tmp}"}
            )
        except sqlite3.DatabaseError as err:
            database_logger.exception(f'\tuser_ID:{user_id}')
        else:
            self.connect.commit()

    """
    def get_all (self):
        try:
            self.cursor.executescript(
                '''
                select * from users;
                select * from subscription;
                select * from favorite;
                '''
            )   
        except sqlite3.DatabaseError as err:
            database_logger.exception(f'\tuser_ID:{user_id}')
        else: 
            return self.cursor.fetchall()
    """

    def drop_user(self, user_id: int):
        users = self.get_users()
        if user_id not in users:
            return
        self.cursor.execute(
            '''
            SELECT name from sqlite_master where type= "table"
            '''
        )
        tables = self.cursor.fetchall()
        try:
            for i in tables:
                self.cursor.execute(
                    f'''
                    delete from {i[0]} where ID = :user_id;
                    ''',
                    {"user_id": user_id}
                )
        except sqlite3.DatabaseError as err:
            database_logger.exception(f'\tuser_ID:{user_id}')
        else:
            self.connect.commit()

    def drop_all_users(self):
        self.cursor.execute(
            '''
            SELECT name from sqlite_master where type= "table"
            '''
        )
        tables = self.cursor.fetchall()
        try:
            for i in tables:
                self.cursor.execute(
                    f'''
                    delete from {i['name']};
                    '''
                )
        except sqlite3.DatabaseError as err:
            database_logger.exception('')
        else:
            self.connect.commit()

    def show_all(self):
        self.cursor.execute(
            '''
            SELECT name from sqlite_master where type= "table"
            '''
        )
        tables = self.cursor.fetchall()
        try:
            for i in tables:
                print(i['name'])
                SQL = f'''
                    select * from {i['name']}
                    '''
                self.cursor.execute(SQL)
                tmp = self.cursor.fetchall()
                for i in tmp:
                    for j in i:
                        print(j, end='\t')
                    print()
                print('\n')
        except sqlite3.DatabaseError as err:
            database_logger.exception('')

    def __del__(self):
        self.cursor.close()
        self.connect.close()





if __name__ == '__main__':
    a = DB('database/bot_database.sqlite')
    # a.insert_new_user(449977514)
    # a.drop_user(449977514)
    # a.get_security(1723464345)
    # a.insert_security(1723464345, 'null')
    # a.concat_security(1723464345, 'ACADEMY DINOSAUR;ACE GOLDFINGER')

    # a.cursor.execute(
    #         '''
    #         drop table trigger_scheduler
    #         '''
    #     )
    # a.connect.commit()


    # a.cursor.execute(
    #         '''
    #         CREATE TABLE trigger_scheduler
    #            (
    #             ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    #             trigger_name TEXT,
    #             date_trigger DATETIME,
    #             date_last_update DATETIME,
    #             user_id INTEGER,
    #             document_id TEXT,
    #             document_filters TEXT,
    #             document_name TEXT)
    #         '''
    #     )
    # a.connect.commit()

    a.cursor.execute(
            '''
            INSERT INTO trigger_scheduler (trigger_name) VALUES ('trigger_5');
            '''
        )
    a.connect.commit()
    print(a.get_user_triggers(1723464345))
    print(1)

# a = DB('database/bot_database.sqlite')

# a.cursor.executescript(
#                 '''
#                 ALTER TABLE users
#                 ADD language VARCHAR(2) DEFAULT 'ru';
#                 '''
#             )   

# a.show_all()

#a.drop_all_users()
#a.insert_new_user(1)
# a.concat_security(1, 'q')
# a.concat_security(1, 'w')
# a.concat_security(1, 'e')
# import time

# start = time.time()
# for i in range(10000):
#     z = a.get_users()

# print(time.time()-start)

# print(z)
# a.insert_security(1723464345, None)
# a.concat_security(1723464345, 'ACADEMY DINOSAUR;ACE GOLDFINGER')
# print(a.get_security(1723464345))
# a.show_all()

# a.show_all()

"""
import random
import time
def test():
    a.drop_all_users()
    print('drop_all_user')


    for i in range(100):
        b=random.randint(1,1111111111)
        a.insert_new_user(b)
        #print('insert_new_user')
        a.insert_security(b, 'sec_'+str(b))
        a.insert_favorite(b, 'fav'+str(b))
        a.insert_subscription(b, {"indicator_change": 'ind'+str(b), "company_events": 'comp'+str(b), "time_events": "time"+str(b)})
        #a.show_all() 
        a.concat_favorite(b,'NEW')
        a.concat_security(b,'NEW')
        a.concat_subscription(b,{"indicator_change": 'NEW', "company_events": 'NEW', "time_events": 'NEW'})
        #print(a.get_users()[0][0])
        #print(a.get_security(b)[0])
        #a.show_all() 
    #a.show_all() 
    a.drop_user(b)
    #a.show_all() 
    a.drop_all_users()
    #a.show_all() 



a = DB('database/bot_database.sqlite')

a.drop_all_users()
start = time.time()
test()
print(time.time()-start)
exit()
a.insert_new_user(1)
a.insert_security(1,"first")
print(a.get_security(1))
a.concat_security(1,"second")
z=a.get_security(1)
print(z)
z=z[0][0].split(';')
print(z)
exit()
start = time.time()
a.cursor.execute(
        '''
        select * from subscription
        '''
    )   
p=a.cursor.fetchall()
'''
print(p)
print(p[0])
print(p[0][1])
print(a.get_users())
z=a.get_subscription(1723464345)
print(a.get_favorite(1723464345))
print(a.get_security(1723464345))
print(a.get_subscription(1723464345))
print(time.time()-start)
'''
"""
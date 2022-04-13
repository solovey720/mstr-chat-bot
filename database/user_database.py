
import sqlite3 
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

    def __init__(self, path: str):
        self.connect = sqlite3.connect(path)
        self.connect.row_factory = sqlite3.Row
        self.cursor = self.connect.cursor()

    def insert_new_user(self, user_id: int):
        users = self.get_users()
        if (user_id,) in users: 
            return
        self.cursor.execute(
                '''
                SELECT name from sqlite_master where type= "table"
                '''
            ) 
        tables=self.cursor.fetchall()
        try:
            for i in tables:
                self.cursor.execute(
                    f'''
                    insert into {i['name']} (ID) values (:user_id);
                    ''', 
                    {"user_id": user_id}
                )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
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
            print("Error: ", err)
        else: 
            return self.cursor.fetchall()

    def insert_security (self, user_id: int, security: str):
        try:
            self.cursor.execute(
                '''
                UPDATE users SET security = :security WHERE ID = :user_id
                ''', 
                {"user_id": user_id, "security": security}
            )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            self.connect.commit()

    def insert_favorite (self, user_id: int, favorite: str):
        try:
            self.cursor.execute(
                '''
                UPDATE favorite SET favorite = :favorite WHERE ID = :user_id
                ''', 
                {"user_id": user_id, "favorite": favorite}
            )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            self.connect.commit()

    def insert_subscription (self, user_id: int, subscription: dict):
        try:
            self.cursor.execute(
                '''
                select * from subscription LIMIT 1
                '''
            )   
            z=a.cursor.fetchone()
            for i in z.keys()[1:]:
                self.cursor.execute(
                    f'''
                    UPDATE subscription SET {i} = :subs WHERE ID = :user_id;
                    ''', 
                    {"user_id": user_id, "subs": subscription.get(i, None)}
                )  
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            self.connect.commit()
        
    def concat_security (self, user_id: int, security: str):
        try:
            self.cursor.execute(
                '''
                select security from users WHERE ID = :user_id
                ''', 
                {"user_id": user_id}
            )   
            tmp = self.cursor.fetchall()[0][0]

            self.cursor.execute(
                '''
                UPDATE users SET security = :security WHERE ID = :user_id
                ''', 
                {"user_id": user_id, "security": f"{tmp};{security}"}
            )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            self.connect.commit()
    
    def concat_favorite (self, user_id: int, favorite: str):
        try:
            self.cursor.execute(
                '''
                select favorite from favorite WHERE ID = :user_id
                ''', 
                {"user_id": user_id}
            )   
            tmp = self.cursor.fetchall()[0][0]

            self.cursor.execute(
                '''
                UPDATE favorite SET favorite = :favorite WHERE ID = :user_id
                ''', 
                {"user_id": user_id, "favorite": f"{tmp};{favorite}"}
            )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            self.connect.commit()

    def concat_subscription (self, user_id: int, subscription: dict):
        try:
            self.cursor.execute(
                '''
                select * from subscription LIMIT 1
                '''
            )   
            z=a.cursor.fetchone()
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
            print("Error: ", err)
        else: 
            self.connect.commit()

    def get_security (self, user_id: int):
        try:
            self.cursor.execute(
                '''
                select security from users WHERE ID = :user_id
                ''', 
                {"user_id": user_id}
            )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            return self.cursor.fetchone()

    def get_favorite (self, user_id: int):
        try:
            self.cursor.execute(
                '''
                select favorite from favorite WHERE ID = :user_id
                ''', 
                {"user_id": user_id}
            )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            return self.cursor.fetchone()

    def get_subscription (self, user_id: int):
        try:
            self.cursor.execute(
                '''
                select indicator_change, company_events, time_events from subscription WHERE ID = :user_id;
                ''', 
                {"user_id": user_id}
            )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            return self.cursor.fetchone()

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
            print("Error: ", err)
        else: 
            return self.cursor.fetchall()
    """

    def drop_user (self, user_id: int):
        users = self.get_users()
        if (user_id,) not in users: 
            return
        self.cursor.execute(
                '''
                SELECT name from sqlite_master where type= "table"
                '''
            ) 
        tables=self.cursor.fetchall()
        try:
            for i in tables:
                self.cursor.execute(
                    f'''
                    delete from {i} where ID = :user_id;
                    ''', 
                    {"user_id": user_id}
                )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else:
            self.connect.commit()
    
    def drop_all_users(self):
        self.cursor.execute(
            '''
            SELECT name from sqlite_master where type= "table"
            '''
        ) 
        tables=self.cursor.fetchall()
        try:
            for i in tables:
                self.cursor.execute(
                    f'''
                    delete from {i['name']};
                    '''
                )   
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
        else: 
            self.connect.commit()

    def show_all(self):
        self.cursor.execute(
                '''
                SELECT name from sqlite_master where type= "table"
                '''
            ) 
        tables=self.cursor.fetchall()
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
                        print (j, end='\t')
                    print()        
                print('\n')
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)

    def __del__(self):
        self.cursor.close()
        self.connect.close()
        
"""
a = DB('database/bot_database.sqlite')

a.drop_all_users()
a.insert_new_user(1)
a.insert_favorite(1," sdf")
print(a.get_favorite(1)[0])
a.show_all()
"""
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
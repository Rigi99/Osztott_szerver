import mysql.connector
from mysql.connector import Error
from secrets import token_hex


def insertIntoUserDb(nev, nem, vote):
    global connection, cursor
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='personal_data',
                                             user='root',
                                             password='')
        if connection.is_connected():
            cursor = connection.cursor()

            token = token_hex(16)

            mySql_insert_query = """INSERT INTO user_datas (name, gen, token) 
                                      VALUES  (%s, %s, %s) """

            record = (nev, nem, token)
            cursor.execute(mySql_insert_query, record)
            connection.commit()

            sql_select_query = "select * from user_datas where token=token"
            cursor.execute(sql_select_query)
            records = cursor.fetchall()
            if len(records) > 0:
                insertIntoVoteDb(token, vote)
            else:
                raise Exception("Failed to save user data")


    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def insertIntoVoteDb(token, vote):
    global connection, cursor
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='vote',
                                             user='root',
                                             password='')
        if connection.is_connected():
            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO vote (user_token, vote) 
                                      VALUES  (%s, %s) """

            record = (token, vote)
            cursor.execute(mySql_insert_query, record)
            connection.commit()


    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def getVotesByCategory():
    global connection, cursor
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='vote',
                                             user='root',
                                             password='')
        if connection.is_connected():
            cursor = connection.cursor()

            sql_select_query = "select vote, count(*) from vote group by vote"
            cursor.execute(sql_select_query)
            categories = cursor.fetchall()
            votes = "<h3> Szavazatok szama: </h3>";
            for category in categories:
                votes = votes + "<h5>" + category[0] + ":" + str(category[1]) + "</h5><br>"
            print(votes)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

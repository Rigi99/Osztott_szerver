import mysql.connector
from mysql.connector import Error
from secrets import token_hex


def insertIntoUserDb(nev, nem, email, vote):
    global connection, cursor
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='oszt_rendszerek',
                                             user='root',
                                             password='')
        if connection.is_connected():
            cursor = connection.cursor()

            sql_select_query = "select * from user_datas where email = %s"
            cursor.execute(sql_select_query, (email,))
            userExists = cursor.fetchall()
            print(userExists)
            if len(userExists) == 0:
                token = token_hex(16)
                mySql_insert_query = """INSERT INTO user_datas (name, gen, email, token) 
                                          VALUES  (%s, %s, %s, %s) """

                record = (nev, nem, email, token)
                cursor.execute(mySql_insert_query, record)
                connection.commit()

                sql_select_query = "select * from user_datas where token=token"
                cursor.execute(sql_select_query)
                records = cursor.fetchall()
                if len(records) > 0:
                    insertIntoVoteDb(token, vote)
                else:
                    raise Exception("Failed to save user data")
            else:
                token = userExists[0][3]
                insertIntoVoteDb(token, vote)


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
                                             database='oszt_rendszerek',
                                             user='root',
                                             password='')
        if connection.is_connected():
            cursor = connection.cursor()

            sql_select_query = "select * from vote where user_token = %s"
            cursor.execute(sql_select_query, (token,))
            records = cursor.fetchall()
            if len(records) == 0:

                my_sql_insert_query = "INSERT INTO vote (user_token, vote) VALUES  (%s, %s) "

                record = (token, vote)
                cursor.execute(my_sql_insert_query, record)
                connection.commit()
            else:

                my_sql_update_query = "UPDATE vote SET vote = %s  where user_token = %s"
                record = (vote, token)

                cursor.execute(my_sql_update_query, record)
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
                                             database='oszt_rendszerek',
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
            return votes
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def getVotesByCategoryToServer():
    global connection, cursor
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='oszt_rendszerek',
                                             user='root',
                                             password='')
        if connection.is_connected():
            cursor = connection.cursor()

            sql_select_query = "select vote, count(*) from vote group by vote"
            cursor.execute(sql_select_query)
            categories = cursor.fetchall()
            str1 = ""
            for category in categories:
                str1 = str1 + category[0] + "|" + str(category[1]) + "#"
            return str1
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

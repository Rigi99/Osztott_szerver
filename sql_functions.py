import mysql.connector
from mysql.connector import Error
import pandas as pd
from IPython.display import HTML


def insert_into_table(nev, zavazat):
    global connection, cursor
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='osztott_rendszerek',
                                             user='root',
                                             password='')
        if connection.is_connected():
            sql_select_Query = "select * from szavazok"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            # get all records
            records = cursor.fetchall()
            id = cursor.rowcount + 1

            mySql_insert_query = """INSERT INTO szavazok (id, nev, szavazat) 
                                      VALUES  (%s, %s, %s) """

            record = (id, nev, zavazat)
            cursor.execute(mySql_insert_query, record)
            connection.commit()
            print("Record inserted successfully into szavazok table")

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def get_voters():
    global query_string, connection, cursor
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='osztott_rendszerek',
                                             user='root',
                                             password='')

        sql_select_Query = "select * from szavazok order by id asc"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        # get all records
        records = cursor.fetchall()
        print("Szavazok szama: ", cursor.rowcount)

        # print("\nSzavazok listaja")
        query_string = ""
        for row in records:
            query_string += row[1] + '|' + row[2] + '#'

    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")
            return query_string

        def get_voters():
            global query_string, connection, cursor
            try:
                connection = mysql.connector.connect(host='localhost',
                                                     database='osztott_rendszerek',
                                                     user='root',
                                                     password='')

                sql_select_Query = "select * from szavazok order by id asc"
                cursor = connection.cursor()
                cursor.execute(sql_select_Query)
                # get all records
                records = cursor.fetchall()
                print("Szavazok szama: ", cursor.rowcount)

                # print("\nSzavazok listaja")
                query_string = ""
                for row in records:
                    query_string += row[1] + '|' + row[2] + '#'

            except mysql.connector.Error as e:
                print("Error reading data from MySQL table", e)
            finally:
                if connection.is_connected():
                    connection.close()
                    cursor.close()
                    print("MySQL connection is closed")
                    return query_string

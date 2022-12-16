import pymysql
import os


class Nimbus_Attendees:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        ENDPOINT="nimbus-db.c4dwsoa8ic0w.us-east-1.rds.amazonaws.com"
        PORT="3306"
        HOST=os.environ.get("DBHOST")
        USER=os.environ.get("DBUSER")
        PW=os.environ.get("DBPW")
        REGION="us-east-1"
        DBNAME="nimbus-db"
        
        conn = pymysql.connect(
            db=ENDPOINT,
            user=USER,
            password=PW,
            host=HOST,
            port=PORT,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn


    @staticmethod
    def create_attendee(user):
        sql = "INSERT INTO USERS (first_name, last_name, email_address, birth_date, phone, gender) VALUES (%s,%s,%s,%s,%s,%s);"
        conn = Nimbus_Attendees._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, user.first_name, user.last_name, user.email_address, user.birth_date, user.phone, user.gender)
        result = cur.fetchone()
        return result


    @staticmethod
    def get_all_users():
        sql = "SELECT * FROM USERS;"
        conn = Nimbus_Attendees._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchone()
        return result


    @staticmethod
    def get_attendee_by_uid(uid):
        sql = "SELECT * FROM f22_databases.columbia_students WHERE guid=%s"
        conn = Nimbus_Attendees._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=uid)
        result = cur.fetchone()
        return result


    @staticmethod
    def update_attendee_by_uid(uid, user):
        sql = "UPDATE USERS SET first_name=%s, last_name=%s, email_address=%s, birth_date=%s, phone=%s, gender=%s WHERE guid=%s;"
        conn = Nimbus_Attendees._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, user.first_name, user.last_name, user.email_address, user.birth_date, user.phone, user.gender)
        result = cur.fetchone()
        return result


    @staticmethod
    def delete_attendee_by_uid(uid):
        sql = "DELETE FROM USERS WHERE guid=%s;"
        conn = Nimbus_Attendees._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=uid)
        result = cur.fetchone()
        return result
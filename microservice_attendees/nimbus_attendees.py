import pymysql
import os


class Nimbus_Attendees:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        ENDPOINT="nimbus-db.c4dwsoa8ic0w.us-east-1.rds.amazonaws.com"
        PORT="3306"
        # HOST=os.environ.get("DBHOST")
        # USER=os.environ.get("DBUSER")
        # PW=os.environ.get("DBPW")
        HOST=""
        USER="admin"
        PW="dbpassword"
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
    def create_attendee(attendee):
        sql = "INSERT INTO contact_info (first_name, last_name, email_address, birth_date, phone, gender) VALUES (%s,%s,%s,%s,%s,%s);"
        conn = Nimbus_Attendees._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, attendee.first_name, attendee.last_name, attendee.email_address, attendee.birth_date, attendee.phone, attendee.gender)
        result = cur.fetchone()
        return result


    @staticmethod
    def get_all_attendees():
        sql = "SELECT * FROM contact_info;"
        conn = Nimbus_Attendees._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchone()
        return result


    @staticmethod
    def get_attendee_by_uid(uid):
        sql = "SELECT * FROM contact_info WHERE guid=%s"
        conn = Nimbus_Attendees._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=uid)
        result = cur.fetchone()
        return result


    @staticmethod
    def update_attendee_by_uid(uid, attendee):
        sql = "UPDATE contact_info SET first_name=%s, last_name=%s, email_address=%s, birth_date=%s, phone=%s, gender=%s WHERE guid=%s;"
        conn = Nimbus_Attendees._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, attendee.first_name, attendee.last_name, attendee.email_address, attendee.birth_date, attendee.phone, attendee.gender, uid)
        result = cur.fetchone()
        return result


    @staticmethod
    def delete_attendee_by_uid(uid):
        sql = "DELETE FROM contact_info WHERE guid=%s;"
        conn = Nimbus_Attendees._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=uid)
        result = cur.fetchone()
        return result
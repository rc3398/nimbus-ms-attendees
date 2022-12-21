import pymysql
import os


class Nimbus_Attendees:

    def __init__(self):
        #self.cursor = self._get_connection().cursor()
        pass

    @staticmethod
    def _get_connection():

       #usr = os.environ.get("DBUSER")
       #pw = os.environ.get("DBPW")
       #h = os.environ.get("DBHOST")

        usr = 'admin' 
        pw = 'dbpassword'
        h = 'nimbus-db.c4dwsoa8ic0w.us-east-1.rds.amazonaws.com'
        
        conn = pymysql.connect(
            port=3306,
            user=usr,
            password=pw,
            host=h,
            database='attendee',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn



    @staticmethod
    def create_attendee(attendee):
        conn = Nimbus_Attendees._get_connection()
        cur = conn.cursor()
        attendee.gender = attendee.gender.name
        sql = "INSERT INTO contact_info (first_name, last_name, email_address, birth_date, phone, gender, attendee_id) VALUES (%s,%s,%s,%s,%s,%s,%s);"
        args = (attendee.first_name, attendee.last_name, attendee.email_address, attendee.birth_date, attendee.phone, attendee.gender, attendee.email_address)
        result = cur.execute(sql, args=args)
        #result = cur.fetchone()
        return result


    @staticmethod
    def get_all_attendees():
        sql = "SELECT * FROM contact_info;"
        conn = Nimbus_Attendees._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()
        return result


    @staticmethod
    def get_attendee_by_uid(uid):
        sql = "SELECT * FROM contact_info WHERE attendee_id=%s"
        conn = Nimbus_Attendees._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=uid)
        result = cur.fetchone()
        return result


    @staticmethod
    def update_attendee_by_uid(uid, attendee):
        sql = "UPDATE contact_info SET first_name=%s, last_name=%s, email_address=%s, birth_date=%s, phone=%s, gender=%s, attendee_id=% WHERE guid=%s;"
        conn = Nimbus_Attendees._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, attendee.first_name, attendee.last_name, attendee.email_address, attendee.birth_date, attendee.phone, attendee.gender, attendee.email_address, uid)
        result = cur.fetchone()
        return result


    @staticmethod
    def delete_attendee_by_uid(uid):
        sql = "DELETE FROM contact_info WHERE attendee_id=%s;"
        conn = Nimbus_Attendees._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=uid)
        if res == 1:
            return f'Deleted id : {uid}'
        else:
            return f'attendee_id : {uid} does not exist'

if __name__ == "__main__":
    nimbus = Nimbus_Attendees()
    conn = Nimbus_Attendees._get_connection()
    cur = conn.cursor()
    try:
        if cur.connection:
              print("Connected")
              print("Testing get_all_attendee")
              for i in nimbus.get_all_attendees():
                  print(i)
              print("testing creating a user")
              print(nimbus.get_attendee_by_uid('aarger0@fda.gov'))
        else:
            print("No connection")
    except Exception as e:
        print(str(e))
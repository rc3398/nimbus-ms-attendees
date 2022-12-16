import pymysql
import os


class Nimbus_Attendees:

    def __int__(self):
        self.cursor = self._get_connection().cursor()

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

if __name__ == "__main__":
    
   nimbus = Nimbus_Attendees()
   conn = Nimbus_Attendees._get_connection()
   cur = conn.cursor()
   try:
       if cur.connection:
            print("Connected")
       else:
           print("No connection")
   except Exception as e:
       print(str(e))
   
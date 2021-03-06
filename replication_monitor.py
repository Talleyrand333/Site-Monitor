import datetime
import mysql.connector
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()


class DatabaseMonitor:
    def __init__(self) -> None:
        #Initialize email and database credentials from decrypted file saved in folder
        self.email_user = os.getenv('EM_USER')
        self.password = os.getenv('EM_PASS')
        self.sub = "ERPNext BCP ALERT!"
        self.msg = "NOT CONNECTED"
        self.dbhost =  os.getenv('DB_HOST')
        self.dbuser= os.getenv('DB_USER')
        self.dbpass= os.getenv('DB_PASS')
        self.primary_recipients = ['ebuka.akeru@manqala.com','collins.frederick@tepngcpfa.com']
        self.secondary_recipients = ['dev@manqala.com','ict@tepngcpfa.com']
        self.connection = False
        


    def fetch_credential_status(self,result_set) -> dict:
        #Analyse the replication status of the result sent from the python monitor.
        slave_io =  result_set[0]['Slave_IO_Running'] 
        slave_sql = result_set[0]['Slave_SQL_Running']
        replication_status = True if slave_io and slave_sql == "Yes" else False
        date = datetime.date.today().strftime("%Y-%m-%d")
        data_ = """Subject: {}      \n\n Dear Team, \n Please see the latest update from the Database Instance of the CPFA for {}. \n\t Slave IO : {}\n
        Slave SQL: {} \n\nFrom the parsed report, the replication status is {} \n\nPlease See the dump of the replication status \n\n{} """.format(self.sub,date,slave_io,slave_sql, 'Working' if replication_status else 'Not Working',result_set[0])
        credentials = {}
        credentials['body'] = data_
        credentials['status'] = replication_status
       
        return credentials




    def check_database_uptime_status(self) -> bool:
        #Check the database status of a local instance
        connection = False
        try:
            connection = mysql.connector.connect(host=self.dbhost, user=self.dbuser, passwd=self.dbpass)
        except:
            # raise
            #Send mail to users or attempt to restart
            print("ERROR  OCCURED")
            self.send_mail()

        if connection:
            cursor =  connection.cursor()
            cursor.execute("SHOW SLAVE 'master03' STATUS")
            result_set = cursor.fetchall()
            row_headers = [x[0] for x in cursor.description] #Extract headers
            json_data = []
            for result in result_set:
                json_data.append(dict(zip(row_headers,result)))
            credentials = self.fetch_credential_status(json_data)
            self.send_mail(arg_list=credentials)
        else:
            print("CANNOT CONNECT")
            self.send_mail()

    

    def send_mail(self,arg_list:dict = None) -> None:
        #Simple smtp function that receives a dictionary of arguments or Nothing and sends a response to a defined group.
        body = 'Subject: {} \n\n\nThe  database of the BCP Site is not responding, Please take a look ASAP!'.format(self.sub) if not arg_list else arg_list['body']
        with smtplib.SMTP('smtp.office365.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(self.email_user, self.password)
            recipients = self.primary_recipients+self.secondary_recipients if  not arg_list.get('status') else self.primary_recipients
            smtp.sendmail(self.email_user, recipients, body)
    
    
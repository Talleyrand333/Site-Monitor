import datetime
import mysql.connector
import smtplib
from dotenv import load_dotenv
import email
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


load_dotenv()


class DatabaseMonitor_T:
    def __init__(self) -> None:
        #Initialize email and database credentials from decrypted file saved in folder
        # self.email_user = os.getenv('EM_USER')
        # self.email_user = 'p020004@tepngcpfa.com'
        self.email_user = 'manqalaemailacc@gmail.com'
        self.password = 'paulpogba6'
        # self.password = os.getenv('EM_PASS')
        # self.password = '@DM4ERP&Next_2021'
        self.sub = "ERPNext BCP ALERT!"
        self.msg = "NOT CONNECTED"
        self.dbhost =  os.getenv('DB_HOST')
        # self.dbuser= 'monitor'
        # self.dbpass='Y563NDHE!$@'
        # self.dbpass='admin'
        self.dbuser= os.getenv('DB_USER')
        self.dbpass= os.getenv('DB_PASS')
        # self.primary_recipients = ['ebuka.akeru@manqala.com','collins.frederick@tepngcpfa.com']
        self.primary_recipients = ['ebuka.akeru@manqala.com','collins.frederick@tepngcpfa.com']
        self.secondary_recipients = ['dev@manqala.com','ict@tepngcpfa.com']
        self.connection = False
        


    def fetch_credential_status(self,result_set) -> dict:
        #Analyse the replication status of the result sent from the python monitor.
        slave_io =  result_set[0]['Slave_IO_Running'] 
        slave_sql = result_set[0]['Slave_SQL_Running']
        msg = email.message.EmailMessage()
        msg['Subject'] = 'Here is my newsletter'
        msg['From'] = self.email_user
        msg['To'] = self.primary_recipients
        replication_status = True if slave_io and slave_sql == "Yes" else False
        date = datetime.date.today().strftime("%Y-%m-%d")
        data_ = """Subject: {}      \n\n Dear Team, \n Please see the latest update from the Database Instance of the CPFA for {}. \n\t Slave IO : {}\n
        Slave SQL: {} \n\nFrom the parsed report, the replication status is {} \n\nPlease See the dump of the replication status \n\n{} """.format(self.sub,date,slave_io,slave_sql, 'Working' if replication_status else 'Not Working',result_set[0])
        font_color = 'color:green' if replication_status else 'color:red'
        alt_data = '''
        <!DOCTYPE html>
        <html>
            <body>
                <div>
                    <p> Dear Team, \n Please see the latest update from the Database Instance of the CPFA for {}. </p>
                </div>
                <div style="{}">
                    <p style="font-family:Georgia, 'Times New Roman', Times, serif;color#454349;">SLAVE IO: {}</p>
                    <p style="font-family:Georgia, 'Times New Roman', Times, serif;color#454349;"SLAVE SQL: {}</p>
                    <p>From the parsed report, the replication status is {} </p>
                </div>
                <p> Please See the dump of the replication status query  </p>
            </body>
        </html>
        '''.format(date,font_color,slave_io,slave_sql,"WORKING" if replication_status else "NOT WORKING",)
        
        
        
        credentials = {}
        credentials['message'] = alt_data
        credentials['body'] = data_
        credentials['status'] = replication_status
       
        return credentials


    def check_database_uptime(self) -> bool:
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
        msg = email.message.EmailMessage()
        msg['Subject'] = 'BCP UPDATE'
        msg['From'] = self.email_user
        msg['To'] = self.primary_recipients
        date = datetime.date.today().strftime("%Y-%m-%d")
        font_color = 'color:green' if arg_list['status'] else 'color:red'
        # data_ = """Subject: {}      \n\n Dear Team, \n Please see the latest update from the Database Instance of the CPFA for {}. \n\t Slave IO : {}\n
        # Slave SQL: {} \n\nFrom the parsed report, the replication status is {} \n\nPlease See the dump of the replication status \n\n{} """.format(self.sub,date,slave_io,slave_sql, 'Working' if replication_status else 'Not Working',result_set[0])        
        msg.set_content(arg_list['message'],subtype='html')
        
        with smtplib.SMTP('smtp.outlook.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(self.email_user, self.password) 
            # print(self.email_user)
            recipients = self.primary_recipients if arg_list['status'] else self.primary_recipients+self.secondary_recipients
            print("BEFORE SEND")
            print(recipients)
            smtp.sendmail(self.email_user,recipients, msg.as_string())

from replication_monitor import DatabaseMonitor

moni = DatabaseMonitor()
moni.check_database_uptime()




# import mysql.connector
# import smtplib

# em = 'manqalaemailacc@gmail.com'
# pd = 'paulpogba6'
# sub = "BCP ALERT!"
# msg = "NOT CONNECTED"
# connection = False


# def send_update(message):
#     with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
#             smtp.ehlo()
#             smtp.starttls()
#             smtp.ehlo()
#             smtp.login(em, pd)
#             subj = "Site availability unconfirmed"
#             body = 'Subject: UPDATE \n\n\n  Please find below the update from the Master Slave replication {}'.format(message)
#             smtp.sendmail(em, 'ebukaakeru@gmail.com', body)



# def send_mail():
#     with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
#             smtp.ehlo()
#             smtp.starttls()
#             smtp.ehlo()
#             smtp.login(em, pd)
#             subj = "Site availability unconfirmed"
#             body = f'Subject: {subj}\n\n\n It seems the database of the BCP Site is down, Please take a look ASAP'
#             smtp.sendmail(em, 'ebukaakeru@gmail.com', body)

# try:
#     connection = mysql.connector.connect(host="localhost", user='monitor', passwd='Y563NDHE!$@')
# except:
#     # raise
#     #Send mail to users or attempt to restart
#     send_mail()
    

# if connection:
#     cursor =  connection.cursor()
#     cursor.execute("SHOW SLAVE MASTER03 STATUS")
#     for i in cursor:
#         print(i)


import smtplib
import email.utils
from email.mime.text import MIMEText
import psycopg2
import pendulum

# Backtrack date to 3 days from current date
now = pendulum.now("Pacific/Auckland")
date = now.subtract(days=3)
event_date = date.format("YYYY-MM-DD", formatter="alternative")

# Open connection to Postgres table
conn = psycopg2.connect(host="localhost", database="test", user="admin", password="123")
print("Database Connected")
cur = conn.cursor()
rowcount = cur.rowcount

# Check row count for events that came in based on event_date
def check_count():
    
    print("Check Event Daily row count")
    
    thereshold = 1000000

    cur.execute(""" Select 
                        row_count,
                        created_at::DATE
                    FROM
                        test
                    WHERE
                        created_at::DATE = '{}';
                """.format(event_date))
    
    row = cur.fetchone()
    row_count = int(row[0])
    date = row[1]
    
    #check if row count is less than threshold
    if (row_count < threshold):
        print("\nDouble checking: Row count problem")
        print("Row count no good. Only : " + str(row_count))
        print("Trigger sending email now")

        #send email since the row count is lower than threshold
        message(str(row_count),str(date))

    else:
        print("Row count good")   

# Draft your message here
def message(row_count,eventdate):
    

    author = 'automail@gmail.com' 
    recipient_list = 'test1@gmail.com,test2@gmail.com'

    msg = MIMEText('Good Morning,\n\nDetected Events on ' + eventdate + ' row count is lower than the threshold (1,000,000 rows).\n\nThe row count is : ' + row_count + '\n\nPlease investigate on this issue. \n\n\nThank you,\nSupport Team')
    msg['To'] = email.utils.formataddr(('Recepient', recipient_list))
    msg['From'] = email.utils.formataddr(('Python Automated Mail', 'automail@gmail.com'))
    msg['Subject'] = 'Events Row Count < 1,000,000'
    
    send_email(author, recepient_list.split(','), msg.as_string())

def send_email(sent_from,to,email_text):
    try:
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.set_debuglevel(True)
        server_ssl.ehlo()
        server_ssl.login('auto@gmail.com','password')
        server_ssl.sendmail(sent_from,to,email_text)
        server_ssl.close()

    except:  
        print ('Something went wrong...')

if __name__ == '__main__':
    check_count()
    conn.commit()
    cur.close()

import imaplib
import email
from email import policy
import datetime
from time import sleep
from database.user_database import DB, sqlite3

CHECK_TIMEOUT_SEC = 10
FROM_EMAIL  = "microstrategySubscription@gmail.com"
FROM_PWD    = "Ceo143566!@"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

db = DB('database/bot_database.sqlite', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        mail.login(FROM_EMAIL, FROM_PWD)
        
        mail.select('inbox')
        
        result, data = mail.search(None, 'UNSEEN')
    
        ids = data[0]
        id_list = ids.split()

        for id in id_list:
            result, data = mail.fetch(id, "(RFC822)")
            raw_email = data[0][1]
            raw_email_string = raw_email.decode()

            email_message = email.message_from_string(raw_email_string, policy=policy.default)
            message_from = email.utils.parseaddr(email_message['From'])

            if message_from[1] == 'DistributionServices@MicroStrategy.com':
                title = email_message['Subject'].split(';')
                trigger_name = title[0].strip()
                date_time = datetime.datetime.strptime(';'.join(title[1:]), "%Y-%m-%d;%H.%M.%S")
                all_triggers = db.get_triggers_by_name(trigger_name)
                for row in all_triggers:
                    db.insert_date_trigger(row['ID'], date_time)

                print(trigger_name)
                print(date_time)
                print()
        return
    except Exception as e:
        print(str(e))

while True:
    read_email_from_gmail()
    sleep(CHECK_TIMEOUT_SEC)
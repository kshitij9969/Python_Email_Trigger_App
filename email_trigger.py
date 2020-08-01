import imaplib
import email
import re
import database
import smtplib
import ssl
import sys
import time

'''
Provide your email password and folder name.
It will continuously check for new mail, do the transaction and return successful/ not successful mails to the sender.
'''


def send_mail(from_addr, password, to_addr, message):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = from_addr
    password = password
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(from_addr, to_addr, message)
        # TODO: Send email here
    except Exception as e:
        print(e)


email_user = sys.argv[1]
email_pass = sys.argv[2]


def main():
    global email_user
    global email_pass
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(email_user, email_pass)
    mail.select(str(sys.argv[3]), readonly=False)
    type, data = mail.search(None, "ALL")
    print(data)
    mail_ids = data[0]
    id_list = mail_ids.split()

    for mail_id in data[0].split():
        typ, data = mail.fetch(mail_id, '(RFC822)')
        print(mail_id)
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
        email_from = str(email_message).split("From: ", 1)[1].split("\nDate:", 1)[0]
        email_from = str(re.findall('(?s)<.+>', email_from)[0]).strip('<').strip('>')
        print(email_from)
        # format of the subject = Deposit/withdraw #### from customer_id #### amount ####
        print(subject)
        try:
            CUSTOMER_ID = int(re.findall('customer_id\s[0-9]+', subject)[0].split(' ')[1])
            amount = int(re.findall('amount\s[0-9]+', subject)[0].split(' ')[1])
            action = str(re.findall('deposit|withdraw', subject)[0])
            print(CUSTOMER_ID)
            print(amount)
            print(action)
            if all([CUSTOMER_ID, amount, action]):
                if action == 'withdraw':
                    response = database.withdraw(CUSTOMER_ID, amount)
                    print("Transaction successful" in response)
                    if "Transaction successful" in response:
                        mov, data = mail.store(mail_id, '+FLAGS', '\\Deleted')
                        mail.expunge()
                    else:
                        mov, data = mail.store(mail_id, '+FLAGS', '\\Deleted')
                        mail.expunge()
                    send_mail(email_user, email_pass, email_from, response)
                else:
                    response = database.deposit(CUSTOMER_ID, amount)
                    print("Transaction successful" in response)
                    if "Transaction successful" in response:
                        mov, data = mail.store(mail_id, '+FLAGS', '\\Deleted')
                        mail.expunge()
                    else:
                        mov, data = mail.store(mail_id, '+FLAGS', '\\Deleted')
                        mail.expunge()
                    send_mail(email_user, email_pass, email_from, response)
        except:
            mov, data = mail.store(mail_id, '+FLAGS', '\\Deleted')
            mail.expunge()
            send_mail(sys.argv[1], sys.argv[2], email_from, 'invalid_subject_format, it should be'
                                                            'deposit/withdraw #### from customer_id ####'
                                                            ' amount ####, (case-sensitive)')
        else:
            mov, data = mail.store(mail_id, '+FLAGS', '\\Deleted')
            mail.expunge()
            send_mail(email_user, email_pass, email_from, 'invalid_subject_format, it should be'
                                                            'deposit/withdraw #### from customer_id'
                                                            ' #### amount ####, (case-sensitive)')


if __name__=="__main__":
    while(1):
        main()
        time.sleep(10)

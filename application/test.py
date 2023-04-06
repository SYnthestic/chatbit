import os
import smtplib
import imghdr
from email.message import EmailMessage
EMAIL_USER = 'samuel.yam@thinkture.com.sg'
EMAIL_PASS = 'ihK!.sNGCfA4HXG'

# EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
# EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
EMAIL_ADDRESS = 'sam75yam@gmail.com'
EMAIL_PASSWORD = 'SP2124syzm'

# # Create email message
msg = EmailMessage()
msg['Subject'] = "Feedback on our service"
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'samuelyam953@gmail.com'
msg.set_content('How about dinner at 6pm this Saturday?')
            
# Connect to SMTP server and send email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    print(EMAIL_ADDRESS)
    print(EMAIL_PASSWORD)

                
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                
                
    # subject = 'Feedback at QueueCut'
    # body = 'Blah blah blah'
    # msg = f'Subject: {subject}\n\n{body}'
                
    smtp.send_message(msg)
                
    # smtp.sendmail(EMAIL_ADDRESS, 'sam75yam@gmail.com')
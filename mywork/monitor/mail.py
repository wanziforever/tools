#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import smtplib
from email.mime.text import MIMEText

mailto_list = ['wanziforever@163.com']
mail_host = "mail.hisense.com"
mail_user = "wangliang8@hisense.com"
mail_pass = "Wl@800803"
mail_postfix = "hisense.com"

def send_mail(sub, content):
    me = mail_user + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(mailto_list)

    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(me, mailto_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

if __name__ == "__main__":
    if send_mail("test", "denny send email"):
        print "send success"
    else:
        print "send failed"
    
    

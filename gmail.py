import smtplib

def send_email(to, msg):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(username, pw)
    server.sendmail(
      "reincara@gmail.com",
      to,
      msg)
    server.quit()

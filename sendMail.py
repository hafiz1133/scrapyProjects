try:
    import smtplib
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import datetime
    import json
    import requests

    obj = smtplib.SMTP(host='Smtp.gmail.com', port=587, timeout=1000)
    obj.starttls()
    obj.ehlo()
    msg = MIMEMultipart()
    filename = 'big_cube.csv'

    msg['Subject'] = "{}{}".format(filename, datetime.datetime.now())
    password = "hafiz1133github"
    obj.login("rixtysoft02@gmail.com", password)
    with open(filename, 'rb') as file:
        # Attach the file with filename to the email
        msg.attach(MIMEApplication(file.read(), Name=filename))

    obj.sendmail("rixtysoft02@gmail.com", "syedumairzafar@gmail.com", msg.as_string())
    obj.quit()

    '''
        The most Important thing is that you must change GMAIL settings before using it
        In setting-> Forwarding and POP/IMAP, Enable IMAP
        In Account setting ON Less secure ap access
    '''
except:

    headers={"Authorization": "Bearer ya29.a0AfH6SMBY-vlNc7r51RZMfVyB7qmh0-KL_nXe5n7idgLqVHl2x8OIpgmk3mS4u50kMDdknx5TiahtqYt6kB-7NDBh-tCqod9Z9KGjk6IRrYhfhLcq7z0n8TWxN8j2M__xb_-eZmAaG4YySW8Vo9_9T_qPH-nsjCEIiesJWgt29Mg"}
    para={
        "name":"big_cube.csv"
    }
    files={
    'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': open("big_cube.csv", "rb")
    }

    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files
    )
    a=r.text.split('\n')[2].split(':')[1].replace('"', "")
    b=a.replace("'","")
    link=b.replace(",","")
    link=link.lstrip()
    # print(link)

    fileink='https://drive.google.com/file/d/'+str(link)+'/view?usp=sharing'

    text='''
            
    '''
    obj = smtplib.SMTP(host='Smtp.gmail.com', port=587, timeout=1000)
    obj.starttls()
    obj.ehlo()
    msg = MIMEMultipart()
    filename = 'big_cube.csv'
    body=fileink
    body = MIMEText(body)
    msg.attach(body)
    msg['Subject'] = "{}{}".format(filename, datetime.datetime.now())
    password = "hafiz1133github"
    obj.login("rixtysoft02@gmail.com", password)

    obj.sendmail("rixtysoft02@gmail.com", "syedumairzafar@gmail.com", msg.as_string())
    obj.quit()



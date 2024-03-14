import requests
import time
import json
import datetime
import smtplib
import urllib3
import warnings
from urllib3.exceptions import NotOpenSSLWarning
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendEmail(body="badminton court"):
    mail_host = 'smtp.163.com'
    sender_email = "seuzhusiyu@163.com"
    sender_password = "ZSY13851228256"
    receiver_email = "524537167@qq.com"
    receiver_email_wanzi = "18679959637@163.com"
    subject = "badminton court is here"

    # Set up the MIME
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach the body with the msg instance
    message.attach(MIMEText(body, 'plain'))
    # Create SMTP session for sending the mail
    try:
        print("create server")
        server = smtplib.SMTP()  # Use 587 for TLS
        print("connect to mail host")
        server.connect(mail_host, 25)
        # Login with the email and password
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.sendmail(sender_email, receiver_email_wanzi, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


def convert_epoch_to_local(epoch_time, is_milliseconds=True):
    """
    Convert epoch time to local time.

    :param epoch_time: Epoch time in milliseconds or seconds.
    :param is_milliseconds: Set True if epoch time is in milliseconds, False if in seconds.
    :return: Local time as a datetime object.
    """
    if is_milliseconds:
        # Convert milliseconds to seconds
        epoch_time /= 1000

    # Convert to local time
    local_time = datetime.datetime.fromtimestamp(epoch_time)
    return local_time


def query_and_send_email():
    warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

    url = 'https://jsapp.jussyun.com/jiushi-core/venue/getVenueGround'
    headers = {
        'Host': 'jsapp.jussyun.com',
        'os_type': 'wechat_mini',
        'gw_channel': 'api',
        'app_id': '0ff444f417de34c1352af3b3ffc30348',
        'js_sign': 'ZmYyNzY3ZWQyZTE3YmNhMWEzZTk2YmNkYzliNzVmZTU=',
        'os_version': 'Windows 11 x64',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090919) XWEB/8531',
        'Content-Type': 'application/json',
        'xweb_xhr': '1',
        'device_type': 'microsoft',
        'token': 'PBdsyB6wIBTZNp2V9bVHAQBCJ7TsLOfyfbZsTQOlfsI100aN7VBhH/kbhfFg7DwPVGndMrjkD4Vljlk3p97RoT+vlpFA3uQuOpGDlct2v+5p6I6uDIES6ANmNvHYsXWD6d821EHGsZvUPrHL5ZmDheWIPetcQWSF1F5LtHtRBgo',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://servicewechat.com/wxbd4ec54a9e9ce6dd/96/page-frame.html',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'acw_tc=3daa4d1e17103755319921519ec5c3129ed8172d33816fb8bb50463d44'
    }

    data = '{"venueId":"27","bookTime":"1710518400000"}'

    response = requests.post(url, headers=headers, data=data, verify=False)
    # print(response.text)
    data = json.loads(response.text)
    print(datetime.datetime.now())
    for status in data["data"]["statusList"]:
        startTime = convert_epoch_to_local(int(status["startTime"]))
        h = startTime.hour;

        if   h == 12 or h == 13 or h == 14:
            found = False
            print("checking courts at " + str(h) +":00")
            for court in status["blockModel"]:
                court_id = int(court["groundId"])
                if court_id == 216 or court_id == 217: #skip court 34 and 35
                    continue
                court_id = court_id - 142
                if court["status"] == "1": 
                    found = True
                    emailMessage = "Court: " + court["groundName"] + " Time: " + str(startTime)
                    print(emailMessage)
                    sendEmail(emailMessage)
            if not found:
                print("no court available")

urllib3.disable_warnings()

if __name__ == "__main__":
    for _ in range(6):  # 6 iterations for 6 x 10 seconds = 60 seconds
        query_and_send_email()
        time.sleep(10)

import requests
import os
import hashlib
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_wordpress"
)

mycursor = mydb.cursor()
mycursor.execute(
    "SELECT * FROM wp_posts where post_type='attachment' && post_mime_type='image/jpeg' || post_mime_type='image/png' ")
datas = mycursor.fetchall()
for row in datas:
    path = row[18]
    filename = os.path.basename(path)
    title = row[5]
    caption = row[6]
    tipefile = row[21]

    createSig = "!Nr"+filename
    hashing = hashlib.sha256((createSig).encode()).hexdigest()
    upper_hashing = hashing.upper()
    sig = "?sig="+upper_hashing
    url = "https://api2228.kgnewsroom.com/api/files/uploadsiloimage"+sig
    payload = {
        'Title': title,
        'Caption': caption,
        'Byline': 'test byline'
    }
    content = requests.get(path).content
    open("temp", "wb").write(content)
    fileobj = open("temp", "rb")
    files = {'file': open('temp', 'rb')}
    headers = {}
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)
    print(response.text)

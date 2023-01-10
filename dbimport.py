import mysql.connector
import csv
from firebase_admin import credentials, initialize_app, storage

cred = credentials.Certificate("C:/Users/pheew/mysql/letsfestival-d6f3d-84c458f18732.json")
initialize_app(cred, {'storageBucket': 'letsfestival-d6f3d.appspot.com'})

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="balloon",
)

cursor = db.cursor()

#cursor.execute("CREATE TABLE data (f_id int(12) auto_increment primary key, f_index VARCHAR(200), f_location VARCHAR(200), f_address VARCHAR(200), f_name VARCHAR(200), f_time VARCHAR(200), f_month VARCHAR(200), f_image1 VARCHAR(500), f_image2 VARCHAR(500))")


row_num = 0

with open('C:/Users/pheew/Desktop/festival2.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if (row_num < 100):
            row_num += 1
            fileName = "C:/Users/pheew/Desktop/festival_/{}-1.png".format(row_num)
            bucket = storage.bucket()
            blob = bucket.blob(fileName)
            blob.upload_from_filename(fileName)
            # Opt : if you want to make public access from the URL
            blob.make_public()
            fileName2 = "C:/Users/pheew/Desktop/festival_/{}-2.png".format(row_num)
            bucket2 = storage.bucket()
            blob2 = bucket.blob(fileName2)
            blob2.upload_from_filename(fileName2)
            # Opt : if you want to make public access from the URL
            blob2.make_public()
            print(row)
            sql = "INSERT INTO data (f_index, f_location, f_address, f_name, f_time, f_month, f_image1, f_image2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (row[0], row[1], row[2], row[3], row[4], row[5], blob.public_url, blob2.public_url)
            cursor.execute(sql, val)

db.commit()

print("good")

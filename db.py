import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="bgxvyyzg6jsrhj5qwwap-mysql.services.clever-cloud.com",
        user="uxuposwsyowholjw",
        password="hMpaxzFwpeNd62fa1r9Z",
        database="bgxvyyzg6jsrhj5qwwap"
    )
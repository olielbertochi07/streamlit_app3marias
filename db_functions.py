import mysql.connector
from decouple import config

DB_HOST = config('DB_HOST')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_PORT = config('DB_PORT')
DB_DATABASE = config('DB_DATABASE')

def get_database_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        database=DB_DATABASE
    )
def check_login(username, password):
    mydb = get_database_connection()
    mycursor = mydb.cursor()
    sql = "CALL `App_Consulta_Sessao`(%s, %s)"
    mycursor.execute(sql, (username, password))
    result = mycursor.fetchone()
    mycursor.close()
    mydb.close()
    return result

def get_filtered_data(filtro_id, filtro_codigo, filtro_descricao):
    mydb = get_database_connection()
    mycursor = mydb.cursor()
    sql = "CALL `App_Consulta_Stock`(%s, %s, %s, '100')"
    mycursor.execute(sql, (filtro_id, f'%{filtro_codigo}%', f'%{filtro_descricao}%'))
    results = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return results
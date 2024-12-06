try:
    from dotenv import load_dotenv
    import pyodbc
    import os
except Exception as e:
    print(f"Error al importar las librerias en data_base.py, {e}")

load_dotenv()

try:
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={os.getenv("DATABASE_SERVER")};'
        f'DATABASE={os.getenv("DATABASE_NAME")};'
        f'UID={os.getenv("DATABASE_USER")};'
        f'PWD={os.getenv("DATABASE_PASSWORD")}'
    )
    cursor = conn.cursor()
    print(f"Conexion realizada con exito, {cursor}")
except Exception as e:
    message = f"Error en la conexion con la base de datos, {e}"
    print(message)

# def create_table_curstomers():
#     try:
#         with conn.cursor() as cursor:
#             cursor.execute("""
#                 IF EXISTS (SELECT * FROM sysobjects WHERE name='rptUnosof_Customers_Dev' AND xtype='U')
#                 BEGIN
#                     DROP TABLE rptUnosof_Customers_Dev
#                 END
#             """)
#             cursor.commit()
#             cursor.execute("""
#                 CREATE TABLE rptUnosof_Customers_Dev(
#                     cus_id INT PRIMARY KEY,
#                     cus_market NVARCHAR(50),
#                     cus_opening_date DATE,
#                     cus_credit_limit FLOAT,
#                     cus_term NVARCHAR(40),
#                     cus_ruc_resale NVARCHAR(30),
#                     cus_customer NVARCHAR(100),
#                     cus_parent_billing NVARCHAR(150),
#                     cus_parent_trading NVARCHAR(150),
#                     cus_flow NVARCHAR(20),
#                     cus_shipping_address NVARCHAR(150),
#                     cus_cargo_agency NVARCHAR(50),
#                     cus_incoterm NVARCHAR(15),
#                     cus_sales_rep NVARCHAR(30),
#                     cus_phone NVARCHAR(MAX),
#                     cus_city NVARCHAR(40),
#                     cus_country NVARCHAR(40),
#                     cus_sri_country INT,
#                     cus_created NVARCHAR(30)
#                 )
#             """)
#             cursor.commit()
#     except Exception as e:
#         message = f"Error al crear la tabla, {e}"
#         print(message)

# create_table_curstomers()

def log_to_db(log_level, message, endpoint=None, status_code=None):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Logs_Info (id_group, log_level, message, endpoint, status_code)
            VALUES (?, ?, ?, ?, ?)
        """, 2, log_level, message, endpoint, status_code)
        conn.commit()

url_login_query = """SELECT prm_valor
                FROM dbo.Parametros_Sistema
                WHERE id_grupo = 1 AND prm_descripcion = 'url_login'"""

user_query = """SELECT prm_valor
                FROM dbo.Parametros_Sistema
                WHERE id_grupo = 1 AND prm_descripcion = 'user_name'"""

password_query = """SELECT prm_valor
                FROM dbo.Parametros_Sistema
                WHERE id_grupo = 1 AND prm_descripcion = 'password'"""

user_mail_query = """SELECT prm_valor
                FROM dbo.Parametros_Sistema
                WHERE id_grupo = 5 AND prm_descripcion = 'user_mail'"""

password_mail_query = """SELECT prm_valor
                FROM dbo.Parametros_Sistema
                WHERE id_grupo = 5 AND prm_descripcion = 'password_mail'"""

url_cst_query = """SELECT prm_valor
                FROM dbo.Parametros_Sistema
                WHERE id_grupo = 11 AND prm_descripcion = 'url_cst'"""

insert_query = """INSERT INTO rptUnosof_Customers_Dev VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

def get_url():
    try:
        url = cursor.execute(url_login_query)
        result = cursor.fetchone()
        if result:
            url = result[0]
            print(f"URL obtenida: {url}")
            return str(url.encode('utf-8').decode('utf-8'))
        else:
            return None, "Error al obtener la url de la base de datos"
    except Exception as e:
        print(f"Ocurrio un error al obtener la url, {e}")

def get_user():
    try:
        user = cursor.execute(user_query)
        result = cursor.fetchone()
        if result:
            user = result[0]
            print(f"Usuario obtenido: {user}")
            return user.encode('utf-8').decode('utf-8')
    except Exception as e:
        print(f"Ocurrio un error al obtener el usuario, {e}")
        
def get_password():
    try:
        password = cursor.execute(password_query)
        result = cursor.fetchone()
        if result:
            password = result[0]
            print(f"Usuario obtenido: {password}")
            return password.encode('utf-8').decode('utf-8')
    except Exception as e:
        print(f"Ocurrio un error al obtener el usuario, {e}")

def get_url_cst():
    try:
        home = cursor.execute(url_cst_query)
        result = cursor.fetchone()
        if result:
            home = result[0]
            print(f"URL home obtenida: {home}")
            return home.encode('utf-8').decode('utf-8')
    except Exception as e:
        print(f"Ocurrio un error al obtener el usuario, {e}")

def get_user_mail():
    try:
        user_mail = cursor.execute(user_mail_query)
        result = cursor.fetchone()
        if result:
            user_mail = result[0]
            print(f"Usuario de correo obtenido: {user_mail}")
            return user_mail
    except Exception as e:
        print(f"Ocurrio un error al obtener el usuario de correo electronico, {e}")

def get_password_mail():
    try:
        passwd_mail =  cursor.execute(password_mail_query)
        result = cursor.fetchone()
        if result:
            passwd_mail = result[0]
            print(f"Contrasenia del correo obtenido: {passwd_mail}")
            return passwd_mail
    except Exception as e:
        print(f"Ocurrio un error al obtener la contrasenia del correo, {e}")
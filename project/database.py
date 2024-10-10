import cx_Oracle
import os
from dotenv import load_dotenv

load_dotenv()
ENV_VAR_HOST = os.getenv('HOST')
ENV_VAR_PORT = os.getenv('PORT')
ENV_VAR_SERVICE_NAME = os.getenv('SERVICE_NAME')
ENV_VAR_ORACLE_CLIENT_PATH = os.getenv('ORACLE_CLIENT_PATH')
ENV_VAR_DB_USER = os.getenv('DB_USER')
ENV_VAR_DB_PASSWORD = os.getenv('DB_PASSWORD')


# ORACLE CLIENT - LOCAL PATH==========================================
cx_Oracle.init_oracle_client(lib_dir=ENV_VAR_ORACLE_CLIENT_PATH)
# ====================================================================

# ORACLE CONNECTION======================================================================
def ora_connection():
    dsn_tns = cx_Oracle.makedsn(ENV_VAR_HOST,ENV_VAR_PORT,service_name=ENV_VAR_SERVICE_NAME) 
    con = cx_Oracle.connect(user=ENV_VAR_DB_USER, password=ENV_VAR_DB_PASSWORD, dsn=dsn_tns) 
    cursor = con.cursor()
# ========================================================================================


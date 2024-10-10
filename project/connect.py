import cx_Oracle
import platform
import sys
import os

#Oracle Client Path
cx_Oracle.init_oracle_client(lib_dir=r"INLCUDE PATH TO ORACLE CLIENT")

#Database Connection
dsn_tns = cx_Oracle.makedsn('0.0.0.0', '1521', service_name='DBNAME') 
con = cx_Oracle.connect(user=r'USER', password=r'PASSWORD', dsn=dsn_tns) 
cur = con.cursor()


# Import necessary modules and classes
from http.client import HTTPException  # Import HTTPException from http.client
from fastapi import FastAPI  # Import FastAPI class
from fastapi import HTTPException  # Import HTTPException from FastAPI
from fastapi import status  # Import status codes from FastAPI
from fastapi import Depends  # Import Depends for dependency injection
from project.common import create_access_token, oauth2_schema  # Import custom functions and schemas
from fastapi.security import OAuth2PasswordRequestForm  # Import OAuth2PasswordRequestForm for handling form data
from dotenv import load_dotenv  # Import load_dotenv to load environment variables from a .env file
import os  # Import os module for environment variable access
import cx_Oracle  # Import cx_Oracle for Oracle database connectivity

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables for database connection
ENV_VAR_HOST = os.getenv('HOST')
ENV_VAR_PORT = os.getenv('PORT')
ENV_VAR_SERVICE_NAME = os.getenv('SERVICE_NAME')
ENV_VAR_ORACLE_CLIENT_PATH = os.getenv('ORACLE_CLIENT_PATH')
ENV_VAR_DB_USER = os.getenv('DB_USER')
ENV_VAR_DB_PASSWORD = os.getenv('DB_PASSWORD')

# Retrieve API credentials from environment variables
user = os.getenv('API_USER')
passw = os.getenv('API_PASSWORD')
ENV_VAR_API_VER_FOLDER = os.getenv('API_VER_FOLDER')

# Initialize Oracle client with the specified local path
cx_Oracle.init_oracle_client(lib_dir=ENV_VAR_ORACLE_CLIENT_PATH)

app = FastAPI(title='CCT Link',
            description='API Restful',
            version='BETA',
            contact={
                "acces_token": "Colon Container Terminal"
                })

@app.get('/')
async def index():

    return {"message": "CCTLINK API"}

# AUTH2 LOGIN ==================================================
@app.post('/auth')
async def auth(data: OAuth2PasswordRequestForm = Depends()):
        
        
        if data.username == user and data.password == passw:
                return {
                    'access_token': create_access_token(user),
                    'token_type': 'Bearer'
                }
        else:
                raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Username or Password Incorrect',
                        headers={ 'WWWW-Autenticate:' 'Bearer' }
                )

         
# Operation Berth =========================================================================
@app.get(ENV_VAR_API_VER_FOLDER+"/OperationBerth/{PI_DATE_FROM_ETB}/{PI_DATE_TO_ETB}")
async def cntr_query_hold(PI_DATE_FROM_ETB,PI_DATE_TO_ETB,token:str=Depends(oauth2_schema)):
        
        # ORACLE CONNECTION======================================================================
        dsn_tns = cx_Oracle.makedsn(ENV_VAR_HOST,ENV_VAR_PORT,service_name=ENV_VAR_SERVICE_NAME) 
        con = cx_Oracle.connect(user=ENV_VAR_DB_USER, password=ENV_VAR_DB_PASSWORD, dsn=dsn_tns) 
        cursor = con.cursor()
        # ========================================================================================        

        ref_cursor = cursor.callfunc('TOS2P_CCT_LINK_API.TOS2F_OPERATION_BERTH',
                             cx_Oracle.DB_TYPE_CURSOR,[PI_DATE_FROM_ETB,PI_DATE_TO_ETB])
        for row in ref_cursor:
                return {"PO_BERTH_ID": row[0],
                        "PO_PS": row[1],
                        "PO_VESSEL_NAME": row[2],
                        "PO_VESSEL_CODE": row[3],
                        "PO_ARR_VOYAGE": row[4],
                        "PO_DEP_VOYAGE": row[5],
                        "PO_ETA_DATE": row[6],
                        "PO_ETB_DATE": row[7],
                        "PO_ETD_DATE": row[8]}
# ========================================================================================
   
# Operation Berth (Vessel Info)
@app.get(ENV_VAR_API_VER_FOLDER+"/VesselInfo/{PI_VESSEL_CODE}")
async def cntr_hold(PI_VESSEL_CODE,token:str=Depends(oauth2_schema)):
    
    # ORACLE CONNECTION======================================================================
    dsn_tns = cx_Oracle.makedsn(ENV_VAR_HOST,ENV_VAR_PORT,service_name=ENV_VAR_SERVICE_NAME) 
    con = cx_Oracle.connect(user=ENV_VAR_DB_USER, password=ENV_VAR_DB_PASSWORD, dsn=dsn_tns) 
    cursor = con.cursor()
    # ========================================================================================        

    ref_cursor = cursor.callfunc('TOS2P_CCT_LINK_API.TOS2F_VESSEL_INFO',
                             cx_Oracle.DB_TYPE_CURSOR,[PI_VESSEL_CODE])
    for row in ref_cursor:
            return {"PO_VESSEL_CODE": row[0],
                    "PO_ARR_VOYAGE": row[1],
                    "PO_DEP_VOYAGE": row[2],
                    "PO_BERTH_ID": row[3],
                    "PO_ETA_DATE": row[4],
                    "PO_ETB_DATE": row[5],
                    "PO_ATB_DATE": row[6],
                    "PO_COMMENCE_DATE": row[7],
                    "PO_COMPLETE_DATE": row[8],
                    "PO_ETD_DATE": row[9],
                    "PO_ATD_DATE": row[10]}


# Container Operation Information 
@app.get(ENV_VAR_API_VER_FOLDER+"/CntrOperationInformation/{PI_CNTR_NUMBER}")
async def cntr_release(PI_CNTR_NUMBER,token:str=Depends(oauth2_schema)):
    
    # ORACLE CONNECTION======================================================================
    dsn_tns = cx_Oracle.makedsn(ENV_VAR_HOST,ENV_VAR_PORT,service_name=ENV_VAR_SERVICE_NAME) 
    con = cx_Oracle.connect(user=ENV_VAR_DB_USER, password=ENV_VAR_DB_PASSWORD, dsn=dsn_tns) 
    cursor = con.cursor()
    # =======================================================================================

    ref_cursor = cursor.callfunc('TOS2P_CCT_LINK_API.TOS2F_CNTR_OPERATION_INFO',
                             cx_Oracle.DB_TYPE_CURSOR,[PI_CNTR_NUMBER])
    for row in ref_cursor:
            return {"PO_VESSEL_NAME": row[0],
                    "PO_TYPE": row[1],
                    "PO_SHIPPING_LINE": row[2],
                    "PO_ARR_DATE": row[3],
                    "PO_DEP_DATE": row[4],
                    "PO_DEP_TIME": row[5]}

# Vessel Operation Summary by Shipping Company 
@app.get(ENV_VAR_API_VER_FOLDER+"/VesselOperationSummary/{PI_SHIPPING_LINE}/{PI_OPD_DATE}")
async def cntr_release(PI_SHIPPING_LINE,token:str=Depends(oauth2_schema)):
    
    # ORACLE CONNECTION======================================================================
    dsn_tns = cx_Oracle.makedsn(ENV_VAR_HOST,ENV_VAR_PORT,service_name=ENV_VAR_SERVICE_NAME) 
    con = cx_Oracle.connect(user=ENV_VAR_DB_USER, password=ENV_VAR_DB_PASSWORD, dsn=dsn_tns) 
    cursor = con.cursor()
    # =======================================================================================

    ref_cursor = cursor.callfunc('TOS2P_CCT_LINK_API.TOS2F_VESSEL_OPERATION_SUM',
                             cx_Oracle.DB_TYPE_CURSOR,[PI_SHIPPING_LINE],[PI_OPD_DATE])
    for row in ref_cursor:
            return {"PO_VESSEL_NAME": row[0],
                    "PO_COMM_DATE_TIME": row[1],
                    "PO_TTL_VALUE": row[2],
                    "PO_DISG_VALUE": row[3],
                    "PO_LOAD_VALUE": row[4]}

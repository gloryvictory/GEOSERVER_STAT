import os
from time import strftime  # Load just the strftime Module from Time
from dotenv import load_dotenv

load_dotenv()


GSERVER_URL = os.getenv("GSERVER_URL", "https://localhost/geoserver/rest")
GSERVER_USER = os.getenv("GSERVER_USER", "admin")
GSERVER_PASS = os.getenv("GSERVER_PASS", "geoserver")
FILE_CSV_NAME = 'layers.csv'
FILE_XLS_NAME = 'layers.xlsx'


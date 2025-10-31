import os # for filesystem operations 
import re # used for error normalization
import logging # structured logging for information and errors
from datetime import date, datetime # for working with dates and parsing a date string
import psycopg2 # postgresql client library (connect, cursors, transactions)
from psycopg2.extras import execute_values # helper for efficient bulk inserts into the table
from typing import Dict, Tuple # tell readers / IDEs what types functions return
from dotenv import load_dotenv # used to load the dotenv file

# Load environment variables from .env file 
load_dotenv()

LOG_DIR = os.getenv("LOG_DIR","logs") # folder with .log files 
# DB connection parameters
PG_HOST = os.getenv("PG_HOST") 
PG_PORT = os.getenv("PG_PORT")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
RUN_DATE = os.getenv("RUN_DATE")

# setup logging

logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Helper functions

def normalizeError(line: str) -> str:
    # remove the white spaces in front and back
    sample = line.strip()
    # remove the leading bracketed timestamp and log level 
    line = re.sub(r'^\[.*?\]\s*\[.*?\]\s*','',sample)

    # remove numbers,UUIDs, hex, strings, file paths, etc...
    sig = re.sub(r'\b[0-9]+\b', '<NUM>', line)
    sig = re.sub(r'\b0x[0-9a-fA-F]+\b', '<HEX>', sig)
    sig = re.sub(r'\b[0-9a-fA-F]{8,}\b', '<HASH>', sig)
    sig = re.sub(r'/[^\s]+', '<PATH>', sig)
    sig = re.sub(r'https?://\S+', '<URL>', sig)
    # collapse whitespace
    sig = re.sub(r'\s+',' ',sig).strip()

    #optionally truncate to a reasonable length
    if (len(sig) > 500):
        sig = sig[:500]+"..."
    
    return sig

def parseLogs(log_dir: str) -> Dict[str, int]:
    # return the signature->(count,sample_message)
    counter: Dict[str, int] = {}
    if not os.path.isdir(log_dir): # if directory is present then True , now not True -> False the if statment to run
        logger.warning("Log directory %s does not exist", log_dir)
        return counter
    
    for fn in os.listdir(log_dir): # take each file from the log_dir directory
        if not fn.endswith('.log'):
            continue # no need to touch that unknown file
        path = os.path.join(log_dir,fn) # join the folder name with the current log file
        logger.info("Parsing file: %s",path)

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as fh: # with is automatically close the file. thats why we used it here
                for line in fh:
                    if "ERROR" in line.upper(): # if the ERROR is present in the line then normalize the error string
                        signature = normalizeError(line)
                        if signature in counter: # checks if the counter already had this particular signature. then just increement the count of that signature
                            counter[signature] = counter[signature] + 1# increement the count + 1
                        else:
                            counter[signature] = 1 # creates a new one
        except Exception as e:
            logger.exception("Failed to read %s: %s",path,e)
    return counter

def writeSummaryToDB(summary: Dict[str, int],run_date:date):
    # Insert aggregated summary rows into postgresql using execute_values

    if not summary:
        logger.info("No errors found; nothing to insert.")
        return
    
    rows = [(run_date,signature,count) for signature,(count) in summary.items()]

    # create a connection to db
    connection = None
    try:
        connection = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            dbname=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD
        )
        cursor = connection.cursor()
        sql = sql = """
INSERT INTO log_table (run_date, error_signature, error_count)
VALUES %s
ON CONFLICT (run_date, error_signature)
DO UPDATE SET error_count = EXCLUDED.error_count;
"""

        execute_values(cursor,sql,rows)
        connection.commit()
        logger.info("Inserted %d rows into log_table",len(rows))
    except Exception:
        logger.exception("Failed to insert into DB")
        if connection:
            connection.rollback()
        raise
    finally:
        if connection: connection.close()

# main function

def run():
    rd = RUN_DATE or date.today().isoformat()
    try:
        run_date = datetime.strptime(rd,"%Y-%m-%d").date()
    except Exception:
        logger.warning("Invalid RUN_DATE '%s' , using today's date",rd)
        run_date = date.today()

    summary = parseLogs(LOG_DIR)
    writeSummaryToDB(summary,run_date)
    logger.info("Run completed for date %s",run_date)

if __name__ == "__main__":
    run()                        





import os
from dotenv import load_dotenv
load_dotenv();
def getEnv(key=None):
    if key is None:
        return None
    return os.getenv(key)

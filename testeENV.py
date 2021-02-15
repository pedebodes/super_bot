import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

CONFIG_PATH = os.environ.get("CONFIG_PATH")
DOMAIN = os.environ.get("DOMAIN")

import pdb; pdb.set_trace()
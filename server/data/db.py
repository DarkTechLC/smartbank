from lib.pyg import Pyg
from settings import *


bank_db = Pyg(
    database=PG_DATABASE,
    port=PG_PORT,
    user=PG_USER,
    password=PG_PASSWORD,
    host=PG_HOST,
)

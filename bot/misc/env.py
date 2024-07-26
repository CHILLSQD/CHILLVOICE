import os
from abc import ABC
from typing import Final

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Env(ABC):
    TOKEN: Final = os.environ.get('TOKEN', 'define me!')
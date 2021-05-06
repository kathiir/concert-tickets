import time

from flask import Flask, request, make_response, jsonify, abort
import os
from config import app, db
from models import Concert, Artist, Performance

import datetime
import random
from genius_api import Genius
from spotify_api import Spotify



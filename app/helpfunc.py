
import os
import requests
import urllib.parse
from flask import redirect, render_template, request, session
from functools import wraps


# writing this for later to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/register")
        return f(*args, **kwargs)
    return decorated_function


# Helper function that calls Merriam Webster API to provide word definitions
def lookup_word(word):
    try:
        k = {'key': os.environ.get('MWDICT_KEY')}
        r = requests.get(
            f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{urllib.parse.quote_plus(word)}",
            params=k)
        r.raise_for_status()
    except requests.RequestException:
        return None

    try:
        defined_word = r.json()
        return defined_word
    except ValueError:
        return None



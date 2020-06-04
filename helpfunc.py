import os
import requests

from flask import redirect, render_template, request, session
from functools import wraps


# writing this for later to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

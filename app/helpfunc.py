
import os
import requests
import string
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
        j = r.json()
        return j
    except ValueError:
        return None


# Takes a list (partial dict from API call) and constructs a link to the audio file.
# Per https://dictionaryapi.com/products/json#sec-2
def audio_url(aud_list):
    nlist = []
    for sound in aud_list:
        # Not all items in list have the sound key, wrapped in try catch to fix this
        try:
            x = sound['sound']['audio'][0]
            if x.isdigit() or x in string.punctuation:
                sub = "number"
            elif x == "b":
                sub = "bix"
            elif x == "g":
                sub = "gg"
            else:
                sub = x
            aud_url = f"https://media.merriam-webster.com/audio/prons/en/us/mp3/{sub}/{sound['sound']['audio']}.mp3"
            nlist.append(aud_url)
        except KeyError:
            pass
    return nlist



# Not finished but
# ------------
# strip_fix takes in the list returned from API call and converts it into something a little easier for me to use
# with the application. Should hopefully keep the routes.py & lookup.html from doing to much parsing
# Each object has the following properties:
    # shortdef, a short definition (some words don't have one so it ends up an empty list)
    # head, one or more "headwords" which are similar words or more words to give context
    # stems, a list of stem words, usually pluralized or conjugated versions of headword
# Optionally, each word may have 0 or more of the following:
    # audio, a link to a pronunciation of the word
    # quotes, a list of one or more objs with: quote itself, year, publication, author
# ------------


def strip_fix(list_words=None):

    if list_words is None:
        list_words = "Nothing Found"
        return list_words
    else:
        fixed_list = []
        for item in list_words:
            new_item = {"shortdef": item["shortdef"], "head": item["hwi"]["hw"], "stems": item["meta"]["stems"]}
            try:
                new_item["audio"] = audio_url(item["hwi"]["prs"])
                new_item["quotes"] = item["quotes"]
            except KeyError as e:
                print(f"the key [{e}] was not found for this entry")
                pass
            fixed_list.append(new_item)

        for x in fixed_list:
            print(x)

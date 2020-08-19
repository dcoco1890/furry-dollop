import itertools
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
            # Had to add checks for ix in bix and the second g in gg because words that started with b or g were
            # not working. Looking back it was silly to only check the first letter
            elif x == "b" and sound['sound']['audio'][1] == 'i' and sound['sound']['audio'][2] == 'x':
                sub = "bix"
            elif x == "g" and sound['sound']['audio'][1] == 'g':
                sub = "gg"
            else:
                sub = x
            aud_url = f"https://media.merriam-webster.com/audio/prons/en/us/mp3/{sub}/{sound['sound']['audio']}.mp3"
            nlist.append(aud_url)
        except KeyError:
            pass
    return nlist

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
            try:
                new_item = dict(shortdef=item["shortdef"], head=item["hwi"]["hw"], stems=item["meta"]["stems"],
                                speechpart=item['fl'])
                if "quotes" in item:
                    new_item["quotes"] = item["quotes"]
                if "hom" in item:
                    new_item["homnum"] = str(item["hom"])
                try:
                    new_item["audio"] = audio_url(item["hwi"]["prs"])
                except KeyError:
                    pass
                for i in item['def']:
                    flatboi = list(itertools.chain(*i['sseq']))
                    for j in flatboi:
                        print(j[1]['dt'][0][1])
                        try:
                            print(j[1]['sdsense'])
                        except KeyError:
                            pass
                print("____________")
                fixed_list.append(new_item)
            except TypeError as e:
                print(f"{e}")
                return None
        for thing in fixed_list:
            print(thing)

        return fixed_list



# def json_extract(obj, key):
#     """Recursively fetch values from nested JSON."""
#     arr = []
#
#     def extract(obj, arr, key):
#         """Recursively search for values of key in JSON tree."""
#         if isinstance(obj, dict):
#             for k, v in obj.items():
#                 if k == key and isinstance(v, list):
#                     narr = []
#                     for item in v:
#                         narr.append(item)
#                     arr.append(narr)
#                 if isinstance(v, (dict, list)):
#                     extract(v, arr, key)
#                 elif k == key:
#                     print("______________________")
#                     print(k, v)
#                     arr.append(v)
#         elif isinstance(obj, list):
#             for item in obj:
#                 extract(item, arr, key)
#         return arr
#
#     values = extract(obj, arr, key)
#     return values

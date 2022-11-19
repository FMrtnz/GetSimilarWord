from flask import Flask,redirect,render_template,request,url_for
import pandas as pd

# Module to get levenshtein distance
import nltk
# Module to translate
#from deep_translator import GoogleTranslator
import translators as ts

# Get list of languages available on Google Translate
df_lang = pd.DataFrame.from_dict({'code_lang': {0: 'af', 1: 'sq', 2: 'am', 3: 'ar', 4: 'hy', 5: 'az', 6: 'eu', 7: 'be', 8: 'bn', 9: 'bs', 10: 'bg', 11: 'ca', 12: 'ceb', 13: 'ny', 14: 'co', 15: 'hr', 16: 'cs', 17: 'da', 18: 'nl', 19: 'en', 20: 'eo', 21: 'et', 22: 'tl', 23: 'fi', 24: 'fr', 25: 'fy', 26: 'gl', 27: 'ka', 28: 'de', 29: 'el', 30: 'gu', 31: 'ht', 32: 'ha', 34: 'iw', 35: 'hi', 36: 'hmn', 37: 'hu', 38: 'is', 39: 'ig', 40: 'id', 42: 'it', 43: 'ja', 44: 'jw', 45: 'kn', 46: 'kk', 47: 'km', 48: 'ko', 49: 'ku', 50: 'ky', 51: 'lo', 53: 'lv', 54: 'lt', 55: 'lb', 56: 'mk', 57: 'mg', 58: 'ms', 59: 'ml', 61: 'mi', 62: 'mr', 63: 'mn', 64: 'my', 65: 'ne', 66: 'no', 67: 'ps', 68: 'fa', 69: 'pl', 70: 'pt', 71: 'pa', 72: 'ro', 73: 'ru', 74: 'sm', 75: 'gd', 76: 'sr', 77: 'st', 78: 'sn', 79: 'sd', 80: 'si', 81: 'sk', 82: 'sl', 83: 'so', 84: 'es', 85: 'su', 86: 'sw', 87: 'sv', 88: 'tg', 89: 'ta', 91: 'th', 92: 'tr', 93: 'uk', 94: 'ur', 95: 'uz', 96: 'vi', 97: 'cy', 98: 'xh', 99: 'yi', 100: 'yo', 101: 'zu'}, 'language': {0: 'afrikaans', 1: 'albanian', 2: 'amharic', 3: 'arabic', 4: 'armenian', 5: 'azerbaijani', 6: 'basque', 7: 'belarusian', 8: 'bengali', 9: 'bosnian', 10: 'bulgarian', 11: 'catalan', 12: 'cebuano', 13: 'chichewa', 14: 'corsican', 15: 'croatian', 16: 'czech', 17: 'danish', 18: 'dutch', 19: 'english', 20: 'esperanto', 21: 'estonian', 22: 'filipino', 23: 'finnish', 24: 'french', 25: 'frisian', 26: 'galician', 27: 'georgian', 28: 'german', 29: 'greek', 30: 'gujarati', 31: 'haitian creole', 32: 'hausa', 34: 'hebrew', 35: 'hindi', 36: 'hmong', 37: 'hungarian', 38: 'icelandic', 39: 'igbo', 40: 'indonesian', 42: 'italian', 43: 'japanese', 44: 'javanese', 45: 'kannada', 46: 'kazakh', 47: 'khmer', 48: 'korean', 49: 'kurdish (kurmanji)', 50: 'kyrgyz', 51: 'lao', 53: 'latvian', 54: 'lithuanian', 55: 'luxembourgish', 56: 'macedonian', 57: 'malagasy', 58: 'malay', 59: 'malayalam', 61: 'maori', 62: 'marathi', 63: 'mongolian', 64: 'myanmar (burmese)', 65: 'nepali', 66: 'norwegian', 67: 'pashto', 68: 'persian', 69: 'polish', 70: 'portuguese', 71: 'punjabi', 72: 'romanian', 73: 'russian', 74: 'samoan', 75: 'scots gaelic', 76: 'serbian', 77: 'sesotho', 78: 'shona', 79: 'sindhi', 80: 'sinhala', 81: 'slovak', 82: 'slovenian', 83: 'somali', 84: 'spanish', 85: 'sundanese', 86: 'swahili', 87: 'swedish', 88: 'tajik', 89: 'tamil', 91: 'thai', 92: 'turkish', 93: 'ukrainian', 94: 'urdu', 95: 'uzbek', 96: 'vietnamese', 97: 'welsh', 98: 'xhosa', 99: 'yiddish', 100: 'yoruba',
  101: 'zulu'}})

app = Flask(__name__)

@app.route("/")
def main():
    opt_param = request.args.get("txt")
    if opt_param == "load_file":
      df = pd.read_csv("results.csv")
      txt = df[["language", "translation"]].to_html(classes='table  ', header="true")
    else:
      txt = ""
    return render_template('index.html', x=txt)

@app.route('/find_translation', methods=['POST', 'GET'])
def find_translation():
    if request.method == 'POST':
      word_input = request.form['word_input']
      return redirect(url_for('main', txt=find_synonyme(word_input)))
    else:
       word_input = request.args.get('word_input')
       return redirect(url_for('main', txt=find_synonyme(word_input)))

def find_synonyme(word):
  # Apply to the table a translation with the input
  df_lang["translation"] = df_lang["code_lang"].apply(lambda code: ts.google(word, to_language=code) )
  # 
  # Apply levensthein distance to get the most close word
  df_lang["distance"] = df_lang["translation"].apply(lambda x: nltk.edit_distance(word, x))
  # Get the 20 most similar words and the language
  html_str = df_lang.sort_values("distance").head(10).to_csv("results.csv")
  return "load_file"


app.run(host='0.0.0.0', port=5000, debug=True)
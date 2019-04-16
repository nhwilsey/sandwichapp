#app.py

from flask import Flask, render_template, request, jsonify
from PIL import Image, ImageDraw, ImageFont
from subprocess import Popen, PIPE
import time
import json
import os
import time
app = Flask(__name__)
sandwich_list = []
current_sandwich = []
with open('data.txt') as json_file:  
    data = json.load(json_file)

def get_printer_address():
    process = Popen(['brother_ql', '-b', 'pyusb', 'discover'], stdout=PIPE, stderr=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    
    if exit_code != 0:
        print(err)
    
    return output.decode()

os.environ['BROTHER_QL_MODEL'] = 'QL-810W'
os.environ['BROTHER_QL_PRINTER'] = get_printer_address()

@app.route('/query-example')
def query_example():
    language = request.args.get('language') #if key doesn't exist, returns None
    framework = request.args['framework'] #if key doesn't exist, returns a 400, bad request error
    website = request.args.get('website')

    return '''<h1>The language value is: {}</h1>
              <h1>The framework value is: {}</h1>
              <h1>The website value is: {}'''.format(language, framework, website)


@app.route('/form-example', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        language = request.form.get('language')
        framework = request.form['framework'] #they do both the same thing

        return '''<h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)

    return '''<form method="POST">
                  Language: <input type="text" name="language"><br>
                  Framework: <input type="text" name="framework"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

@app.route('/json-example', methods=['POST']) #GET requests will be blocked
def json_example():
    req_data = request.get_json()
    with open('data.txt') as json_file:  
        data = json.load(json_file)

    # language = None
    # if 'language' in req_data:
    #     language = req_data['language']
    name = req_data['NAME']
    date = req_data['DATE']
    pin = req_data['PIN']
    bread = req_data['BREAD']
    meat = req_data['MEAT']
    cheese = req_data['CHEESE'] #two keys are needed because of the nested object
    condiments = req_data['CONDIMENTS'] #an index is needed because of the array
    extras = req_data['EXTRAS']
    
    img = Image.open("/home/pi/sandorderrrr.png")
 
    fnt = ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-Medium.ttf', 33)
    d = ImageDraw.Draw(img)
    d.text((230,155), name, font=fnt, fill=(0,0,0))
    d.text((210,255), date, font=fnt, fill=(0,0,0))
    d.text((530,253), pin, font=fnt, fill=(0,0,0))
    d.text((230,332), bread, font=fnt, fill=(0,0,0))
    d.text((225,410), meat, font=fnt, fill=(0,0,0))
    d.text((258,495), cheese, font=fnt, fill=(0,0,0))
    d.text((90,650), condiments, font=fnt, fill=(0,0,0))
    d.text((235,775), extras, font=fnt, fill=(0,0,0))

 
    img.save('pil_text.png')
    
    time.sleep(1)

    cmd = 'brother_ql print -l 62 --red pil_text.png'
    
    exit_code = os.system(cmd)

    print(exit_code)

    if exit_code != 0:
        print("HELP")

    current_sandwich = [meat,bread,cheese,condiments,extras]
    sandwich_list.append(current_sandwich)
    print(sandwich_list)
    
    data['people'].append({  
        'meat': meat,
        'bread': bread,
        'cheese': cheese,
        'condiments':condiments,
        'extras':extras
    })

    print("gotem")
    
    
    with open('data.txt', 'w') as outfile:  
        json.dump(data, outfile)
    print("done")

    return '''

           The meat is: {}
           The bread is: {}
           The cheese is: {}
           The condiments are: {}
           The extras are: {}
           All of em are {}'''.format(meat, bread, cheese, condiments, extras, data)



if __name__ == '__main__':
    app.run(host= '0.0.0.0') #run app in debug mode on port 5000 // remove for localhost


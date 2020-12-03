from flask import Flask, jsonify, request
from datetime import datetime
import json
import base64

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

def read_file():
    f = open("db.json","r")
    db = json.load(f)
    main_db = []
    for member in db['main']:
        main_db.append(member)
    
    return main_db
    
def write_file(main_db):   
    main = {}
    main['main'] = []
    for member in main_db:
        main['main'].append(member)
    with open('db.json','w') as f:
        json.dump(main,f,indent = 2)   


@app.route('/info/all', methods=['GET'])
def get_db():
    db = read_file()
    return jsonify(db)
    
@app.route('/info/lights', methods=['GET'])
def get_lights():
    db = read_file()
    lights=[]
    for member in db:
        if member['name'] == 'lvLight':
            lights.append(member)
        elif member['name'] == 'bedLight':
            lights.append(member)
    return jsonify(lights)
    
@app.route('/info/thermistor', methods=['GET'])
def get_thermistor():
    db = read_file()
    thermistor = None
    for member in db:
        if member['name'] == 'thermistor':
            thermistor = member
    return jsonify(thermistor)
    
@app.route('/info/security', methods=['GET'])
def get_security():
    db = read_file()
    security=[]
    for member in db:
        if member['name'] == 'haveKey':
            security.append(member)
        elif member['name'] == 'noKey':
            security.append(member)
    return jsonify(security)
    
@app.route('/info/security/keys', methods=['GET'])
def get_security_key():
    db = read_file()
    security=[]
    for member in db:
        if member['name'] == 'keys':
            for key in member['value']:
                security.append(key)
    return jsonify(security)
    
@app.route('/info/security/keys', methods=['POST'])
def post_keys():
    db = read_file()       
    security=[]
    for member in db:
        if member['name'] == 'keys':
            for key in member['value']:
                security.append(key)
    if not request.json or not 'key' in request.json:
        abort(400)
    new_key = {
        'id': security[-1]['id'] + 1,
        'key': request.json['key']
    }
    security.append(new_key)
    for member in db:
        if member['name'] == 'keys':
            member['value'] = security
    write_file(db)
    return jsonify({'status':'ok'})   
    
@app.route('/info/security/keys', methods=['DELETE'])
def delete_key():
    del_key = request.json['key']
    db = read_file()       
    security=[]
    for member in db:
        if member['name'] == 'keys':
            for key in member['value']:
                if key['key'] != del_key:
                    security.append(key)
    return jsonify({'deleted': True})
    
@app.route('/info/images/<int:id>', methods=['GET'])
def get_images(id):
    #store images in base64
    f = open("images.json","r")
    db = json.load(f)
    images= []
    for member in db['images']:
        images.append(member)
    
    output = None
    for image in images:
        if image['id'] == id:
            output = image
    
    return jsonify(output)
    
@app.route('/info/images', methods=['POST'])
def send_images():
    #store images in base64
    f = open("images.json","r")
    db = json.load(f)
    images= []
    for member in db['images']:
        images.append(member)
    current = datetime.now().strftime('%Y-%m-%d %H:%M')
    new_image = {
        'id' : images[-1]['id']+1,
        'image': request.json['image'],
        'time': current
    }
    images.append(new_image)
    
    main = {}
    main['images'] = []
    for member in images:
        main['images'].append(member)
    with open('images.json','w') as f:
        json.dump(main,f,indent = 2)
    
    return jsonify({'status':'ok'})
    
@app.route('/info/lights', methods=['POST'])
def post_lights():
    db = read_file()       
    if not request.json or not 'name' in request.json:
        abort(400)
    new_member = {
        'id': db[-1]['id'] + 1,
        'name': request.json['name'],
        'value': False
    }
    db.append(new_member)
    write_file(db)
    return jsonify({'status':'ok'})    
    
@app.route('/info/security/<string:feature>', methods=['PUT'])
def update_security_db(feature):
    db = read_file()
    temp = False
    for member in db:
        if member['name'] == feature:
            if member['value'] == False:
                temp = True
            member['value'] = temp
    write_file(db)
    return jsonify(db)
    
@app.route('/info/thermistor', methods=['PUT'])  
def update_temp_db():
    if not request.json:
        abort(400)
    db = read_file()
    
    if 'temp' in request.json and type(request.json['temp']) != int:
        abort(400)
    
    temp = db[0]
    temp['value'] = request.json.get('temp')
    db[0] = temp
    write_file(db)
    return jsonify({'db': db})
    
@app.route('/info/lights/<string:name>', methods=['PUT'])  
def update_lights_db(name):
    db = read_file()  
    temp = True
    for member in db:
        if member['name'] == name:
            if member['value'] == True:
                temp = False
            member['value'] = temp
            
    write_file(db)
    return jsonify({'db': db})

    
if __name__ == '__main__':
    app.run(debug=True)
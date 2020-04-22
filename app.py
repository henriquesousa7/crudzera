from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()

db = client['testEPI']

@app.route('/get_data', methods=['GET'])
def get():
    data = db.people.find()
    result = []
    for value in data:
        result.append({'name':value['name'], 'age':value['age'], 'gender':value['gender']})

    return jsonify(result)

@app.route('/get_databyname/<string:name>', methods=['GET'])
def get_databyname(name):
    data = db.people.find()
    output = []
    for person in data:
        if person['name'].upper() == name.upper():
            output.append({'name':person['name'], 'age':person['age'], 'gender':person['gender']}) 
    return jsonify(output)

@app.route('/set_data', methods=['POST', 'GET'])
def set_data():
    if request.method == 'POST':
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]

        return redirect(url_for('send', name=name, age=age, gender=gender))
    else:

        return render_template('form.html')

@app.route('/send/<name>&<age>&<gender>', methods=['POST'])
def send(name, age, gender):
        
    values = {'name':name, 'age':age, 'gender':gender}

    post_id = db.people.insertOne(values).inserted_id

    return jsonify(post_id)


if __name__ == '__main__':
    app.run(debug=True)

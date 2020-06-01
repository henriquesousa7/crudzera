from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()

db = client['testCRUD']

@app.route('/')
def index():
    return '<h1>by henriquesousa7 on github</h1>'

@app.route('/get_data', methods=['GET'])
def get():
    data = db.users.find()
    result = []
    for value in data:
        result.append({'name':value['name'], 'age':value['age'], 'gender':value['gender']})

    return jsonify(result)

@app.route('/set_data', methods=['POST', 'GET'])
def set_data():
    if request.method == 'POST':
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]

        return redirect(url_for('send_info', name=name, age=age, gender=gender))
    else:
        return render_template('form.html')

@app.route('/sendInfo/<name>&<age>&<gender>', methods=['GET','POST'])
def send_info(name, age, gender):
        
    values = {'name':name, 'age':age, 'gender':gender}

    db.users.insert(values)
    
    return '<h1>User added</h1>'

@app.route('/remove_data', methods=['GET','POST'])
def remove():
    if request.method == 'POST':
        name_remove = request.form['name_remove']
        age_remove = request.form['age_remove']
        return redirect(url_for('remove_info', name_remove=name_remove, age_remove=age_remove))
    else:
        return render_template('remove.html')

@app.route('/removeInfo/<name_remove>&<age_remove>', methods=['GET','POST'])
def remove_info(name_remove, age_remove):

    values_remove = {'name':name_remove, 'age':age_remove}
    db.users.remove(values_remove)
    
    return '<h1>User removed</h1>'



if __name__ == '__main__':
    app.run(debug=True)

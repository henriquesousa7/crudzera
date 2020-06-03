from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()

db = client['testCRUD']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        data = db.users.find()
        result = []
        for value in data:
            result.append({'name':value['name'], 'age':value['age'], 'gender':value['gender']})

        return jsonify(result)
    except Exception as exc:

        error = [{'Error': str(exc)}]
        return jsonify(error)

@app.route('/set_data', methods=['POST', 'GET'])
def set_data():
    if request.method == 'POST':
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]

        return redirect(url_for('set_info', name=name, age=age, gender=gender))
    else:
        return render_template('form.html')

@app.route('/setInfo/<name>&<age>&<gender>', methods=['GET','POST'])
def set_info(name, age, gender):
    try:

        values = {'name':name, 'age':age, 'gender':gender}

        db.users.insert_one(values).inserted_id
        
        return 'Sucess'

    except Exception as exc:
        error = [{'Error': str(exc)}]
        return jsonify(error)

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
    try:

        values_remove = {'name':name_remove, 'age':age_remove}
        msg = db.users.remove(values_remove)
        return jsonify(msg)

    except Exception as exc:

        error = [{'Error': str(exc)}]
        return jsonify(error)

@app.route('/search_data', methods=['GET','POST'])
def search_data():
    if request.method == 'POST':
      data = db.users.find()
      name = request.form["name"]
      age = request.form["age"]
      gender = request.form["gender"]
      for x in data:
          if x['name'].upper() == name.upper() and x['age'] == age and x['gender'].upper() == gender.upper():
              return redirect(url_for('update_data', name_update=name, age_update=age, gender_update=gender))
        
    else:
        return render_template('searchdata.html')

@app.route('/update_data/<name_update>&<age_update>&<gender_update>', methods=['GET','POST'])
def update_data(name_update, age_update, gender_update):
    if request.method == 'POST':
        new_name = request.form['new_name']
        new_age = request.form['new_age']
        new_gender = request.form['new_gender']
        
        try:

            old_data = {'name':name_update, 'age':age_update, 'gender':gender_update}
            new_data = {'name':new_name, 'age':new_age, 'gender':new_gender}

            msg = db.users.update(old_data,{"$set":new_data})
        
            return jsonify(msg)

        except Exception as exc:
            
            error = [{'Error': str(exc)}]
            return jsonify(error)

    else:
        return render_template('update.html')

if __name__ == '__main__':
    app.run(debug=True)

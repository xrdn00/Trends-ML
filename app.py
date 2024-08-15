from flask import Flask, render_template, request,redirect,url_for
import pandas as pd
from sklearn.tree import DecisionTreeClassifier


app = Flask(__name__)

dataset = []



@app.route("/", methods=['GET', 'POST'])
def index():
    sentences=[]
    dataset.clear()
    n=0
    sx = 0

    if request.method == 'POST':
        filename = request.files['filename']
        age = int(request.form['age'])  # Convert age to int

        sex = request.form['sex']
        sx = 1 if sex == "male" else 0  # Convert sex to int
        print(filename)
        

        extract = str(filename).split("'")[1]
        print(extract)
        if extract == '':

            return redirect(url_for('index'))
        
        data = pd.read_csv(extract)
        features = data.drop(columns=["food", "clothes","games"])
        food_data = data["food"]
        clothe_data = data["clothes"]
        game_data = data["games"]

        model1 = DecisionTreeClassifier()
        model1.fit(features.values, food_data)
        print(data.columns)
        model2 = DecisionTreeClassifier()
        model2.fit(features.values, clothe_data)

        model3 = DecisionTreeClassifier()
        model3.fit(features.values, game_data)

        food = model1.predict([[age,sx]]) 
        clothe = model2.predict([[age,sx]])
        game = model3.predict([[age,sx]])
    
        dataset.append(str(food))
        dataset.append(str(clothe))
        dataset.append(str(game))
        dataset.append(str(age))
        dataset.append(str(sex))
        sentences = ["{} are the most popular choice in foods category for {}s ages {} years old.".format(dataset[0],dataset[4],dataset[3]),"{} is the most bought product in clothing category for {}s ages {} years old.".format(dataset[1],dataset[4],dataset[3]),"{} is the most played game for games category for {}s ages {} years old.".format(dataset[2],dataset[4],dataset[3])]

        
    else:
        print("Invalid filename or file does not exist.")
        

    return render_template("index.html",extracted_data = sentences,data = dataset)

if __name__ == "__main__":
    app.run(debug=True)

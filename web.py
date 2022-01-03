from flask import Flask,render_template,request
from urllib.parse import parse_qsl
import os
import main

app=Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/test',methods=['POST'])
def test():
    if request.method == 'POST':
        main.Init()
        return "OK"

@app.route('/predict',methods=['POST'])
def Predict():
    if request.method == 'POST':
        mode=request.form['mode']
        input=request.form['input']
        result=main.Predict(mode,input)
        return result


if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(port=port)
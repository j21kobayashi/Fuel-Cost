from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'input_value1' in request.form and 'input_value2' in request.form and 'input_value3' in request.form and 'input_value4' in request.form:
            input_value1 = request.form['input_value1']
            input_value2 = request.form['input_value2']
            input_value3 = request.form['input_value3']
            input_value4 = request.form['input_value4'] 
            result2 = calculate2([input_value1, input_value2, input_value3, input_value4])
            return render_template('index.html', result=result2)
    return render_template('index.html',result=111)

def i_or_f(x):
    if x %1==0:
        x=int(x)
    return x

def nfm3(y):
    return'{:,}'.format(i_or_f(y))

def calculate2(x):
    try:
        for i in range(len(x)):
            x[i]=i_or_f(float(x[i]))
        cost=x[1]*x[3]/x[2]
        result2=[f"{x[0]}人,単価{x[1]}円/L,燃費{x[2]}km/L,走行距離{x[3]}km"]
        result2.append(f"⇒総額{nfm3(round(cost))}円 , {x[0]}人で割ると1人当たり{nfm3(round(cost/float(x[0]),1))}円 ")
    except:
        result2 = ["計算エラーが発生しました","すべての項目を数値で入力してください"]
    return result2

if __name__ == '__main__':
    app.run(debug=True)

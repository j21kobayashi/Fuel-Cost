from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
import datetime

# # #ユーザーエージェント（2022/07現在Yahooファイナンスではなくても動きます。）
# user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'
# header = {'User-Agent': user_agent}
# # #サイトからデータを取得
# url = "https://info.finance.yahoo.co.jp/fx/detail/?code=USDJPY=FX"
# r = requests.get(url,headers=header)
# # #現在時刻を取得（本書のサンプルコードを使用）
# now = datetime.datetime.now()
# now_19 = "{0.year}年{0.month}月{0.day}日{0.hour}時{0.minute}分".format(now)
# # #サイトから取得したデータから必要な部分を抽出
# soup = BeautifulSoup(r.text, 'html.parser')
# yen_price = soup.find('span', class_='_3Pvw_N8d').text
# # print(now_19 + '：ドル円レート')
# # print(yen_price + '円')

# サイトからデータを取得
url = "https://info.finance.yahoo.co.jp/fx/detail/?code=USDJPY=FX"
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'
header = {'User-Agent': user_agent}
r = requests.get(url, headers=header)
# 現在時刻を取得（本書のサンプルコードを使用）
now = datetime.datetime.now()
now_19 = "{0.year}年{0.month}月{0.day}日{0.hour}時{0.minute}分".format(now)
# サイトから取得したデータから必要な部分を抽出
soup = BeautifulSoup(r.text, 'html.parser')
yen_price = soup.find('span', class_='_3Pvw_N8d')#.text
if type(yen_price != str):
    yen_price=str(yen_price)[24:27]+str(yen_price)[35:36]+str(yen_price)[60:62]+str(yen_price)[69:70]

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    
    
    if request.method == 'POST':
        if 'input_value' in request.form:
            input_value = request.form['input_value']
            result1 = calculate1(input_value)
            return render_template('index.html', result1=result1)

        elif 'input_value1' in request.form and 'input_value2' in request.form and 'input_value3' in request.form:
            input_value1 = request.form['input_value1']
            input_value2 = request.form['input_value2']
            input_value3 = request.form['input_value3']
            result2 = calculate2(input_value1, input_value2, input_value3)
            return render_template('index.html', result2=result2)

    return render_template('index.html')

#Kさんに共通する変数設定
py_rate=float(yen_price) #1ポンド当たりの日本円を以下に入力
gp_rate=174000000/34000872#1ガリオンあたりのポンドを以下に入力(幻の動物とその生息地から引用)
gs=17   #ガリオン-シックル為替
sk=29   #シックル-クヌート為替

def calculate1(input_value):
    try:
        # 機能①の計算処理を実装
        input_value=eval(input_value)
        p=float(input_value)/py_rate
        g=p/gp_rate
        s=g*gs
        k=sk*s
        s=k//sk
        g=s//gs
        s=s%gs
        k=k%sk

        if k%1!=0:
            k=f"{nfm3(int(k))}〜{nfm3(int(k+1))}"
    #    result1=f"{input_value} 円 ⇨ {round(g)}ガリオン  {round(s)}シックル  {round(k)}クヌート"
        result1=f"{nfm3(input_value)} 円 ⇨ {nfm3(int(g))}ガリオン  {nfm3(int(s))}シックル  {(k)}クヌート"
        #result1 = f"機能①の計算結果: {input_value}"  # 仮の計算結果
    except:
        result1 = "計算エラーが発生しました"  
    return result1

def i_or_f(x):
    if x %1==0:
        x=int(x)
    return x

def nfm3(y):
    return'{:,}'.format(i_or_f(y))

def calculate2(g, s, k):
    try:
        g=i_or_f(float(g))
        s=i_or_f(float(s))
        k=i_or_f(float(k))

        tmp_g=g
        g=g+(s/gs)+(k/(gs*sk))
        p=g*gp_rate
        y=p*py_rate
        if y%1!=0:
            y=f"{nfm3(int(y))}〜{nfm3(int(y+1))}"
        else:
            y=nfm3(y)

        # 機能②の計算処理を実装
        result2 = f" {nfm3(tmp_g)} ガリオン  {nfm3(s)} シックル  {nfm3(k)} クヌート  ⇨ {(y)} 円"  # 仮の計算結果
    #    result2 = f" {round(g1)} ガリオン  {round(s)} シックル  {round(k)} クヌート  ⇨ {round(y)} 円"  # 仮の計算結果
    except:
        result2 = "計算エラーが発生しました"
    return result2

def format_result(result):
    if '~' in result:
        parts = result.split('~')
        return f"{parts[0]}<br>{parts[1]}"
    return result

if __name__ == '__main__':
    app.run(debug=True)




# from flask import Flask, render_template, request

# app = Flask(__name__)


# @app.route('/', methods=['GET', 'POST'])

# def home():
    
#     if request.method == 'POST':
#         if 'input_value1' in request.form and 'input_value2' in request.form and 'input_value3' in request.form and 'input_value4' in request.form:
#             result=[1,2]
#             return render_template('index.html', result=result)
#     return render_template('index.html')



# if __name__ == '__main__':
#     app.run(debug=True)













# # @app.route('/', methods=['GET', 'POST'])

# # def home():
    
# #     if request.method == 'POST':
# #         if 'input_value1' in request.form and 'input_value2' in request.form and 'input_value3' in request.form and 'input_value4' in request.form:
# #             # input_value1 = request.form['input_value1']
# #             # input_value2 = request.form['input_value2']
# #             # input_value3 = request.form['input_value3']
# #             # input_value4 = request.form['input_value4']
# #             # result = calculate(input_value1, input_value2, input_value3, input_value4)
# #             result=[1,2]
# #             return render_template('index.html', result=result)
# #         return render_template('index.html')


# # # def calculate(a,b,c,d):
# # #     result1=[]
# # #     try:
# # #         # 機能①の計算処理を実装
# # #         x=1
# # #         x=(float(d)*float(b)/float(c))
# # #         result1.append(f" ガソリン単価{b}(円/L) , 燃費{c}(km/L) ,走行距離{d}(km)" )
# # #         result1.append(f"⇒総額{round(x)}円 , {a}人で割ると1人当たり{round(x/float(a))}円 ")
# # # #        result1 = f"⇒総額{round(x)}円 , {a}人で割ると1人当たり{round(x/float(a))}円 "
# # #     except:
# # #         result1.append("計算エラーが発生しました")  
# # # #        result1 ="計算エラーが発生しました"

# # #     return result1

# # if __name__ == '__main__':
# #     app.run(debug=True)

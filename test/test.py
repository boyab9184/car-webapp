
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def student():
   return render_template('index2.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':

   
    result ='Hello world'
    return result


if __name__ == '__main__':
   app.run(debug = True)
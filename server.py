from waitress import serve
from flask import Flask
from concurrent.futures import thread
app=Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World'


mode='dev'

if __name__ == '__main__':
    # if mode=='dev':
    #     app.run(host='0.0.0.0', port=50100, debug=True)
    # else:
    serve(app, host='0.0.0.0', port='50100', thread=2, url_prefix="/my-app")

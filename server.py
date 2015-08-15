from flask import Flask
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mylatestserver'

@app.route('/')
def main():
    return "Shubham"

some = {
  "data": [
    {
      "name": "The name is",
      "url": "Get the song",
      "image": "So here is the image as well"
    },
    {
      "name": "The name this time is",
      "url": "Get the song",
      "image": "So here is the image as well"
    }
  ]
}

@app.route('/users/shubham')
def user():
    return json.dumps(some)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

import copy
from flask import Flask, request, url_for, send_file
import json
import apiclient
import os

from apiclient.discovery import build
from apiclient.errors import HttpError
#from oauth2client.tools import argparser
import argparse

DEVELOPER_KEY = 'AIzaSyBcYKu5TcSDF9yxQEmydlN1Ax9BMb0jmxk'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = 'mylatestserver'


def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options.q,
        part="id,snippet",
        maxResults=options.max_results
    ).execute()

    #print type(search_response)

    data = {}
    data['data'] = []

    for i in search_response['items']:
        filler = {
            'image': i['snippet']['thumbnails']['medium']['url'],
            'name': i['snippet']['title'],
            #'id': i['id']['videoId'],
            'url': 'Link mein kya rakha h?'
        }

        try:
            filler['id'] = i['id']['videoId']
            data['data'].append(copy.deepcopy(filler))
        except:
            pass

    return json.dumps(data)


def run(query='None'):
    parse = argparse.ArgumentParser()
    parse.add_argument("--q", help="Search term", default=query)
    parse.add_argument("--max-results", help="Max results", default=25)
    args = parse.parse_args()

    try:
        return youtube_search(args)
    except HttpError, e:
        return some


@app.route('/')
def main():
    return run('Thinking out loud')
    #return "Shubham"

some = {
    "data": [
        {
            "name": "The name is",
            "url": "Get the song",
            "image": "So here is the image as well",
            "id": "Video_ID"
        }
    ]
}


@app.route('/api/search', methods=['GET'])
def search():
    return run(query=str(request.args.get('query')))


@app.route('/api/download', methods=['GET'])
def download():
    try:
        os.system('youtube-dl https://www.youtube.com/watch?v=' + str(request.args.get('id') + ' -o "./static/%(title)s.%(ext)s" --extract-audio --audio-format mp3'))
        name = request.args.get('name')
        id_file = request.args.get('id')
        print "Downloaded and sent to the client"
        return json.dumps({"url": "http://localhost:8080/api/download/music?id="+str(id_file)+"&name="+ str(name)})

    except:
        name = request.args.get('name')
        print name
        id_file = request.args.get('id')
        print "sent"
        return json.dumps({"url": "http://localhost:8080/api/download/music?id="+str(id_file)+"&name="+ str(name)})


@app.route('/api/download/music', methods=['GET'])
def downloadMusic():
    try:
        name = request.args.get('name')
        #print name
        id_file = request.args.get('id')
        print "sent"
        return send_file('static/'+str(name)+'.mp3', mimetype='audio/mp3')
    except:
        #os.system('youtube-dl https://www.youtube.com/watch?v=' + str(request.args.get('id') + ' -o "./static/%(title)s.%(ext)s" --extract-audio --audio-format mp3'))
        name = request.args.get('name')
        return send_file('static/'+str(name)+'.mp3', mimetype='audio/mp3')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

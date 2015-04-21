#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'jibarish':
        return 'foo'
    return None


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


songs = [
    {
        'id':       1,
        'title':    u'Brown-Eyed Girl',
        'artist':   u'Van Morrison', 
        'key':      u'G', 
        'lyrics':   u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done':     True
    },
    {
        'id':       2,
        'title':    u'Fountain of Sorrow',
        'artist':   u'Jackson Browne', 
        'key':      u'G', 
        'lyrics':   u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done':     True
    }
]


def make_public_song(song):
    new_song = {}
    for field in song:
        if field == 'id':
            new_song['uri'] = url_for('get_song', song_id=song['id'], _external=True)
        else:
            new_song[field] = song[field]
    return new_song


@app.route('/shalaladida/api/v1.0/songs', methods=['GET'])
@auth.login_required
def get_songs():
    return jsonify({'songs': [make_public_song(song) for song in songs]})


@app.route('/shalaladida/api/v1.0/songs/<int:song_id>', methods=['GET'])
@auth.login_required
def get_song(song_id):
    song = [song for song in songs if song['id'] == song_id]
    if len(song) == 0:
        abort(404)
    return jsonify({'song': make_public_song(song[0])})


@app.route('/shalaladida/api/v1.0/songs', methods=['POST'])
@auth.login_required
def create_song():
    if not request.json or not 'title' in request.json:
        abort(400)
    song = {
        'id':       songs[-1]['id'] + 1,
        'title':    request.json['title'],
        'artist':   request.json['artist'],
        'key':      request.json['key'],
        'lyrics':   request.json.get('lyrics', ""), # tolerate missing lyrics field
        'done':     False
    }
    songs.append(song)
    return jsonify({'song': make_public_song(song)}), 201


@app.route('/shalaladida/api/v1.0/songs/<int:song_id>', methods=['PUT'])
@auth.login_required
def update_song(song_id):
    song = [song for song in songs if song['id'] == song_id]
    if len(song) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'artist' in request.json and type(request.json['artist']) != unicode:
        abort(400)
    if 'key' in request.json and type(request.json['key']) != unicode:
        abort(400)                
    if 'lyrics' in request.json and type(request.json['lyrics']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    song[0]['title'] = request.json.get('title', song[0]['title'])
    song[0]['artist'] = request.json.get('artist', song[0]['artist'])
    song[0]['key'] = request.json.get('key', song[0]['key'])
    song[0]['lyrics'] = request.json.get('lyrics', song[0]['lyrics'])
    song[0]['done'] = request.json.get('done', song[0]['done'])
    return jsonify({'song': make_public_song(song[0])})


@app.route('/shalaladida/api/v1.0/songs/<int:song_id>', methods=['DELETE'])
@auth.login_required
def delete_song(song_id):
    song = [song for song in songs if song['id'] == song_id]
    if len(song) == 0:
        abort(404)
    songs.remove(song[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)

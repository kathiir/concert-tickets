from flask import Flask, request, make_response, jsonify, abort
import os
from config import app
from models import Concert



@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/artist/s/<string:artist_name>', methods=['GET'])
def get_artist_search(artist_name):
    # task = filter(lambda t: t['id'] == task_id, tasks)
    # if len(task) == 0:
        abort(404)
    # return jsonify({'task': task[0]})


@app.route('/api/artist/<int:artist_id>', methods=['GET'])
def get_artist_by_id(artist_id):
    # task = filter(lambda t: t['id'] == task_id, tasks)
    # if len(task) == 0:
        abort(404)
    # return jsonify({'task': task[0]})


@app.route('/api/concerts', methods=['GET'])
def get_concert_list(concert_name):
    # task = filter(lambda t: t['id'] == task_id, tasks)
    # if len(task) == 0:
        abort(404)
    # return jsonify({'task': task[0]})


@app.route('/api/concert/s/<string:concert_name>', methods=['GET'])
def get_concert_search(concert_name):
    # task = filter(lambda t: t['id'] == task_id, tasks)
    # if len(task) == 0:
        abort(404)
    # return jsonify({'task': task[0]})


@app.route('/api/concert/<int:concert_id>', methods=['GET'])
def get_concert_by_id(concert_id):
    # task = filter(lambda t: t['id'] == task_id, tasks)
    # if len(task) == 0:
        abort(404)
    # return jsonify({'task': task[0]})

#
# @app.route('/', methods=['GET'])
# def get_concerts():
#     # task = filter(lambda t: t['id'] == task_id, tasks)
#     all_concert = Concert.query.all()
#
#     print(all_concert)
#
#     # if len(all_concert) == 0:
#     #     abort(404)
#     return jsonify({'task': all_concert})



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(' http://127.0.0.1:5000/')
    app.run(host='0.0.0.0', port=port)

from flask import Blueprint, request, make_response
from google.cloud import datastore
import json
from constants import *
from common_functions import get_entity, is_nonexistent, response_object, new_boat

client = datastore.Client()
bp = Blueprint('boat', __name__, url_prefix='/boats')


@bp.route('', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def get_post_boats():
    if request.method == 'GET':
        query = client.query(kind=BOAT)
        res = list(query.fetch())
        for e in res:
            e['id'] = e.key.id
        return json.dumps(res), 200

    elif request.method == 'POST':
        content = request.get_json()
        if 'name' in content and 'type' in content and 'length' in content:
            boat = new_boat(datastore, client, content)
            return response_object(make_response(json.dumps(boat)), AJSON, 201)
        else:
            return {'Error': MISSING_ATTR}, 400

    elif request.method == 'PUT':
        return {'Error': NOT_SUPPORTED + 'PUT'}, 405

    elif request.method == 'PATCH':
        return {'Error': NOT_SUPPORTED + 'PATCH'}, 405

    elif request.method == 'DELETE':
        return {'Error': NOT_SUPPORTED + 'DELETE'}, 405

    else:
        return {'Error': NOT_ACCEPTABLE}, 406


@bp.route('/<bid>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def get_put_patch_delete(bid):
    if request.method == 'GET':
        boat = get_entity(client, BOAT, bid)
        if is_nonexistent(boat):
            return {'Error': NO_BOAT}, 404
        boat['id'] = boat.key.id
        return response_object(make_response(json.dumps(boat)), AJSON, 200)

    elif request.method == 'POST':
        return {'Error': NOT_SUPPORTED + 'POST'}, 405

    elif request.method == 'PUT':
        return {'Error': NOT_SUPPORTED + 'PUT'}, 405

    elif request.method == 'PATCH':
        return {'Error': NOT_SUPPORTED + 'PATCH'}, 405

    elif request.method == 'DELETE':
        boat = get_entity(client, BOAT, bid)
        if is_nonexistent(boat):
            return {'Error': NO_BOAT}, 404
        client.delete(client.key(BOAT, int(bid)))
        return '', 204

    else:
        return {'Error': NOT_ACCEPTABLE}, 406

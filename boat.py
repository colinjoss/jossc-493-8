from flask import Blueprint, request, make_response
from google.cloud import datastore
import json
from json2html import json2html
from constants import *
from common_functions import get_entity, is_nonexistent, name_in_use, valid, \
    response_object, new_boat

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
            if not valid('name', content['name']):
                return {'Error': BAD_VALUE}, 400
            if not valid('type', content['type']):
                return {'Error': BAD_VALUE}, 400
            if not valid('length', content['length']):
                return {'Error': BAD_VALUE}, 400
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

    elif request.method == 'PATCH':
        content = request.get_json()
        if 'id' in content or 'self' in content:
            return {'Error': NO_EDIT}, 403

        if 'name' in content or 'type' in content or 'length' in content:
            boat = get_entity(client, BOAT, bid)
            if is_nonexistent(boat):
                return NO_BOAT, 404
            for prop in content:
                if not valid(prop, content[prop]):
                    return {'Error': BAD_VALUE}, 400
                boat[prop] = content[prop]
            res = response_object(make_response(json.dumps(boat)), AJSON, 200)
            client.put(boat)
            return res
        else:
            return {'Error': MISSING_ATTR}, 400

    elif request.method == 'PUT':
        content = request.get_json()
        if 'id' in content:
            return {'Error': NO_EDIT}, 403
        if 'name' in content and 'type' in content and 'length' in content:
            boat = get_entity(client, BOAT, bid)
            if boat is None:
                return NO_BOAT, 404
            for prop in content:
                if not valid(prop, content[prop]):
                    return {'Error': BAD_VALUE}, 400
                boat[prop] = content[prop]
            res = response_object(make_response(json.dumps(boat)), AJSON, 200)
            client.put(boat)
            return res
        else:
            return {'Error': MISSING_ATTR}, 400

    elif request.method == 'DELETE':
        boat = get_entity(client, BOAT, bid)
        if is_nonexistent(boat):
            return {'Error': NO_BOAT}, 404
        client.delete(client.key(BOAT, int(bid)))
        return '', 204

    else:
        return {'Error': NOT_ACCEPTABLE}, 406

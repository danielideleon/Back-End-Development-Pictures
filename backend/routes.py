from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all pictures"""
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a single picture by id"""
    # Parse through the list to find the picture with the given id
    for picture in data:
        if picture.get('id') == id:
            return jsonify(picture), 200
    
    # If no picture found with that id, return 404
    return jsonify({"error": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture"""
    # Extract picture data from request body
    new_picture = request.get_json()
    
    # Print the picture data
    print(new_picture)
    
    # Check if picture with this id already exists
    for picture in data:
        if picture.get('id') == new_picture.get('id'):
            # If found, return 302 with message
            return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302
    
    # If no duplicate found, append the new picture to the data list
    data.append(new_picture)
    
    # Return the new picture with 201 Created status
    return jsonify(new_picture), 201
    

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update an existing picture"""
    # Extract the updated picture data from request body
    updated_picture = request.get_json()
    
    # Find the picture with the given id
    for i, picture in enumerate(data):
        if picture.get('id') == id:
            # Update the picture while preserving the id
            updated_picture['id'] = id  # Ensure id doesn't change
            data[i] = updated_picture
            return jsonify(updated_picture), 200
    
    # If picture not found, return 404 with message
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by id"""
    # Traverse the data list to find the picture by id
    for i, picture in enumerate(data):
        if picture.get('id') == id:
            # If picture exists, delete it from the list
            data.pop(i)
            # Return an empty body with 204 No Content status
            return '', 204
    
    # If picture not found, return 404 with message
    return jsonify({"message": "picture not found"}), 404
from flask import Blueprint, jsonify
from flask_login import login_required, current_user



api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

@api_bp.route("/health")
def connection_check():
    return jsonify({
        "message": "Connection success"
    }), 200

# @api_bp.route("/keys", methods=["GET","POST"])
# @login_required
# def keys():


    # # get curent user id
    # result = create_api_key(user_id=current_user.id)

    # if result is None:
    #     return jsonify({
    #         "error": "Failed to create API Key"
    #     }), 400
    
    # return jsonify({
    #     "api_key": result
    # }), 201

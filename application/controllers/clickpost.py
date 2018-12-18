
from flask import Blueprint
from application.utils.invalid_data_exception import *
from application.utils.api_exception import ApiException
from application.utils.response_util import *
from flask import request, jsonify
from application.services.clickpost_service import Clickpost

click_post = Blueprint('clickpost', __name__)

@click_post.route('/', methods=['GET'])
def index():
    return "Welcome to Clickpost!"

@click_post.route('/delivery_status', methods=['GET'])
def get_delivery_status():

    awbno = request.args.get('awbno')
    if awbno is None:
        return construct_response("Invalid awbno", INVALID_DATA_FORMAT)
    else:
        try:
            resp = Clickpost().get_delivery_status(awbno)
        except InvalidDataException as e:
            return construct_response(e.msg, e.value)
        except ApiException as e:
            return construct_response(e.msg, e.value)
        except Exception as e:
            return construct_response("Internal Server Server", INTERNAL_SERVER_ERROR)
    return jsonify(resp)
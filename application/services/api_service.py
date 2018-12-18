from application.utils.response_util import *
from application.utils.api_exception import ApiException

class ApiServiceProvider:

    """
    ApiServiceProvider: service for fetching response from third party APIs
    """

    def __init__(self):
        self.url = 'https://wowship.wowexpress.in/index.php/api/detailed_status/trackAwb'
        self.headers = {
            'Content-Type': "application/json",
            'Cache-Control': "no-cache"
        }

    def get_status_response(self, awbno):
        param = {'awb': awbno}
        resp = get_response(url=self.url, headers=self.headers, params=param)
        if resp.status_code == SUCCESS:
            return resp
        else:
            raise ApiException(INTERNAL_SERVER_ERROR, 'Internal server error')

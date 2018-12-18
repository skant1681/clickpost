from application import celery
from pymemcache.client import base
import requests, urllib
from application.models.shipment_dao import Shipment

SUCCESS = 200

# background task for fetching response from third party API and updating cache and db,
#if delivery status is not DELIVERED or RTO-DELIVERED
@celery.task(name='fetch_response_from_api.fetch_status_from_api_and_update')
def fetch_status_from_api_and_update(awbno):

    url = 'https://wowship.wowexpress.in/index.php/api/detailed_status/trackAwb'
    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache"
    }
    param = {'awb': awbno}

    resp = requests.request("GET", url, headers=headers, params=urllib.parse.urlencode(param))

    if resp.status_code == SUCCESS:
        resp = resp.json()[0]
        if 'scan_detail' in resp:
            _client = base.Client(('localhost', 11211))
            _client.set(awbno, resp['scan_detail'][-1]['status'])

            shipment_obj = Shipment.objects(awbno=awbno).only('details').first()
            shipment_obj_length = len(shipment_obj['details'])
            updated_status_length = len(resp['scan_detail'])
            diff = updated_status_length - shipment_obj_length
            if diff > 0:
                for i in range(0, diff):
                    shipment_obj.details[shipment_obj_length + i] = resp['scan_detail'][shipment_obj_length + i]
            shipment_obj.save()


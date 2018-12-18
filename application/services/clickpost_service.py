from application.models.shipment_dao import Shipment
from .api_service import ApiServiceProvider
from pymemcache.client import base
from application.services.tasks.save_to_db import save_to_clickpost_db
from application.services.tasks.save_to_cache import save_to_memcache
from application.services.tasks.fetch_response_from_api import fetch_status_from_api_and_update


class Clickpost:

    """ Clickpost Service: consist of services for creating,
        updating and fetching tracking details of particular awbno
    """

    def __init__(self):
        # connected to memcached server running on localhost:11211
        self._client = base.Client(('localhost', 11211))

    def get_delivery_status(self, awbno):

        # checking if {awbno: status} is present in memcache
        status = self._client.get(awbno)
        if status is None:
            # In case of cache miss, checking if awbno is present is db
            shipment_obj = Shipment.objects(awbno=awbno).only('details.status').first()
            if shipment_obj is None:
                # fetching track details from third party API case of cache miss and not in db
                resp = ApiServiceProvider().get_status_response(awbno)
                resp = resp.json()[0]
                if 'scan_detail' not in list(resp.keys()):
                    return resp
                else:
                    # storing the {awbno: status} in memcache
                    save_to_memcache.delay(awbno, resp['scan_detail'][-1]['status'])
                    # saving the track details in the db
                    save_to_clickpost_db.delay(awbno, resp['scan_detail'])
                    resp = resp['scan_detail'][-1]
                    return {'status': resp['status']}
            else:
                shipment_details = shipment_obj['details']
                shipment_details = shipment_details[-1]
                # if status of track details found in db is DELIVERED or RTO-DELIVERED, returning the response
                # and updating {awbno: status} in cache
                if shipment_details['status'] == 'DELIVERED' or shipment_details['status'] == 'RTO-DELIVERED':
                    save_to_memcache.delay(awbno, shipment_details['status'])
                    return {'status': shipment_details['status']}
                else:
                    # if status is anything else, added rest api call to the queue
                    fetch_status_from_api_and_update.delay(awbno)
                    return {'status': shipment_details['status']}
        # if status of track details found in cache is DELIVERED or RTO-DELIVERED, returning the response
        elif status.decode('utf') == 'DELIVERED' or status.decode('utf') == 'RTO-DELIVERED':
            return {'status': status.decode('utf')}
        else:
            #  if status is anything else, added rest api call to the queue
            fetch_status_from_api_and_update.delay(awbno)
            return {'status': status.decode('utf')}









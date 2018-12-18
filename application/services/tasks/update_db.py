from application import celery
from application.models.shipment_dao import Shipment


# background task to update db
@celery.task(name='update_db.update_status_in_clickpost_db')
def update_status_in_clickpost_db(awbno, status_detail):

    shipment_obj = Shipment.objects(awbno=awbno).only('details').first()
    shipment_obj_length = len(shipment_obj['details'])
    updated_status_length = len(status_detail)
    diff = updated_status_length - shipment_obj_length
    if diff > 0:
        for i in range(0,diff):
            shipment_obj.details[shipment_obj_length + i] = status_detail[shipment_obj_length + i]
    shipment_obj.save()


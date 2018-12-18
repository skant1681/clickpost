from application import celery
from application.models.shipment_dao import ShipmentDetail, Shipment
import csv

# background task to create new entry for awbno
@celery.task(name='tasks.save_to_db.save_to_clickpost_db')
def save_to_clickpost_db(awbno, status_detail):

    shipment_obj = Shipment()
    for item in status_detail:
        shipment_detail_obj = ShipmentDetail()
        shipment_detail_obj.status = item['status']
        shipment_detail_obj.location = item['location']
        shipment_detail_obj.remarks = item['remarks']
        shipment_detail_obj.status_code = item['status_code']
        shipment_detail_obj.status_description = item['status_description']
        shipment_detail_obj.updated_date = item['updated_date']
        shipment_obj.details.append(shipment_detail_obj)
    shipment_obj.awbno = awbno

    """ Assuming src and dest pincode are updated through different APIs,
        temporary soln: updating src and dest pincode in the db, from file
        assuming size of file fits in memory, or we'll have to read it in chunks of smaller sizes
    """
    with open('application/tracking_ids.csv', 'r') as fp:
        data = csv.DictReader(fp)
        for row in data:
            if row['awbno'] == awbno:
                shipment_obj.source_pincode = row['src']
                shipment_obj.destination_pincode = row['dest']
                break

    shipment_obj.save()
    return "successfully saved to database"

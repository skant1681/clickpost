import mongoengine as me
from application.models.shipment_dao import Shipment
from datetime import datetime

"""
Algorithm:
> Based on scan detail, find the last tracked location,
> retrieve all the track details which has last tracked loaction as one of the location 
  and also has same destination pincode,
> finally count all the track id's which was completed within 24 hrs and divide by all track details retrieved

"""

def predict_out_delivery(src, dest, scan_detail):

    db = me.connect(host="mongodb://127.0.0.1:27017/clickpost")

    # current location of shipment
    curr_location = scan_detail[-1]['location'] if 'location' in scan_detail[-1] else None

    if curr_location is None:
        return "Current scan does not have location"

    # get pincode for current location
    ship_obj = Shipment.objects(details__location=curr_location, destination_pincode=dest).only('details.location','details.status_code', 'details.updated_date')
    obj_count = ship_obj.count()

    one_day_delivery = 0
    for obj in ship_obj:
        for detail in obj.details:
            if detail.location == curr_location:
                start_date = datetime.strptime(detail.updated_date, '%Y-%m-%d %H:%M:%S')
            if detail.status_code == '305':
                end_date = datetime.strptime(detail.updated_date, '%Y-%m-%d %H:%M:%S')
                break
        time_taken = end_date - start_date
        if time_taken.days == 0:
            one_day_delivery +=1

    return one_day_delivery/obj_count


if __name__ == '__main__':
    src = input("Enter Source Pincode: ")
    dest = input("Enter Destination Pincode: ")
    scan_detail = input("Enter scan detail (list of dict)")   # e.g. [{"awbno":"C0053087810","status_code":"99","status":"PENDING PICKUP","status_description":"PENDING PICKUP","remarks":"PENDING PICKUP","location":"NA","updated_date":"2018-11-03 23:31:51"},{"awbno":"C0053087810","status_code":"100","status":"PICKUP DONE","status_description":"PICKUP DONE","remarks":"PICKUP DONE FROM BOMBAY HUB HUB","location":"MUMBAI HUB","updated_date":"2018-11-04 00:57:25"},{"awbno":"C0053087810","status_code":"102","status":"IN-TRANSIT","status_description":"PROCESSING AT ORIGIN HUB","remarks":"SHIPMENT INSERTED IN BAG AT BOMBAY HUB (ORIGIN HUB)","location":"MUMBAI HUB","updated_date":"2018-11-04 02:10:38"}]

    res = predict_out_delivery(src, dest, scan_detail)
    print(res)



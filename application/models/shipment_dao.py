from mongoengine import *

class ShipmentDetail(EmbeddedDocument):
    status_code = IntField()
    status = StringField()
    status_description = StringField()
    remarks = StringField()
    location = StringField()
    updated_date = StringField()

class Shipment(Document):
    awbno = StringField(unique=True)
    source_pincode = StringField()
    destination_pincode = StringField()
    details = ListField(EmbeddedDocumentField(ShipmentDetail))

    meta = {
        'collection': 'Shipment',
        'indexes': [
            {
                'fields': ['awbno'],
                'unique' : True
             },
            {
                'fields': ['awbno','details.status'],
                'unique' : True
            }
        ]
    }
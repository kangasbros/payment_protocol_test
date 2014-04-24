import datetime
import time
from flask import Flask
from paymentrequest_pb2 import PaymentRequest, PaymentDetails, Output, PaymentACK
app = Flask(__name__)
app.debug = True
from flask import request

SELF_URL = "http://localhost:5000"

@app.route("/payment_request")
def payment_request():
    payment_details = PaymentDetails()
    payment_details.time = int(time.time())
    payment_details.expires = int(time.time()) + 3600*6
    payment_details.memo = "blaa blaa"
    payment_details.payment_url = SELF_URL + "/payment"
    payment_details.merchant_data = '\x00\xf0\x03'
    output = payment_details.outputs.add()
    output.script = "13MwCu4gVfYRNDCbZBXTLHLNHBD3TuxVFN"
    output.amount = 10000
    payment_request = PaymentRequest()
    payment_request.serialized_payment_details = payment_details.SerializeToString()
    return payment_request.SerializeToString()

@app.route("/payment", methods=['POST'])
def payment():
    payment_data = request.data
    payment = Payment().ParseFromString(payment_data)
    payment_ack = PaymentACK()
    payment_ack.memo = "this is shit"
    return payment_ack.SerializeToString()

if __name__ == "__main__":
    app.run()

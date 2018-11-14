import androidhelper
import json
import time
from bottle import Bottle, run, response, request


app = Bottle()
droid = androidhelper.Android()


@app.route("/hello")
def hello():

	return "Hello World!"


@app.route("/location")
def get_location():

	droid.startLocating()
	droid.eventWaitFor('location', 12500)

	time.sleep(0.1)

	current_location = droid.readLocation().result

	if not current_location:

		current_location = droid.getLastKnownLocation().result

	droid.stopLocating()
	response.content_type = "application/json"

	return json.dumps(
		{
		  "result": current_location
		}, indent=4
 	)


@app.route("/orientation")
def get_orientation():

	droid.startSensingTimed(1, 100)
	sensor_result = droid.sensorsReadOrientation().result #azimuth (z), pitch (x), roll (y)
	droid.stopSensing()

	response.content_type = "application/json"

	return json.dumps(
		{
			"azimuth": sensor_result[0],
			"pitch": sensor_result[1],
			"roll": sensor_result[2]
		}, indent=4
	)


@app.route("/sms/read")
def get_sms():
    	
		unread_sms = droid.smsGetMessages(True).result

		response.content_type = "application/json"

		return json.dumps(
			{
				"unread": unread_sms
			}, indent=4, ensure_ascii=False
		)

@app.get("/sms/send")
def sms_get():
    	
	return """
	<html>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>My SMS Portal</title>
		<body>
			<h1>My SMS Portal</h1>
			<h2>Please enter the following details</h2>
			<form action="/sms/send" id="smsform" method="post">
				Phone Number: <input type="text", name="phone_number">
				<br>
				<br>
				<textarea row="5" cols="40" name="smsContent" form="smsform">Enter message here...</textarea>
				<br>
				<input type="submit">
			</form>
			<p>
				Once completed, please click submit button!
			</p>
		</body>
	</html>
	"""


@app.post("/sms/send")
def sms_post():
    	
	sms_phone = request.forms.get("phone_number")
	sms_content = request.forms.get("smsContent")

	response.content_type = "application/json"

	status = droid.smsSend(sms_phone, sms_content).result

	if status["error"] is None:
		
		return json.dumps(
			{
				"status_code": 200,
				"status_msg": "success",
				"phone_num": sms_phone
			}, indent=4, ensure_ascii=False
		)

	return json.dumps(
		{
			"status_code": 500,
			"status_msg": "failed",
			"phone_number": sms_phone
		}, indent=4, ensure_ascii=False
	)


if __name__ == "__main__":

	run(app, host="localhost", port=8080)

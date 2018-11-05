import androidhelper
import json
import time
from bottle import Bottle, run, response


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


if __name__ == "__main__":

	run(app, host=localhost, port=8080)

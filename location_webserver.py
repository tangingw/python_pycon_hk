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

	droid.startLocating(100, 100)
	time.sleep(0.1)

	current_location = droid.readLocation().result

	droid.stopLocating()
	response.content_type = "application/json"

	return json.dumps(
		{
		  "result": current_location
		}
 	)


import math
import time
import androidhelper


def main():

	droid = androidhelper.Android()

	current_time = int(time.time())
	end_time = current_time + 250

	droid.startSensingTimed(2, 25)

	while int(time.time()) < end_time:

		time.sleep(.5)
		s3 = droid.sensorsReadAccelerometer().result

		g_result = math.sqrt(sum([s**2 for s in s3]))

		print(
			"The gravitation acceleration is %.4f" % g_result
		)
	
	droid.stopSensing()


if __name__ == "__main__":

	main()


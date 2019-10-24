from flaskapp.flask_app import FlaskThread
import time

flask_thread = FlaskThread()
flask_thread.run()

print ('wait')
time.sleep(1)
print ('end wait')
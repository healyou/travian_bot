from gui.view import View
from flaskapp.flask_app import FlaskThread
import time

view = View()
view.mainloop()

# flask_thread = FlaskThread()
# flask_thread.run()

print ('wait')
time.sleep(1)
print ('end wait')
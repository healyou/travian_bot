from datetime import datetime, timedelta
from collections import deque, namedtuple

d = datetime.now()
print (str(datetime.now()))
print (str(datetime.today()))
print (str(datetime.now() + timedelta(seconds=777)))

deq = deque()
deq.append(1)
deq.append(2)
print (deq)
deq.popleft()

print (deq)
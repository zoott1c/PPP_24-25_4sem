# redislite_daemon.py
from redislite import Redis
import time

r = Redis('/tmp/redislite.db')
r.set('foo', 'bar')
print("redislite.db is alive! (daemon запущен)")
try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    print("redislite_daemon остановлен.")

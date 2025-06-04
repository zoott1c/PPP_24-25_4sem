# init_redislite.py

from redislite import Redis

r = Redis('/tmp/redislite.db')
r.set('foo', 'bar')
print("redislite.db создан и готов к работе")

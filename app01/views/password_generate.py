import hashlib
password='123'
obj = hashlib.md5('django-insecure-n+^bx-lug#!un_42-w#9y*sxof^)_5$jnqu!##4qf5^#tdk%16'.encode('utf-8'))
obj.update(password.encode('utf-8'))
print(obj.hexdigest())

from django.conf import settings
import hashlib


def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()


if __name__ == '__main__':
    data_string = '123'
    obj = hashlib.md5('django-insecure-n+^bx-lug#!un_42-w#9y*sxof^)_5$jnqu!##4qf5^#tdk%16'.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    print(obj.hexdigest())

from __future__ import print_function
from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver

auth_username = 'your_auth_username'
auth_password = 'your_auth_password'
auth_url = 'http://controller:5000'
project_name = 'your_project_name_or_id'
region_name = 'your_region_name'

provider = get_driver(Provider.OPENSTACK_SWIFT)
swift = provider(auth_username,
                 auth_password,
                 ex_force_auth_url=auth_url,
                 ex_force_auth_version='2.0_password',
                 ex_tenant_name=project_name,
                 ex_force_service_region=region_name)

container_name = 'fractals'
container = swift.create_container(container_name=container_name)
print(container)

print(swift.list_containers())

file_path = 'goat.jpg'
object_name = 'an amazing goat'
container = swift.get_container(container_name=container_name)
object = container.upload_object(file_path=file_path, object_name=object_name)

objects = container.list_objects()
print(objects)

object = swift.get_object(container_name, object_name)
print(object)

swift.delete_object(object)

objects = container.list_objects()
print(objects)










import base64
import cStringIO
import json

import requests

endpoint = 'http://IP_API_1'
params = { 'results_per_page': '-1' }
response = requests.get('%s/v1/fractal' % endpoint, params=params)
data = json.loads(response.text)
for fractal in data['objects']:
    response = requests.get('%s/fractal/%s' % (endpoint, fractal['uuid']), stream=True)
    container.upload_object_via_stream(response.iter_content(), object_name=fractal['uuid'])

for object in container.list_objects():
    print(object)




file_path = 'goat.jpg'
object_name = 'backup_goat.jpg'
extra = {'meta_data': {'description': 'a funny goat', 'created': '2015-06-02'}}
with open('goat.jpg', 'rb') as iterator:
    object = swift.upload_object_via_stream(iterator=iterator,
                                            container=container,
                                            object_name=object_name,
                                            extra=extra)




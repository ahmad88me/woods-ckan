rm -Rf /lib/ckan/default/src/ckanext-docspace
cp -Rf ckanext-docspace /lib/ckan/default/src
cd /lib/ckan/default/src/ckanext-docspace ; /usr/lib/ckan/default/bin/python setup.py install
supervisorctl reload
service nginx restart
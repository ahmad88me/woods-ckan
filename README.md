# woods-ckan


## Create Extension
1. Setup CKAN
2. Activate the environment `. /usr/lib/ckan/default/bin/activate`.
3. Go to src folder `cd /usr/lib/ckan/default/src/`.
4. Create extension `ckan generate extension`. (Note: `cookiecutter` method does not work for ckan version 2.9).


## Known Issues
* When running: `sudo supervisorctl reload`

Error: ```error: <class 'FileNotFoundError'>, [Errno 2] No such file or directory: file: /usr/lib/python3/dist-packages/supervisor/xmlrpc.py line: 560```

Solution:
```
sudo service supervisor stop
sudo service supervisor start
```

* redis
```
sudo service redis restart
```



 # Funding
 This work was funded partially by EIT Digital under the WOODS project.

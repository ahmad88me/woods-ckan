# woods-ckan


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

 
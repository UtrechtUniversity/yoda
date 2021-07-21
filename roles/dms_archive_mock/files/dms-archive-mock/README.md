# DM Mock

## Install app

```
pipenv --python 3 shel
python3 setup.py install
```

## Run the server
```
dm_server --host 0.0.0.0 --port 5000
```

More info:

```
dm_server --help
```

## Configure the client
Configuration file
```
vi ~/.dmmock_server.json
{
  "host": "127.0.0.1",
  "port": 5000
}
```

## Running directly from source

```
pipenv --python 3 install -r requirements.txt
python3 -m dm_server.app --help
python3 -m dm_server.app --host 0.0.0.0 --port 5000
```

## Publish to Artifactory

### Configuration

configure ~/.pypirc file
```
[distutils]
index-servers =
              public-testing
              public-production
              testing
              production


[public-testing]
repository: https://artie.ia.surfsara.nl/artifactory/api/pypi/DMS-PyPI-Testing-Public
username: dms-artie
password: <PASSWORD>

[testing]
repository: https://artie.ia.surfsara.nl/artifactory/api/pypi/DMS-PyPI-Testing
username: dms-artie
password: <PASSWORD>

[production]
repository: https://artie.ia.surfsara.nl/artifactory/api/pypi/DMS-PyPI-Production
username: dms-artie
password: <PASSWORD>

[public-production]
repository: https://artie.ia.surfsara.nl/artifactory/api/pypi/DMS-PyPI-Production-Public
username: dms-artie
password: <PASSWORD>
```

### Build
```
python setup.py sdist upload -r testing
python setup.py sdist upload -r public-testing

python setup.py sdist upload -r production
python setup.py sdist upload -r public-production
```

### Install

```
pip3 install https://artie.ia.surfsara.nl:443/artifactory/DMS-PyPI-Production-Public/dm-mock/0.8/dm-mock-0.8.tar.gz
```

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

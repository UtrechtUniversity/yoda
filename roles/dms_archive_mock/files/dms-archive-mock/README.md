# DM Mock

## Install app
```
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install .
```

## Run the server
```
dm_server --host 0.0.0.0 --port 5000
```

## More info
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

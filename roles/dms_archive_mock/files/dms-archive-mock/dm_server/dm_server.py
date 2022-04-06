import os
import sys
import time
import json
import threading
import numpy as np


class MockServer(object):
    def __init__(self,
                 random_mig_time=True,
                 default_mig_time=10,
                 default_unmig_time=10,
                 basedir="/",
                 allowedlist=None):
        self.basedir = basedir
        self.allowedlist = allowedlist
        self.random_mig_time = random_mig_time
        self.default_mig_time = default_mig_time
        self.default_unmig_time = default_unmig_time

        if sys.version_info[0] == 2:
            self.fhandle = os.urandom(32).encode('hex')
        else:
            self.fhandle = os.urandom(32).hex()
        self.default_owner = 45953

        # data
        self.inodes = {}
        self.states = {}

        # data dir
        self.data_dir = os.path.join(os.path.expanduser("~"), ".dmmock_server")
        print("data_dir: {}".format(self.data_dir))
        self.read_data()

        # thread
        self.active = True
        self.is_daemon = True
        self.tick_sec = 10
        self.listener_thread = threading.Thread(name='run',
                                                target=self.run,
                                                args=())
        self.listener_thread.setDaemon(self.is_daemon)
        self.listener_thread.start()

    def read_data(self):
        n = 0
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        for root, dirs, files in os.walk(self.data_dir):
            for f in files:
                if f.endswith(".json"):
                    with open(os.path.join(root, f)) as f:
                        data = json.load(f)
                        self.inodes[data['inode']] = data
                        if not data['state'] in self.states:
                            self.states[data['state']] = {}
                        self.states[data['state']][data['inode']] = True
                        n += 1
        print("number of inodes: {}".format(n))

    def get_path(self, path):
        np = os.path.join(self.basedir, path)
        if self.allowedlist is not None:
            p = os.path.abspath(path)
            for prefix in self.allowedlist:
                if p.startswith(prefix):
                    return np
            raise RuntimeError("{} not accepted".format(path))
        else:
            return np

    def get_state(self, path):
        np = self.get_path(path)
        inode = os.stat(np).st_ino
        data_path = path
        if inode in self.inodes:
            return self.inodes[inode].copy()
        else:
            return {'state': 'REG',
                    'inode': inode,
                    '_path': np,
                    '_filename': data_path,
                    'bfid': 0,
                    'fhandle': self.fhandle,
                    'flags': 0,
                    'nregn': 0,
                    'owner': self.default_owner,
                    'projid': 0,
                    'sitetag': 0,
                    'size': 0,
                    'space': 0}

    def set_state(self, obj):
        obj['change_time'] = int(time.time())
        data_path = os.path.join(self.data_dir,
                                 "{0}.json".format(obj['inode']))
        with open(data_path, 'w') as fp:
            json.dump(obj, fp)
        if obj['inode'] in self.inodes:
            old_state = self.inodes[obj['inode']]['state']
        else:
            old_state = None
        if old_state is not None and old_state in self.states:
            del self.states[old_state][obj['inode']]
        if not obj['state'] in self.states:
            self.states[obj['state']] = {}
        self.states[obj['state']][obj['inode']] = True
        self.inodes[obj['inode']] = obj

    def generate_bfid(self, obj):
        if sys.version_info[0] == 2:
            obj['bfid'] = os.urandom(32).encode('hex')
        else:
            obj['bfid'] = os.urandom(32).hex()
        obj['emask'] = 17000
        obj['fhandle'] = self.fhandle
        obj['flags'] = 0
        obj['owner'] = self.default_owner
        obj['nregn'] = 1
        obj['projid'] = 0
        obj['sitetag'] = 0
        obj['size'] = os.stat(obj['_path']).st_size
        obj['space'] = 0

    def put(self, path, remove):
        obj = self.get_state(path)
        if obj['state'] == 'REG':
            obj['state'] = 'MIG'
            obj['remove'] = remove
            obj['change_duration'] = self.get_mig_time()
            print(obj['change_duration'])
            self.generate_bfid(obj)
            self.set_state(obj)
        elif obj['state'] == 'DUL' and remove:
            obj['state'] = 'OFL'
            self.set_state(obj)

    def get(self, path):
        obj = self.get_state(path)
        if obj.get('state') == 'MIG':
            obj['remove'] = False
            self.set_state(obj)
        elif obj.get('state') == 'OFL':
            obj['state'] = 'UNM'
            obj['change_duration'] = self.get_unmig_time()
            print(obj['change_duration'])
            self.set_state(obj)
        return obj

    def run(self):
        while self.active:
            time.sleep(self.tick_sec)
            self.tick()
        print("stopped")

    def check_delay(self, inode):
        if 'change_time' in inode and 'change_duration' in inode:
            now = int(time.time())
            time_diff = now - inode['change_time']
            if time_diff > inode['change_duration']:
                return True
            else:
                return False
        else:
            return True

    def get_mig_time(self):
        if self.random_mig_time:
            value = np.random.poisson(self.default_mig_time)
            if value > self.default_mig_time * 3:
                value = self.default_mig_time * 3
            return value
        else:
            return self.default_mig_time

    def get_unmig_time(self):
        if self.random_mig_time:
            value = np.random.poisson(self.default_unmig_time)
            if value > self.default_unmig_time * 3:
                value = self.default_unmig_time * 3
            return value
        else:
            return self.default_unmig_time

    def tick(self):
        keys = [k for k in self.states.get('MIG', {}).keys()]
        for inode in keys:
            if self.check_delay(self.inodes[inode]):
                obj = self.inodes[inode].copy()
                if obj.get('remove', 0):
                    obj['state'] = 'OFL'
                else:
                    obj['state'] = 'DUL'
                self.set_state(obj)
        keys = [k for k in self.states.get('UNM', {}).keys()]
        for inode in keys:
            if self.check_delay(self.inodes[inode]):
                obj = self.inodes[inode].copy()
                obj['state'] = 'DUL'
                self.set_state(obj)

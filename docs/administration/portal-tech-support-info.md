---
parent: Administration Tasks
title: Collecting portal technical support information
nav_order: 17
---
# Collecting portal technical support information

In case there is a problem with the Yoda portal and the application logs don't provide enough
information about what is going wrong, you may need to collect additional information. The portal
has a monitoring thread to collect information for technical support purposes.

You can start information collection by creating a signal file for the monitoring thread. By default,
this is `/var/www/yoda/show-tech.sig`:

```bash
$ sudo touch /var/www/yoda/show-tech.sig
```

When the signal file is present, the portal monitoring thread will start logging technical support information.
By default, the support information files are written to the Apache private `tmp` directory within the
global `/tmp` directory. These information files contain stack traces for each portal thread, as well
as some other information about the system and the portal.

Remove the signal file after you have collected enough information:

```bash
$ sudo rm /var/www/yoda/show-tech.sig
```

## Example output

```
Portal tech support info for combined.yoda.test, collected on 30/07/2024 at 16:42:46.926656
Yoda version, as per portal config: development (ae4de73e4fe931423caf27f7537a57b72a606764)

System-wide CPU percent:         2.5%
Memory: global total:            4.1 GB
Memory: global available:        2.0 GB
Memory: global buffers:          136.7 MB
Memory: global cached:           674.2 MB
Memory: process RSS:             55.9 MB
Memory: process VMS:             740.7 MB
Memory: process shared:          17.3 MB

Thread ID: 140688039364352
  /usr/lib/python3.8/threading.py:890 [_bootstrap]
     self._bootstrap_inner()
  /usr/lib/python3.8/threading.py:932 [_bootstrap_inner]
     self.run()
  /usr/lib/python3.8/threading.py:1254 [run]
     self.function(*self.args, **self.kwargs)
  /var/www/yoda/monitor.py:47 [record_info_if_needed]
     tshoot_info: StringIO = self.get_tshoot_info()
  /var/www/yoda/monitor.py:80 [get_tshoot_info]
     for filename, line_number, function_name, line in traceback.extract_stack(stack):

Thread ID: 140688058500864
  /usr/lib/python3.8/threading.py:890 [_bootstrap]
     self._bootstrap_inner()
  /usr/lib/python3.8/threading.py:932 [_bootstrap_inner]
     self.run()
  /usr/lib/python3.8/threading.py:870 [run]
     self._target(*self._args, **self._kwargs)
  /var/www/yoda/research/research.py:48 [irods_writer]
     chunk = q.get()
  /usr/lib/python3.8/queue.py:170 [get]
     self.not_empty.wait()
  /usr/lib/python3.8/threading.py:302 [wait]
     waiter.acquire()

Thread ID: 140688071923456
  /usr/lib/python3.8/threading.py:890 [_bootstrap]
     self._bootstrap_inner()
  /usr/lib/python3.8/threading.py:932 [_bootstrap_inner]
     self.run()
  /usr/lib/python3.8/threading.py:870 [run]
     self._target(*self._args, **self._kwargs)
  /var/www/yoda/connman.py:50 [gc]
     time.sleep(1)
```


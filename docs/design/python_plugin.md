# The iRODS python plugin

## Defining python code

Python code can be included in core.py, in the following form:
```
def pythonFunction(rule_args, callback, rei):
    callback.writeLine("stdout", "python rule called")
```

Static python functions must be defined in core.py.  There are three different types of functions, each with its own way of handling arguments and return values.
- rules called directly by iRODS have numbered parameters passed through rule_args:
  ```
  def acPythonPEP(rule_args, callback, rei):
      callback.writeLine("stdout", "arg = " + rule_args[0])
  ```
  such rules can also return values through numbered output parameters.
- rules called with irule or from the frontend have access to ```global_vars```, in which named parameters are passed as strings including the quotes:
  ```
  def pythonFunction(rule_args, callback, rei):
      arg = global_vars['*arg'][1:-1]                # strip the quotes
      callback.writeLine("stdout", "arg = " + arg)
  ```
  Output cannot be passed back through named parameters, but has to be handled with writeString/writeLine:
  ```
  INPUT *arg="some argument"
  OUTPUT ruleExecOut
  ```
  Note that global_vars is only available to python functions defined in core.py, not to functions imported by core.py.
- ordinary python functions which are not called by iRODS or externally, but only by other python code, accept arguments normally and can return a value:
  ```
  def concat(str1, str2):
      return str1 + str2
  ```

## Calling python code

Python functions can be called with irule:
```
irule -r irods_rule_engine_plugin-python-instance pythonFunction '*arg="some argument"' ruleExecOut
```

```
irule -r irods_rule_engine_plugin-python-instance -F pythonfunc.r
```

**pythonfunc.r**:
```
def pythonFunction(rule_args, callback, rei):
    arg = global_vars['*arg'][1:-1]     # strip the quotes
    callback.writeLine("stdout", "arg = " + arg)

INPUT *arg="some argument"
OUTPUT ruleExecOut
```

Note that in the latter case, core.py is not automatically imported.

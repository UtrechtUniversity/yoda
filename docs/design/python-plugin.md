# Yoda and the iRODS python plugin

## Configuring the Python rule plugin

Include the following in ```server_config.json```, in the ```rule_engines``` array:
```
{
    "instance_name": "irods_rule_engine_plugin-python-instance",
    "plugin_name": "irods_rule_engine_plugin-python",
    "plugin_specific_configuration": {}
}
```
We use the python plugin as the second in the array, after the iRODS rule language plugin, so that we can combine our existing rule language code with new python code.

## Defining python code

Python code can be included in core.py, in the following form:
```
def pythonFunction(rule_args, callback, rei):
    callback.writeLine("stdout", "python rule called")
```

Static python functions must be defined in core.py.  There are three different types of functions, each with its own way of handling arguments and return values.
- Rules called directly by iRODS have numbered parameters passed through ```rule_args```:
  ```
  def acPythonPEP(rule_args, callback, rei):
      callback.writeLine("stdout", "arg = " + rule_args[0])
  ```
  Such rules can also return values through numbered output parameters.
- Rules called with irule or from the frontend have access to ```global_vars```, in which named parameters are passed as strings including the quotes:
  ```
  def main(rule_args, callback, rei):
      arg = global_vars["*arg"][1:-1]                # strip the quotes
      callback.writeLine("stdout", "arg = " + arg)
  ```
  Output cannot be passed back through named parameters, but has to be handled with writeString/writeLine:
  ```
  INPUT *arg="some argument"
  OUTPUT ruleExecOut
  ```
  Note that ```global_vars``` is only available to python functions defined in core.py, not to functions imported by core.py.
- Ordinary python functions which are not called by iRODS or externally, but only by other python code, accept arguments normally and can return a value:
  ```
  def concat(str1, str2):
      return str1 + str2
  ```

##  Simple code example roundtrip irods -> python -> irods ##

  Essence of the example is that **rule_args** both serves as input and as output parameters

  iRODS:
  ```
  # \brief Front end rule to retrieve XSD location
  #
  # \param[in]  folder        Path of the folder
  # \param[out] schemaLocation Location of XSD
  # \param[out] status        Status of the action
  # \param[out] statusInfo    Information message when action was not successful

  iiFrontGetSchemaLocation(*folder, *schemaLocation, *status, *statusInfo)
  {
          *status = "Success";
          *statusInfo = "";

          *schema = '';

          iiRuleGetLocation(*folder, *schema); # it is not possible to directly use *schemaLocation here
          writeLine('serverLog', 'schema: ' ++ *schema);

          *schemaLocation =  *schema; # again, does not work when passing schemaLocation direcly in iiRuleGetLocation
  }
  ```

  PYTHON:
  ```
  # \brief Nonsense function that returns 'enriched' text based on rule_args[0]
  # rule_args serves both as input and output parametes

  def iiRuleGetLocation(rule_args, callback, rei):
      rule_args[1] = 'You passed  the  folder: ' + rule_args[0]

```

## Calling python code

Python functions can be called from iRODS rule language rules.

Python functions can also be called with irule:
```
irule -r irods_rule_engine_plugin-python-instance pythonFunction '*arg="some argument"' ruleExecOut
```
or
```
irule -r irods_rule_engine_plugin-python-instance -F pythonfunc.r
```

**pythonfunc.r**:
```
def main(rule_args, callback, rei):
    arg = global_vars["*arg"][1:-1]                # strip the quotes
    callback.writeLine("stdout", "arg = " + arg)

INPUT *arg="some argument"
OUTPUT ruleExecOut
```

Note that in the latter case, python functions in core.py are not available.

## Calling microservices from python code

Use ```irods_types``` to create output parameters of the proper type, and obtain the output values from ```ret_val["arguments"][N]```.

**Example code:**

```
def uuGetGroups(rule_args, callback, rei):
    import json

    groups = []
    ret_val = callback.msiMakeGenQuery("USER_GROUP_NAME", "USER_TYPE = 'rodsgroup'", irods_types.GenQueryInp())
    query = ret_val["arguments"][2]        # output parameter type GenQueryInp

    ret_val = callback.msiExecGenQuery(query, irods_types.GenQueryOut())
    while True:
        result = ret_val["arguments"][1]   # output parameter type GenQueryOut
        for row in range(result.rowCnt):
            name = result.sqlResult[0].row(row)
            groups.append(name)

        # continue with this query
        if result.continueInx == 0:
            break
        ret_val = callback.msiGetMoreRows(query, result, 0)

    callback.writeString("stdout", json.dumps(groups))
```

## Setting AVU's from Python

**Example code:**

```
import irods_types

def uuMetaAdd(callback, objType, objName, attribute, value):
    keyValPair  = callback.msiString2KeyValPair(attribute + "=" + value, irods_types.KeyValPair())['arguments'][1]
    retval = callback.msiAssociateKeyValuePairsToObj(keyValPair, objName, objType)

def addCollectionStatus(rule_args, callback, rei):
    uuMetaAdd(callback, "-C", "/tempZone/home/research-initial", "status", "PUBLISHED")

---
grand_parent: Software design
parent: Other
---
# Yoda and the iRODS Python Rule Engine Plugin

iRODS can be used with various rule engine plugins, so that rules can be written in multiple programming languages.
Yoda uses both the builtin (legacy) iRODS rule language plugin and the Python Rule Engine Plugin (PREP).

This page contains basic information about working with the PREP in combination with Yoda. The
[PREP documentation](https://github.com/irods/irods_rule_engine_plugin_python) has additional generic
information and examples.

## Configuring the Python rule engine plugin

The Python Rule Engine Plugin is configured in ```server_config.json```, in the ```rule_engines``` array:

```json
{
    "instance_name": "irods_rule_engine_plugin-python-instance",
    "plugin_name": "irods_rule_engine_plugin-python",
    "plugin_specific_configuration": {}
}
```

The Python plugin is the second element in the rule engine list, after the iRODS rule language plugin,
so that we can combine legacy rule language code with new Python code.

## Python rule functions

There are three different types of functions, each with its own way of handling arguments and return values:
- Rules called directly by iRODS have numbered parameters passed through ```rule_args```:

  ```python
  def acPythonPEP(rule_args, callback, rei):
      callback.writeLine("stdout", "arg = " + rule_args[0])
  ```

  Such rules can also return values through numbered output parameters.

- Rules called with irule or from the frontend have access to ```global_vars```, in which named parameters are passed as strings including the quotes:

  ```python
  def main(rule_args, callback, rei):
      arg = global_vars["*arg"][1:-1]                # strip the quotes
      callback.writeLine("stdout", "arg = " + arg)
  ```

  Output cannot be passed back through named parameters, but has to be handled with writeString/writeLine:

  ```
  INPUT *arg="some argument"
  OUTPUT ruleExecOut
  ```
  Note that ```global_vars``` is only available to Python rule functions, not to other functions called by rule functions.

- Ordinary Python functions which are not called as a rule by iRODS or externally, but only by other Python code. For example:

  ```python
  def concat(str1, str2):
      return str1 + str2
  ```

Explanation of parameters from the [PREP documentation](https://github.com/irods/irods_rule_engine_plugin_python#configuration):

```
The first argument [...], rule_args, is a tuple containing the optional, positional parameters fed to
the rule function by its caller; these same parameters may be written to, with the effect that the
written values will be returned to the caller. The callback object is effectively a gateway through
which other rules (even those managed by other rule engine plugins) and microservices may be called.
Finally, rei (also known as "rule execution instance") is an object carrying iRODS-related context
for the current rule call, including any session variables.
```

## Running Python rule code using irule

The example below shows a simple "Hello world" rule that can be executed using `irule`. The rule takes
the name argument from global_vars, strips away the quotes and prints a greeting.

```
def main(rule_args, callback, rei):
    name = global_vars["*name"][1:-1]
    callback.writeLine("stdout", "Hello " + name + "!")

input *name="World"
output ruleExecOut
```

The code can be run by putting it in a .r file, e.g. `hello.r` and then running irule on it:

```
$ irule -r irods_rule_engine_plugin-python-instance -F hello.r
Hello World!
```

You need to have a rodsadmin account in order to run Python code this way. The rule function needs
to be named `main`.

## Defining Python code in the ruleset

iRODS Python code in the ruleset needs to ultimately be imported from `/etc/irods/core.py`. On Yoda environments,
`core.py` has an import statement that imports all Python code in the Yoda ruleset directory:

```
from rules_uu import *
```

Yoda Python rule code is put in ruleset directory `/etc/irods/yoda-ruleset`, which is linked from
`/etc/irods/rules_uu`. Each rule is defined in a function.

This is a minimal example of a rule definition in Python:

```python
def hello_world(rule_args, callback, rei):
    callback.writeLine("stdout", "Hello world!")
```

If you add this function to a Python file in the ruleset directory, and ensure it is included in the file's `__all__`
list (assuming it has one), you can call it using irule:

```
$ irule -r irods_rule_engine_plugin-python-instance hello_world null ruleExecOut
Hello world!
```

If the rule would have had a parameter, you could have passed it like this:

```
irule -r irods_rule_engine_plugin-python-instance hello_world '*arg="some argument"' ruleExecOut
```

## Using Yoda rule decorators

In Yoda, the `rule.make` decorator is commonly used to write rules in a more pythonic way and
to reduce boilerplate.

This example defines a rule with two input parameters and a single output parameter using `rule.make`:

```
@rule.make(inputs=[0,1], outputs=[2])
def foo(ctx, x, y):
    return int(x) + int(y)
```

This is the equivalent of the code above without the decorator:

```
def foo(rule_args, callback, rei):
    x, y = rule_args[0:2]
    rule_args[2] = int(x) + int(y)
```

For a complete overview of functionality of `rule.make`, please consult [the function documentation](https://github.com/UtrechtUniversity/yoda-ruleset/blob/development/util/rule.py)

There's also an `api.make` decorator available that creates an API function which can
receive and return data in JSON format. For additional information, please consult [the function documentation](https://github.com/UtrechtUniversity/yoda-ruleset/blob/development/util/api.py)


## Simple code example roundtrip iRODS -> Python -> iRODS

Essence of the example is that **rule_args** serves as both input and as output parameters

iRODS rule language:

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

        *schemaLocation =  *schema; # again, does not work when passing schemaLocation directly in iiRuleGetLocation
}
```

Python:

```python
# \brief Nonsense function that returns 'enriched' text based on rule_args[0]
# rule_args serves both as input and output parameters

def iiRuleGetLocation(rule_args, callback, rei):
      rule_args[1] = 'You passed  the  folder: ' + rule_args[0]
```

## Calling microservices from Python code

Use ```irods_types``` to create output parameters of the proper type, and obtain the output values from ```ret_val["arguments"][N]```.

**Example code:**

```python
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

## Setting AVUs from Python

**Example code:**

```python
import irods_types

def uuMetaAdd(callback, objType, objName, attribute, value):
    keyValPair  = callback.msiString2KeyValPair(attribute + "=" + value, irods_types.KeyValPair())['arguments'][1]
    retval = callback.msiAssociateKeyValuePairsToObj(keyValPair, objName, objType)

def addCollectionStatus(rule_args, callback, rei):
    uuMetaAdd(callback, "-C", "/tempZone/home/research-initial", "status", "PUBLISHED")
```

---
parent: Administration Tasks
title: Local ruleset patches
nav_order: 2
---
# Local ruleset patches

In some cases, you might want to make some local modifications to a ruleset in order to modify Yoda's behaviour. This can
be achieved by defining a `patch` parameter for a ruleset. 

You would usually create a `patch` value using a command like: `git diff | sed 's/^/    /'` on your modified ruleset.

If `patch` is set to "" (empty string), no patch is applied. This effectively resets any earlier local changes
deployed via Ansible. If you want to remove a local patch, you would first need to run the playbook with an empty patch value
in order to reset earlier patches. After that, you can remove the patch value.

## Example

This example patch changes the UUPRIMARYRESOURCES constant in the ruleset code.

```
core_rulesets:
  - name: yoda-ruleset
    repo: https://github.com/UtrechtUniversity/yoda-ruleset.git
    ruleset_name: rules-uu
    version: "{{ yoda_version }}"
    patch: |
      diff --git a/uuConstants.r b/uuConstants.r
      index 5311d5c..aa44bad 100644
      --- a/uuConstants.r
      +++ b/uuConstants.r
      @@ -36,7 +36,7 @@ UURESOURCETIERATTRNAME = UUORGMETADATAPREFIX ++ 'storage_tier';
       UUMETADATASTORAGEMONTH =  UUORGMETADATAPREFIX ++ 'storage_data_month';
    
       # \constant UUPRIMARYRESOURCES
      -UUPRIMARYRESOURCES = list("irodsResc");
      +UUPRIMARYRESOURCES = list("irodsResc3");
    
       # \constant UUREPLICATIONRESOURCE
       UUREPLICATIONRESOURCE = "irodsRescRepl";
    install_scripts: yes
  - name: core
    ruleset_name: core
    path: /etc/irods/core.re
    install_scripts: no
```


## Considerations

* The playbook temporarily restores the original ruleset and then re-applies the patch. This could constitute a risk if the local modifications are related to safety or security. 
* You would need to verify for yourself that the patch is still compatible with the latest version of the ruleset before running the playbook. Having the playbook apply a patch that is no longer compatible with the ruleset code may cause Yoda to fail.

## See also

This page is about making local changes to rulesets that can be deployed via Ansible. This method is typically used for long-term
changes. If you want to make a short-term change (e.g. a temporary change for testing), you might want to consider using
[a hotfix](hotfixing-ruleset.md) instead.

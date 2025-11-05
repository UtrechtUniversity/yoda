---
parent: Administration Tasks
title: Migrating published/depublished data packages
nav_order: 22
---
# Migrating published/depublished data packages

This documentation explains the testing process for migrating Published and Depublished data packages from one Yoda instance to another. 


**Requirements:**
- iPump version 0.2.6 or later
- Yoda version 1.10 or later
- OpenJDK 21 or later

## Setting up iPump

Set up iPump on source instance.

1. Get snapshot jar of latest iPump code

```bash
wget https://github.com/tsmeele/ipump/raw/refs/heads/main/target/ipump-0.2.6-SNAPSHOT.jar
```

2. Install OpenJDK in source instance.

```bash
sudo apt install openjdk-21-jre-headless
```

3. Add IP address of source in destination `/etc/hosts` file.  
4. Add IP address of destination in source `/etc/hosts` file.
5. Create rodsadmin user in source and destination instance.
6. Create `ipump.ini` file in source instance. For example:

```bash
source_host=source-combined.yoda.test
source_port=1247
source_username=samplerodsadmin
source_zone=tempZone
source_password=rodspassword
source_auth_scheme=native
destination_host=dest-combined.yoda.test
destination_port=1247
destination_username=samplerodsadmin
destination_zone=tempZone
destination_password=rodspassword
destination_auth_scheme=native
```
7. Copy self-signed certificate from destination to source instance:

``` bash
scp /etc/ssl/certs/selfsigned_localhost.crt vagrant@source-combined.yoda.test:/home/vagrant
```

8. Rename certificates in source instance:

```bash
sudo keytool -importcert   -file /etc/ssl/certs/selfsigned_localhost.crt   -alias selfsigned-cert-1   -keystore /usr/lib/jvm/java-21-openjdk-amd64/lib/security/cacerts   -storepass changeit
```
```bash
sudo keytool -importcert   -file /home/vagrant/selfsigned_localhost.crt   -alias selfsigned-cert-2   -keystore /usr/lib/jvm/java-21-openjdk-amd64/lib/security/cacerts   -storepass changeit
```

## Description of code changes at destination instance

1. Created utility file for migration that retrieves 'enable_migration' metadata. 

2. Depending on 'enable_migration' value, disabled call to post status transition policy.

In policies.py:

```bash
@rule.make()
def py_acPostProcForModifyAVUMetadata(ctx: rule.Context,
                                      option: str,
                                      obj_type: str,
                                      obj_name: str,
                                      attr: str,
                                      value: str,
                                      unit: str) -> None:
    info = pathutil.info(obj_name)

    if attr == constants.IISTATUSATTRNAME and info.space in [pathutil.Space.RESEARCH, pathutil.Space.DEPOSIT]:
        status = constants.research_package_state.FOLDER.value if option in ['rm', 'rmw'] else value
        policies_folder_status.post_status_transition(ctx, obj_name, str(user.user_and_zone(ctx)), status)

    elif info.space is pathutil.Space.VAULT:
        if attr == constants.IIVAULTSTATUSATTRNAME:
            if not migration.get_migration_config(ctx, obj_name):
                policies_datapackage_status.post_status_transition(ctx, obj_name, str(user.user_and_zone(ctx)), value)
            else:
                return policy.succeed()
        if attr.startswith(constants.UUORGMETADATAPREFIX) and attr != constants.IIARCHIVEATTRNAME:
            vault.update_archive(ctx, obj_name, attr)

    # Send emails after datarequest status transition if appropriate
    elif attr == datarequest.DATAREQUESTSTATUSATTRNAME and info.space is pathutil.Space.DATAREQUEST:
        policies_datarequest_status.post_status_transition(ctx, obj_name, value)

```

2. Modified status transition code to skip the policy check for Published and Depublished data packages.

In policies_datapackage_status.py:

```bash
def can_transition_datapackage_status(ctx: rule.Context,
                                      actor: str,
                                      coll: str,
                                      status_from: str,
                                      status_to: str) -> policy.Succeed | policy.Fail:

    transition = (constants.vault_package_state(status_from),
                  constants.vault_package_state(status_to))
    if transition not in constants.datapackage_transitions:
        if migration.get_migration_config(ctx, coll):
            return policy.succeed()
        else:
            return policy.fail('Illegal status transition')

    if status_to is constants.vault_package_state.SUBMITTED_FOR_PUBLICATION:
        meta_path = meta.get_latest_vault_metadata_path(ctx, coll)
        if meta_path is None:
            return policy.fail('Metadata missing, unable to submit this data package for publication.')

        if not meta.is_json_metadata_valid(ctx, meta_path):
            return policy.fail('Metadata is incomplete or invalid, please open the metadata form for more information')

    return policy.succeed()
```

## Copying data packages

Copying vault space from source to destination instance. For example:

```bash
java -jar ipump-0.2.6-SNAPSHOT.jar -v -config ipump.ini /tempZone/home/vault-initial /tempZone/home/vault-initial
```

## Correct ACLs

After successful migration of data packages, there might be a need to correct ACLs of data packages. As an admin, run the package-check script to fix ACLs of a data package. The script can be run in two modes: 'read' and 'write'. 'Read' mode informs the user that ACLs are missing/incorrect. 'Write' mode fixes incorrect ACLs of a data package. For example:

### Read mode
```bash
irule -r irods_rule_engine_plugin-python-instance -F /etc/irods/yoda-ruleset/tools/package-check.r '*coll=/tempZone/home/vault-initial/research-initial[123456789]' '*mode=read'
```

### Write mode
```bash
irule -r irods_rule_engine_plugin-python-instance -F /etc/irods/yoda-ruleset/tools/package-check.r '*coll=/tempZone/home/vault-initial/research-initial[123456789]' '*mode=write'
```
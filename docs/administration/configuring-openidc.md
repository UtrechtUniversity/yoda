#Configuring OpenId Connect (OIDC)
Instruction on how to configure Openid Connect authentication:
1. When configuring a new Yoda instance
2. On an already existing Yoda instance

## 1. When configuring a new Yoda instance
When creating a new Yoda instance, setup the variables in the group_vars as explained in [Configuring Yoda](configuring-yoda.md).
Alternatively, you can choose to pass the variables with the *--extra-vars* option everytime when running the Ansible playbook.

For OIDC to function properly it requires the following variables to be set:
- oidc_active
- oidc_client_id
- oidc_client_secret
- oidc_auth_base_uri
- oidc_token_uri
- oidc_userinfo_uri

Additionally, depending on the authorization server, you may need to configure the following variables:
- oidc_scopes (default: *openid*)
- oidc_acr_values
- oidc_email_field (default: *email*)

Finally, for customization purposes, you can also configure:
- oidc_signin_text

## 2. On an already existing Yoda instance
When configuring OIDC on an already existing Yoda instance the same variables mentioned in the previous section are needed. 
Whereas the passing them before deploying puts them automatically in the correct places, in this case they need to be set in different locations manually.
Below you can find all the different locations you need to update with the correct configuration.
Administrator rights are required for modifying some of the files and you need to modify **all** the files for OIDC to work correctly.

### Yoda Portal
In /var/www/yoda/yoda-portal/config/config_local.php, update all the `$config` fields that start with `oidc_` as needed (i.e. update the required variables, update the optional variables if needed).
Make sure the values are between single quotes and that lines end with a semicolon.
Some of the OIDC variables need not be changed, they are:
- oidc_callback_uri
- oidc_auth_uri (**Note:** this is a different variable than oidc_auth_base_uri!)

Example:
```
$config['oidc_client_id'] = 'myClienId';
$config['oidc_client_secret'] = 'very-secret-dont-share';
$config['oidc_auth_base_uri'] = 'https://some-doma.in/oauth/authorize';
...
```
Don't forget to set `$config['oidc_active']` to `true`!

### ICAT Server
In /etc/pam.d modify the *irods* file so the following rule is added as the last step

```
auth        required    pam_python.so /var/lib/irods/msiExecCmd_bin/oidc.py
```

And update the line before it so that `required` is updated to `sufficient`
```
auth        required      pam_radius_auth.so
```
Unless the contents of *irods* were changed beforehand, the contents should now look like this
```
# Ansible managed
#%PAM-1.0

auth        optional      pam_faildelay.so delay=1000000
auth        sufficient    pam_unix.so

auth [success=ignore default=1] pam_exec.so /usr/local/bin/is-user-external.sh
auth [success=done default=die] pam_exec.so expose_authtok /usr/local/bin/external-auth.py

auth        sufficient    pam_radius_auth.so
auth        required      pam_python.so /var/lib/irods/msiExecCmd_bin/oidc.py
```

In /var/lib/irods/msiExecCmd_bin open **oidc.py**, and update line 7 so that the `oidc_userinfo_uri` is assigned to the variable.
For example, if our `oidc_userinfo_uri` is `https://my-doma.in/oauth/userinfo`, then the updated line should look like:
```
USERINFO_URI = "https://my-doma.in/oauth/userinfo"
```
In the same file (**oidc.py**), update line 20 so the text between the double quotes is the `oidc_email_field` variable.
For example, if the `oidc_email_field` is `mail`, then the updated line should look like:
```
        email = r.json()["mail"]
```
Please note, the updates in **oidc.py** are whitespace-sensitive, meaning that you should ***not*** add extra whitespace characters.

## Verifying OIDC
To verify whether the deployment/update went successfully, go to the Yoda portal and click the **Sign in** button.
If configured correctly, you should now see an extra button with the text as configured with the `oidc_signin_text` variable (default: *Sign in with OIDC*).

When clicking on the *Sign in with OIDC* button, login at the configured authorized server and verify that you are returned to the Yoda portal homepage.
If so, you have correctly configured authentication via OIDC.
Please also verify that the standard login method is still working as intended.

## Troubleshooting

- **The Sign in with OIDC button is missing:** check if the `$config['oidc_active']` variable is set to `true`.
- **After signing in at the authorization server I am redirected to the login screen with the error \'Failed to login to Yoda. Please contact a data manager about your account.\':** This can have multiple causes:
    1. The user that is trying to sign in does not exist, or
    2. An error occurred after signing in at the authorization server.

To check whether the problem is caused by case 1, verify that the user exists in Yoda and add them if they are not.
To solve case 2, re-check the client secret, the token URI, the email field, and scopes variables.
- **After making the changes I see a blank page:** A PHP error is preventing the requested page from being loaded and it is likely due to a syntax error in the Yoda portal /var/www/yoda/yoda-portal/config/config_local.php file. Please check whether all the changed lines still end with semicolons and all delimiters have a matching pair (i.e. no missing quotes/double quotes/closing brackets etc.).

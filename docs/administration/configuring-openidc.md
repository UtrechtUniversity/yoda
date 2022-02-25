---
parent: Administration Tasks
title: Configuring OIDC
nav_order: 12
---
# Configuring OpenID Connect (OIDC)
Instruction on how to configure OpenID Connect authentication.

## Configuring the variables
When creating a new Yoda instance, setup the variables in the group_vars as explained in [Configuring Yoda](configuring-yoda.md) and run the playbook.
Alternatively, you can choose to pass the variables with the *--extra-vars* option every time when running the Ansible playbook.
The development group_vars contains examples for all of the variables.

For OIDC to function properly it requires the following variables to be set:
- oidc_active (default: `false`), used by Ansible during setup. Please note that switching `oidc_active` to `false` (and running the Ansible playbook again) is not a safe way to disable OIDC: you should also replace the `oidc_client_id` and `oidc_client_secret` values with placeholders.
- oidc_client_id
- oidc_client_secret
- oidc_auth_base_uri
- oidc_token_uri
- oidc_userinfo_uri
- oidc_jwks_uri, which returns all the valid JSON Web Key sets
- oidc_jwt_issuer, the `iss` value in the JWT token

Additionally, depending on the authorization server, you may need to configure the following variables:
- oidc_scopes (default: `openid`)
- oidc_acr_values
- oidc_email_field (default: `email`)

Finally, for customization purposes, you can also configure:
- oidc_domains, which should be an array of domains with OIDC authentication, e.g. `["mydomain.com","myotherdomain.com"]`. By default, OIDC authentication is enabled for every domain (provided that oidc_active is set to `true`)
- oidc_signin_text (deprecated since v1.8)

For token verification there are also the following parameters which define what checks are done when verifying a JWT. Take caution when setting values to `false`, as this makes verification less strict. Details can be found in the group_vars file.
- oidc_req_exp (default: `true`)      
- oidc_req_iat (default: `false`)    
- oidc_req_nbf (default: `false`)   
- oidc_verify_aud (default: `true`)
- oidc_verify_iat (default: `false`)
- oidc_verify_exp (default: `true`)
- oidc_verify_iss (default: `true`)

## Verifying OIDC
To verify whether the deployment/update went successfully, go to the Yoda portal and click the *Sign in* button, enter an email address and click *Next*.
If configured correctly, you should now see an extra button with the text as configured with the `oidc_signin_text` variable (default: *Sign in with OIDC*).

When clicking on the *Sign in with OIDC* button, login at the configured authorized server and verify that you are returned to the Yoda portal homepage.
If so, you have correctly configured authentication via OIDC.
Please also verify that the standard login method is still working as intended.

Alternatively, if you have configured the `oidc_domains` parameter, entering an email address with the configured domain and clicking *Next* should redirect you automatically to the configured authorization server.
Follow the above steps as if having clicked the *Sign in with OIDC* button

## Troubleshooting
- **The Sign in with OIDC button is missing:** check if the `oidc_active` variable is set to `true` in you group_vars and run the Ansible playbook again.
- **After signing in at the authorization server I am redirected to the login screen with the error \'Failed to login to Yoda. Please contact a data manager about your account.\':** This can have multiple causes:
    1. The user that is trying to sign in does not exist, or
    2. An error occurred after signing in at the authorization server.

    To check whether the problem is caused by case 1, verify that the user exists in Yoda and add them if they are not.
    To solve case 2, re-check the client secret, the token URI, the email field, the public key, and scopes variables.

---
parent: Administration Tasks
title: Configuring OIDC
nav_order: 11
---
# Configuring OpenID Connect (OIDC)
Instruction on how to configure OpenID Connect authentication.

## Configuring the variables
When creating a new Yoda instance, setup the variables in the group_vars as explained in [Configuring Yoda](configuring-yoda.md) and run the playbook.
Alternatively, you can choose to pass the variables with the *--extra-vars* option every time when running the Ansible playbook.

For OIDC to function properly it requires the following variables to be set:
- oidc_active
- oidc_client_id
- oidc_client_secret
- oidc_auth_base_uri
- oidc_token_uri
- oidc_userinfo_uri
- oidc_public_key

Additionally, depending on the authorization server, you may need to configure the following variables:
- oidc_scopes (default: *openid*)
- oidc_acr_values
- oidc_email_field (default: *email*)

Finally, for customization purposes, you can also configure:
- oidc_signin_text

## Verifying OIDC
To verify whether the deployment/update went successfully, go to the Yoda portal and click the **Sign in** button.
If configured correctly, you should now see an extra button with the text as configured with the `oidc_signin_text` variable (default: *Sign in with OIDC*).

When clicking on the *Sign in with OIDC* button, login at the configured authorized server and verify that you are returned to the Yoda portal homepage.
If so, you have correctly configured authentication via OIDC.
Please also verify that the standard login method is still working as intended.

## Troubleshooting
- **The Sign in with OIDC button is missing:** check if the `oidc_active` variable is set to `true`.
- **After signing in at the authorization server I am redirected to the login screen with the error \'Failed to login to Yoda. Please contact a data manager about your account.\':** This can have multiple causes:
    1. The user that is trying to sign in does not exist, or
    2. An error occurred after signing in at the authorization server.

    To check whether the problem is caused by case 1, verify that the user exists in Yoda and add them if they are not.
    To solve case 2, re-check the client secret, the token URI, the email field, the public key, and scopes variables.

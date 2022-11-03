# How to troubleshoot email-related issues

In order to verify that sending email messages from Yoda works as
expected, an email test script is included in the irods-ruleset-uu repository.

It can be called from the command line as the irods user. For example:
```bash
/etc/irods/irods-ruleset-uu/tools/mail-test.sh "a.admin@uu.nl"
```

The expected output is:
```
Successfully executed rule for testing email with destination <a.admin@uu.nl>
```

You should shortly receive an email message on the provided address
with subject `[Yoda] Test mail`.

## Postfix

If you have [configured Yoda to use Postfix for email delivery](local-postfix-mta.md),
additional information is logged for troubleshooting.

In that case, email delivery log data can be found in `/var/log/maillog`.
The current contents of the Postfix mail queue can be viewed using the
`sudo postqueue -p` command.

---
grand_parent: Software design
parent: Other
---
# Matomo integration

Yoda supports tracking web statistics for visits to data package landing
pages using [Matomo](https://matomo.org), an open source web analytics application.

Yoda has two Matomo-related configuration options:
- Tracking using Matomo (Ansible parameter: `yoda_matomo_tracking_enabled`): tracks
  visits to landing pages. By itself, tracking visits does not expose any web analytics
  data to Yoda users. Only Matomo users can see web analytics information.
- Visit counter (Ansible parameter: `yoda_matomo_counter_enabled`): when this feature is
  enabled, a visit counter will be shown to visitors on all Yoda landing pages.

See the [Yoda configuration guide](../../administration/configuring-yoda.md) for further
information about configuration parameters.

After changing these configuration options, a publication endpoint update is needed
to effectuate the changes:

```
irule -r irods_rule_engine_plugin-irods_rule_language-instance -F /etc/irods/yoda-ruleset/tools/update-publications.r
```

Matomo itself is not part of Yoda, but an associated
[Ansible playbook](https://github.com/utrechtUniversity/matomo-ansible) is provided
to deploy a Matomo environment that can be used in combination with Yoda. The visit counter
feature requires Matomo to have the [Page View Counter Plugin](https://github.com/UtrechtUniversity/matomo-plugin-pageviewcounter)
installed, and the plugin needs to be configured using the Matomo web interface to make visit
data of the landing page site publicly available by setting the "Allowed Site IDs" plugin parameter.
Furthermore, it is necessary to add the landing page domain to the list of Cross-Origin Resource Sharing (CORS) domains
in the general settings of Matomo, so that browsers permit the front-end page view counter code to access
the page view counter plugin API.

# \file
# \brief job
# \author Sietse Snel
# \copyright Copyright (c) 2022, Utrecht university. All rights reserved
# \license GPLv3, see LICENSE
#
#  This file should be executed as part of a recurring crontab job
#  as the irods admin user (i.e. irods user type rodsadmin)
#  e.g. run every 5 minutes
#
#  It clears all locks on intake folders after job_movetovault has run, in
#  order to facilitate retries after transient errors
#

uuYcClearIntakeLocks {
	# intake areas can be added to the grouplist as needed
	*grouplist = list ("initial","test");
	*zone = $rodsZoneClient;

	foreach (*grp in *grouplist) {
		*intakeRoot = "/*zone/home/grp-intake-*grp";
		*vaultRoot  = "/*zone/home/grp-vault-*grp";
                # uuUnlock also succeeds if lock doesn't exist, so no need to verify that lock exists first
		uuUnlock(*vaultRoot);
	}
}

input *intakeRoot='dummy'
output ruleExecOut

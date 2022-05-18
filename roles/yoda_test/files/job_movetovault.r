# \file
# \brief job
# \author Ton Smeele
# \copyright Copyright (c) 2015, Utrecht university. All rights reserved
# \license GPLv3, see LICENSE
#
#  if another instance of the job is running then the vault will be
#  locked and silently ignored
#

uuYcRunIntake2Vault {
        # intake areas can be added to the grouplist as needed
        *grouplist = list ("initial", "test", "foo");
        *grp_prefixes = list ("grp-intake-", "intake-");
        *zone = $rodsZoneClient;

        foreach (*grp in *grouplist) {
                *intakeRoot = "";
                *found = false;

                foreach (*prefix in *grp_prefixes) {
                    *grp_name = *prefix ++ *grp;
                    foreach(*row in SELECT USER_GROUP_NAME
                        WHERE USER_GROUP_NAME = '*grp_name'
                        AND USER_TYPE = 'rodsgroup') {

                        *path=*row.USER_GROUP_NAME;
                        *found = true;
                        break;
                    }
                    if (*found) {
                        break;
                    }
                }
                *intakeRoot = "/*zone/home/*grp_name";
                *vaultRoot  = "/*zone/home/grp-vault-*grp";

                # uuLock(*vaultRoot, *status);
                *status = 0;
                if (*status == 0) {
                        # we have a lock
                        uuYc2Vault(*intakeRoot, *vaultRoot, *status);
                        if (*status == 0 ) then *result = "ok" else *result = "ERROR (*status)";
                        writeLine("serverLog","RunIntake2Vault for *intakeRoot result = *result");
                        uuUnlock(*vaultRoot);
                }
        }
}


input *intakeRoot='dummy'
output ruleExecOut

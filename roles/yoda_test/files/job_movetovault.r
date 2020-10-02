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
        *grouplist = list ("initial","test");
        *zone = $rodsZoneClient;
        foreach (*grp in *grouplist) {
                *intakeRoot = "/*zone/home/grp-intake-*grp";
                *vaultRoot  = "/*zone/home/grp-vault-*grp";
                uuLock(*vaultRoot, *status);
                # FIX ME: currently we ignore existing locks
                # because locks are not removed when the rule exist with error
                # need a more robust solution for this!
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

# \file      job_checksums.r
# \brief     Youth Cohort - generate checksum index of Vault
# \author    Ton Smeele
# \copyright Copyright (c) 2016, Utrecht University. All rights reserved.
# \license   GPLv3, see LICENSE

job_checksums {
  *root = "/tempZone/home/grp-vault-initial";
# NB: logfile location for test purpose, requires new position upon production!
  *logfile = "/tempZone/home/grp-datamanager-initial/checksums.txt";
  uuYcGenerateDatasetsIndex(*root, *logfile, *status);
  writeLine("stdout","return status is *status");
  *root = "/tempZone/home/grp-vault-test";
  *logfile = "/tempZone/home/grp-datamanager-test/checksums.txt";
  uuYcGenerateDatasetsIndex(*root, *logfile, *status);
  writeLine("stdout","return status is *status");
}

input null
output ruleExecOut
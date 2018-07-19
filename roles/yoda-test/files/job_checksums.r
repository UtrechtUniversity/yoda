# \file      job_checksums.r
# \brief     Youth Cohort - generate checksum index of Vault
# \author    Ton Smeele
# \copyright Copyright (c) 2016, Utrecht University. All rights reserved.
# \license   GPLv3, see LICENSE

job_checksums {
  *zone = $rodsZoneClient;
  *root = "/*zone/home/grp-vault-initial";
# NB: logfile location for test purpose, requires new position upon production!
  *logfile = "/*zone/home/grp-datamanager-initial/checksums.txt";
  uuYcGenerateDatasetsIndex(*root, *logfile, *status);
  writeLine("stdout","return status is *status");
  *root = "/*zone/home/grp-vault-test";
  *logfile = "/*zone/home/grp-datamanager-test/checksums.txt";
  uuYcGenerateDatasetsIndex(*root, *logfile, *status);
  writeLine("stdout","return status is *status");
}

input null
output ruleExecOut
#!/usr/bin/env python3

"""This script retrieves statistics information from a Yoda system. This
   data is about the amount of storage space used by each research compartment.

   - 1.9 : data is not divided into tiers. One data point is collected for each day.
           There is no inherent limit in the amount of historical statistics data that
           can be kept.

   The output format of the script depends on the statistics data version.
"""

import ast
import re
import subprocess
import sys
import yaml
from typing import Dict, List

from packaging.version import parse as parse_version

outputfile = '/var/yoda-financial-data/stats.yaml'
common_fields = ["category", "subcategory"]


def detect_statistics_data_format() -> str:
    with open("/etc/irods/yoda-ruleset/__init__.py", "r") as initfile:
        for line in initfile:
            version_match = re.match(
                "^\\s*__version__\\s+=\\s+\'(\\d+\\.\\d+\\.\\d+)\'", line)
            if version_match:
                version = str(version_match.groups(1)[0])
                return "1.8" if parse_version(version) < parse_version('1.9') else "1.9"

    sys.exit("Error: unable to determine Yoda statistics data version.")


def get_research_groups() -> List[str]:
    groups: List[str] = []
    for line in _get_cmd_stdout_lines(['iadmin', 'lg']):
        if line.startswith("research-") or line.startswith("deposit-"):
            groups.append(line.rstrip())
    return groups


def get_attribute_value_data_for_group(group: str) -> Dict[str, str]:
    """ Returns attributes and values for AVUs as attribute-value dict. This assumes attributes
          are unique (if not, it returns only one of the values).
    """
    attribute = None
    output: Dict[str, str] = dict()

    for line in _get_cmd_stdout_lines(['imeta', 'ls', '-u', group]):
        if line.startswith("attribute: "):
            attribute = line.replace("attribute: ", "", 1).rstrip()
        if line.startswith("value:"):
            value = line.replace("value: ", "", 1).rstrip()
            if attribute is not None:
                output[attribute] = value

    return output


def get_relevant_group_metadata_19(group):
    output = {}
    total_by_date = {}
    common_data = {}
    attribute = None
    stats_prefix = "org_storage_totals"

    for (attribute, value) in get_attribute_value_data_for_group(group).items():
        if attribute in common_fields:
            common_data[attribute] = value
        elif attribute.startswith(stats_prefix):
            date_string = int(attribute.replace(stats_prefix, "", 1).rstrip())
            storagedata = ast.literal_eval(value)
            assert (isinstance(storagedata, list))
            (category, research_space, vault_space,
             rev_space, total_space) = storagedata

            total_by_date[date_string] = {
                "total_space": total_space,
                "research_space": research_space,
                "vault_space": vault_space,
                "revision_space": rev_space
            }

    output["_group_data"] = common_data
    output["totals"] = total_by_date
    return output


def _get_cmd_stdout_lines(args) -> List[str]:
    return subprocess.run(args, stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL).stdout.decode('UTF-8').split('\n')


def main():
    data_format = detect_statistics_data_format()
    with open(outputfile, "w") as out:

        if data_format == "1.9":
            output = {group: get_relevant_group_metadata_19(
                group) for group in get_research_groups()}
        else:
            sys.exit(
                "Error: unknown statistics data format ({})".format(data_format))

        output["__DATA_FORMAT"] = detect_statistics_data_format()
        yaml.dump(output, out)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

"""This script gathers disk usage data for all unixfilesystem vault volumes,
   so that it can be processed by capacity management scripts."""

import os
import socket
import subprocess
import yaml

def get_ufs_resources(hostname):
    """Returns dictionary with unix file system resources on a particular resource host.
       Keys are resource names. Values are dictionaries with
       parent_resource_number (could be None), vault"""
    result = {}
    current_data = {}

    def _flush_current_data_if_complete():
        if ( current_data.get("type", None) in ["unixfilesystem", "unix file system"] and
             current_data.get("location", None) == hostname ):
            if ( "resource name" in current_data and
                 "vault" in current_data and
                 "type" in current_data  ):
                result[ current_data["resource name"] ] = {
                    "parent_resource_number" : current_data.get("parent", None),
                    "vault" : current_data["vault"]
                }
        current_data.clear()
        
    
    for line in _get_cmd_stdout_lines(['ilsresc', '-l']):
        if line == "----":
            _flush_current_data_if_complete()
        elif ( line.startswith("resource name:") or
               line.startswith("parent:") or
               line.startswith("vault:") or
               line.startswith("location:") or
               line.startswith("type:") ):
            ( attr, value ) = line.split(": ")
            if attr == "parent" and value == "":
                current_data[attr] = None
            else:
                current_data[attr] = value
            
    _flush_current_data_if_complete()      
    return result


def _get_cmd_stdout_lines(args):
    return subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('UTF-8').split('\n')


def get_diskspace_free(directory):
    volumedata = os.statvfs(directory)
    return volumedata.f_frsize * volumedata.f_bfree


def get_diskspace_total(directory):
    volumedata = os.statvfs(directory)
    return volumedata.f_frsize * volumedata.f_blocks


def collect_usage_data(resources):
    return { resource_name : 
        { "resource_in_tree" : "no" if resources[resource_name]["parent_resource_number"] is None else "yes",
          "diskspace_free" : get_diskspace_free(resources[resource_name]["vault"]),
          "diskspace_total" : get_diskspace_total(resources[resource_name]["vault"]) }
        for resource_name in resources
    }


def write_usage_data(data, outputfile):
    with open (outputfile, "w") as out:
        yaml.dump(data, out)


# Main
hostname = socket.getfqdn()
outputfile = "/var/yoda-financial-data/{}.capacity.yaml".format(hostname.split(".")[0])
resources = get_ufs_resources(hostname)
usage_data = collect_usage_data(resources)
write_usage_data(usage_data, outputfile)

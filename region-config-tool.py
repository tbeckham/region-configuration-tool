#!/usr/bin/python -tt

import argparse
import re
import sys
import os


def get_options():
    """
    """
    def format_error(err_string):
        msg = ("\nIncorrect Region \'key=value\' format - " + err_string + "\nPlease use "
               + "the following format: " + "\n" + "\t" +
               "region_name=ParameterValue,ip=ParameterValue," +
               "domain_name=ParameterValue") 
        return msg

    def region_check(region):
        # Check each region has correct number of parameters
        try:
            region_name, ip, domain_name = region.split(',')        
        except ValueError:
            msg = format_error(region)
            raise argparse.ArgumentTypeError(msg)
        
        # Check that each parameter is the proper key=value format
        for param in [ region_name, ip, domain_name ]:
            try:
                key_param, value_param = param.split('=')
            except ValueError: 
                msg = format_error(region)
                raise argparse.ArgumentTypeError(msg)
            
            if not any(key_param in key for key in ["region_name", "ip", "domain_name"]):
                msg = format_error(region)
                raise argparse.ArgumentTypeError(msg)

        # Check for proper length and valid region name
        region_key, region_value = region_name.split('=')
        if not re.match("^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$", region_value):
            msg = format_error(region)
            region_msg = ("\n\n" + region_key + " has a value which is not a valid DNS label." +
                          " Please refer to <label> definition for RFC 1035 " +
                          "https://www.ietf.org/rfc/rfc1035.txt.")
            raise argparse.ArgumentTypeError(msg + region_msg)
        
        # Check for proper IPv4 format      
        ip_key, ip_value = ip.split('=')
        if not re.findall(
                         r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
                         ip_value):
            msg = format_error(region)
            ip_msg = ("\n\n" + ip_key + " has a value which is not a valid IPv4 address.")
            raise argparse.ArgumentTypeError(msg + ip_msg)

        # Check for proper domain/subdomain format 
        domain_key, domain_value = domain_name.split('=')
        if not re.findall(
                         r'^[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*$',
                         domain_value):
            msg = format_error(region)
            domain_msg = ("\n\n" + domain_key + " has a value which is not a value DNS domain. " +
                          "Please refer to the <domain> definition in RFC 1035 " +
                          "https://www.ietf.org/rfc/rfc1035.txt.")
            raise argparse.ArgumentTypeError(msg + domain_msg)

        return region
                   
    parser = argparse.ArgumentParser(prog="region-config-tool.py",
                 usage='%(prog)s REGION [REGION ...] [-f | --filename] FILE_NAME',
                 description='Script that creates region configuration file from \
                 multiple region (i.e. cloud) parameters that are intended to be \
                 part of a federated environment.')
    region_group = parser.add_argument_group("Region Arguments", "Arguments to define multiple regions")
    region_group.add_argument('region', nargs='+', type=region_check, help='Region defintion; \
                              multiple regions separated by spaces; should \
                              contain the following format for each entry: \
                              region_name=ParameterValue,ip=ParameterValue,domain_name=ParameterValue.\
                              For each cloud (i.e. region) - \"region_name\" should match \
                              region.region_name cloud property; \"ip\" should be \
                              the IP of the Cloud Controller; \"domain_name\" should match the \
                              system.dns.dnsdomain cloud property')
    file_group = parser.add_argument_group("Region Configuration File Argument", 'Argument to define name of \
                                           of generated region configuration file.') 
    file_group.add_argument('-f', '--filename', dest='file_name', help="Generated region configuration file.")
    options = parser.parse_args()
    return options

if __name__ == "__main__":
    # Grab commandline options for region configuration
    options = get_options()
    print options.region

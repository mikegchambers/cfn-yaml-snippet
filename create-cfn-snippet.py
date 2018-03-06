#!/bin/python

import argparse
#import urllib2
import json
from pprint import pprint


# Input arguments:

parser = argparse.ArgumentParser(description='Create an AWS CloudfFormation TextMate Snippet file.')
parser.add_argument('--input', type=str, default="CloudFormationResourceSpecification.json",
                   help='Source (Input) file from AWS')

parser.add_argument('--output', type=str, default="yaml.json",
                   help='Output file')

#parser.add_argument('--remote', type=bool, default=False,
#                   help='Attempt to get the source file direct from AWS.')

#parser.add_argument('--url', type=str, default="https://d2stg8d246z9di.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json",
#                   help='Input web link')

args = parser.parse_args()

# Load the source data:

#if args.remote == True:
#    response = urllib2.urlopen(args.url)
#    data = response.read()
#else:
#    data = json.load(open(args.input))

data = json.load(open(args.input))

# Start the output data, add the default/extra snippets:

output = {}
output["cfn"] ={ "prefix" : "cfn", "body" : "AWSTemplateFormatVersion: 2010-09-09\r\n\r\nDescription: #String\r\n\r\nMetadata:\r\n\t#template metadata\r\n\r\nParameters:\r\n\t#set of parameters\r\n\r\nMappings:\r\n\t#set of mappings\r\n\r\nConditions:\r\n\t#set of conditions\r\n\r\nTransform:\r\n\t#set of transforms\r\n\r\nResources:\r\n\t#set of resources\r\n\r\nOutputs:\r\n\t#set of outputs\r\n", "description" : "Full template." }
output["cfn-lite"] ={ "prefix" : "cfn-lite", "body" : "AWSTemplateFormatVersion: 2010-09-09\r\n\r\nDescription: #String\r\n\r\nParameters:\r\n\t#set of parameters\r\n\r\nResources:\r\n\t#set of resources\r\n\r\nOutputs:\r\n\t#set of outputs\r\n", "description" : "Full template." }
output["metadata"] ={ "prefix" : "metadata", "body" : "", "description" : "" }
output["parameters"] ={ "prefix" : "parameters", "body" : "${1:LogicalID}:\r\n\tType: String\r\n\tDefault: t2.micro\r\n\tAllowedValues:\r\n\t\t- t2.micro\r\n\t\t- m1.small\r\n\t\t- m1.large\r\n\tDescription: Enter t2.micro, m1.small, or m1.large. Default is t2.micro.\r\n", "description" : "" }
output["mappings"] ={ "prefix" : "mappings", "body" : "${1:LogicalID}:\r\n\tKey01:\r\n\t\tName: Value01\r\n\tKey02:\r\n\t\tName: Value02\r\n\tKey03:\r\n\t\tName: Value03\r\n", "description" : "" }
output["conditions"] ={ "prefix" : "conditions", "body" : "${1:LogicalID}:\r\n\tIntrinsic function\r\n", "description" : "" }
output["transforms"] ={ "prefix" : "transforms", "body" : "", "description" : "" }
output["outputs"] ={ "prefix" : "outputs", "body" : "${1:LogicalID}:\r\n\tDescription: Information about the value\r\n\tValue: Value to return\r\n\tExport:\r\n\t\tName: Value to export\r\n", "description" : "" }

# Add the resources to the output

for d in data['ResourceTypes']:

    prefix = d.replace('AWS::', "")
    prefix = prefix.replace('::', "-")
    prefix = prefix.lower()

    body = ""
    description = ""
    scope = "source.cloudformation"

    body = body + ( '${1:LogicalID}:\r\n' )

    # add a name placeholder
    body = body + ( '\tType: \"' + d + '\"\r\n' )
    body = body + ( "\tProperties:\r\n")

    description = description + d + "\r\n" + data['ResourceTypes'][d]['Documentation']

    # for each resources 'properties':
    for p in data['ResourceTypes'][d]['Properties']:

        required = data['ResourceTypes'][d]['Properties'][p]['Required']

        item = ""
        itemList = 0


        if ( 'PrimitiveType' in data['ResourceTypes'][d]['Properties'][p] ):
            item = data['ResourceTypes'][d]['Properties'][p]['PrimitiveType']
 
        if ( 'PrimitiveItemType' in data['ResourceTypes'][d]['Properties'][p] ):
            item = data['ResourceTypes'][d]['Properties'][p]['PrimitiveItemType']
 

        if ( 'ItemType' in data['ResourceTypes'][d]['Properties'][p] ):
            item = data['ResourceTypes'][d]['Properties'][p]['ItemType']

        if ( 'Type' in data['ResourceTypes'][d]['Properties'][p] ):
            if ( data['ResourceTypes'][d]['Properties'][p]['Type'] == "List" ):
                itemList = 1
            else:
                itemList = 2
                item = data['ResourceTypes'][d]['Properties'][p]['Type']

        ###########################

        if (itemList == 0):
            body = body +  ( "\t\t" + p + ": " + item + "" )
            if (required):
                body = body + ( " #required\r\n" )
            else:
                body = body + ( "\r\n" )


        elif (itemList == 1):
            body = body +  ( "\t\t" + p + ":" + "" )
            if (required):
                body = body + ( " #required\r\n" )
            else:
                body = body + ( "\r\n" )

            body = body +  ( "\t\t\t- " + item + "\r\n")



        elif (itemList == 2):
            body = body +  ( "\t\t" + p + ":" + "" )
            if (required):
                body = body + ( " #required\r\n" )
            else: 
                body = body + ( "\r\n" )

            body = body +  ( "\t\t\t" + item + "\r\n")
        
        output[d] ={ "prefix" : prefix, "body" : body, "description" : description }

#print( json.dumps(output) )

with open(args.output, "w") as text_file:
    text_file.write( json.dumps(output, indent=4 ))
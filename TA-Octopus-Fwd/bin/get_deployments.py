# $Id: get_deployments.py 2016-12-27 $
# Author: Coen Meerbeek <coen@buzzardlabs.com>
# Copyright: BuzzarLabs 2016

"""
This file retrieves deployments from an Octopus application
"""

import logging, json, requests, time, sys
import ConfigParser
import splunk.Intersplunk as isp
import octopus_common

# Parse octopus.conf for configuration settings
stanza = octopus_common.getSelfConfStanza("octopus")
protocol = stanza['protocol']
hostname = stanza['hostname']
apikey   = stanza['apikey']

# Setup logger object
logger = octopus_common.setup_logging()
logger.info(time.time())

try:
  octopus_url = protocol + "://" + hostname + "/api/deployments/"
  last_deployment_id = octopus_common.readCheckPoint("deployments")

  while True:
    # Setup response object and execute GET request
    response = requests.get(
      url = octopus_url,
      headers = {
        "X-Octopus-ApiKey": apikey,
      },
    )
    response.raise_for_status()

    # Handle response
    json_response = json.loads(response.content)

    # Get deployment ID from first deployment returned by the API which is the most recent deployment
    try:
      if json_response['Links']['Page.Current'].split('=')[1][:1] == '0': 
        deployment_id = json_response['Items'][0]['Id'].split('-')[1]       
        octopus_common.writeCheckPoint("deployments", deployment_id)        
    except Exception:
      break

    # Iterate deployments and print results to Splunk if it hasn't been printed before
    for deployment in json_response['Items']:
      # Get deployment ID
      deployment_id = deployment['Id'].split('-')[1]

      if int(deployment_id) > int(last_deployment_id):
        print json.dumps(deployment)

    # Try to get next page if available, else write most recent deployment id and exit
    try:
      octopus_url = protocol + "://" + hostname + json_response['Links']['Page.Next']
    except Exception:
      break

  sys.exit(0)

# Catch exceptions if needed
except Exception as e:
  logger.exception("Exception: " + str(e))
  isp.generateErrorResults(str(e))
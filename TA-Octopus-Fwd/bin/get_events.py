# $Id: get_events.py 2016-12-27 $
# Author: Coen Meerbeek <coen@buzzardlabs.com>
# Copyright: BuzzarLabs 2016

"""
This file retrieves events from an Octopus application
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
  octopus_url = protocol + "://" + hostname + "/api/events/"
  last_event_id = octopus_common.readCheckPoint("events")

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

    # Get event ID from first event returned by the API which is the most recent event
    try:
      if json_response['Links']['Page.Current'].split('=')[1][:1] == '0':
        event_id = json_response['Items'][0]['Id'].split('-')[1]
        octopus_common.writeCheckPoint("events", event_id)
    except Exception:
      break

    # Iterate events and print results to Splunk if it hasn't been printed before
    for event in json_response['Items']:
      event_id = event['Id'].split('-')[1]

      # If event_id is smaller or equal to checkpoint exit
      if int(event_id) <= int(last_event_id):
        break

      print json.dumps(event)

    # Try to get next page if available, else exit
    try:
      octopus_url = protocol + "://" + hostname + json_response['Links']['Page.Next']
    except Exception:
      break
  
  sys.exit(0)

# Catch exceptions if needed
except Exception as e:
  logger.exception("Exception: " + str(e))
  isp.generateErrorResults(str(e))
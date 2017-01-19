# $Id: get_tasks.py 2016-12-27 $
# Author: Coen Meerbeek <coen@buzzardlabs.com>
# Copyright: BuzzarLabs 2016

"""
This file retrieves tasks from an Octopus application
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
  octopus_url = protocol + "://" + hostname + "/api/tasks/"
  last_task_id = octopus_common.readCheckPoint("tasks")

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

    # Get task ID from first task returned by the API which is the most recent task
    try:
      if json_response['Links']['Page.Current'].split('=')[1][:1] == '0': 
        task_id = json_response['Items'][0]['Id'].split('-')[1]       
        octopus_common.writeCheckPoint("tasks", task_id)        
    except Exception:
      break

    # Iterate tasks and print results to Splunk if it hasn't been printed before
    for task in json_response['Items']:
      # Get task ID
      task_id = task['Id'].split('-')[1]

      if int(task_id) > int(last_task_id):
        print json.dumps(task)

    # Try to get next page if available
    try:
      octopus_url = protocol + "://" + hostname + json_response['Links']['Page.Next']
    except Exception:
      break

  sys.exit(0)

# Catch exceptions if needed
except Exception as e:
  logger.exception("Exception: " + str(e))
  isp.generateErrorResults(str(e))
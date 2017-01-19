# $Id: octopus_common.py 2016-12-17 $
# Author: Coen Meerbeek <coen@buzzardlabs.com>
# Copyright: BuzzardLabs 2016

"""
This file has common functions for interacting with Splunk 
for use in the Octopus TA integrations.
"""

import ConfigParser
import os, logging, sys
import splunk.bundle as sb
import splunk.Intersplunk as isp
from splunk.clilib import cli_common as cli
import splunk

def setup_logging():
  """
  Setup logging

  Log is written to /opt/splunk/var/log/splunk/octopus.log
  """
  logger = logging.getLogger('splunk.octopus')    
  SPLUNK_HOME = os.environ['SPLUNK_HOME']
    
  LOGGING_DEFAULT_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log.cfg')
  LOGGING_LOCAL_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log-local.cfg')
  LOGGING_STANZA_NAME = 'python'
  LOGGING_FILE_NAME = "octopus.log"
  BASE_LOG_PATH = os.path.join('var', 'log', 'splunk')
  LOGGING_FORMAT = "%(asctime)s %(levelname)-s\t%(module)s:%(lineno)d - %(message)s"
  
  splunk_log_handler = logging.handlers.RotatingFileHandler(os.path.join(SPLUNK_HOME, BASE_LOG_PATH, LOGGING_FILE_NAME), mode='a') 
  splunk_log_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
  logger.addHandler(splunk_log_handler)
  splunk.setupSplunkLogger(logger, LOGGING_DEFAULT_CONFIG_FILE, LOGGING_LOCAL_CONFIG_FILE, LOGGING_STANZA_NAME)
  
  return logger

def getSelfConfStanza(stanza):
  appdir = os.path.dirname(os.path.dirname(__file__))
  apikeyconfpath = os.path.join(appdir, "default", "octopus.conf")
  apikeyconf = cli.readConfFile(apikeyconfpath)
  localconfpath = os.path.join(appdir, "local", "octopus.conf")
  
  if os.path.exists(localconfpath):
    localconf = cli.readConfFile(localconfpath)
    for name, content in localconf.items():
      if name in apikeyconf:
        apikeyconf[name].update(content)
      else:
        apikeyconf[name] = content
  
  return apikeyconf[stanza]

def writeCheckPoint(sourcetype, checkpoint):
  appdir = os.path.dirname(os.path.dirname(__file__))
  last_eventid_filepath = os.path.join(appdir, "local", "octopus-" + sourcetype + ".chk")

  try:
    last_eventid_file = open(last_eventid_filepath,'w')
    last_eventid_file.write(checkpoint)
    last_eventid_file.close()   
  except IOError:
    sys.stderr.write('Error: Failed to write last_eventid to file: ' + last_eventid_filepath + '\n')
    sys.exit(2)

def readCheckPoint(sourcetype):
  appdir = os.path.dirname(os.path.dirname(__file__))
  last_eventid_filepath = os.path.join(appdir, "local", "octopus-" + sourcetype + ".chk")
  checkpoint = 0;

  if os.path.isfile(last_eventid_filepath):
    try:
      last_eventid_file = open(last_eventid_filepath,'r')
      checkpoint = int(last_eventid_file.readline())
      last_eventid_file.close()   
    except IOError:
      sys.stderr.write('Error: Failed to read last_eventid file, ' + last_eventid_filepath + '\n')
      sys.exit(2)
  else:
    sys.stderr.write('Warning: ' + last_eventid_filepath + ' file not found! Starting from zero. \n')

  return checkpoint
# Splunk Add-on for Octopus

The Splunk Add-On for Octopus is a technology add-on for retrieving data from a Octopus Deployment installation. This Add-On only provides input related configuration files. Dashboards and reports are build in the app "Octopus for Splunk".

## Getting Started

You must have an installed and configured Octopus application to complete the setup process of this app. If you have any questions regarding this app please contact [me](mailto:coen@buzzardlabs.com).

### Install Prerequisites

Too make sure everything works correctly make sure the following is available and working:

1. A working Octopus application
2. Access to the REST API port on the Octopus server from a Heavy Forwarder or Splunk single instance (port 80 for HTTP and port 443 for HTTP or else if configured differently)
3. An API key to retrieve data from Octopus. See [Octopus Wiki](https://github.com/OctopusDeploy/OctopusDeploy-Api/wiki).
4. A Splunk Heavy Forwarder or Single Instance with Splunk 6.0.x or higher

### Install instructions

The Splunk Add-On for Octopus contains three apps:
- TA-Octopus-Idx > Contains index configuration and index-time configurations
- TA-Octopus-Fwd > Contains all the inputs which retrieve the data
- TA-Octopus-Sh > Contains all search-time configurations

Installation of the apps can be done using the Splunk UI as explained below. If you have an index cluster please install TA-Octopus-Idx using the following instructions on [Splunk Docs](https://docs.splunk.com/Documentation/Splunk/latest/Indexer/Manageappdeployment). For search-head cluster please install TA-Octopus-Sh using the following instruction on [Splunk Docs](http://docs.splunk.com/Documentation/Splunk/6.5.1/DistSearch/PropagateSHCconfigurationchanges).

**Install using Splunk UI:**

1. Select "Manage Apps" from the Apps dropdown.
2. Select the "Install app from file" button.
3. Select the generated `TA-Octopus-<Idx|Fwd|Sh>.spl` package.
4. Splunk will walk you through all required setup.

## Data Imported

Data is automatically imported to a custom `octopus` index once the app is enabled.

The following sourcetypes are available:
* octopus:machines
* octopus:projects
* octopus:releases
* octopus:deployments
* octopus:events
* octopus:environments
* octopus:users
* octopus:tasks

## ChangeLog

See [CHANGELOG](CHANGELOG.md) for details.

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

## TODO

* Convert Add-On to Modular Input
 
## Copyright

Copyright (c) 2016 Coen Meerbeek. See [LICENSE](LICENSE) for details.

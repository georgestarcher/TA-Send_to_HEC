## Custom Alert Action Search Results to HTTP Event Collector 

Author: George Starcher (starcher)
Email: george@georgestarcher.com

## Overview

This is a Splunk Modular Alert used to send the search results to Splunk HTTP Event Collector.
It has been built using the Add-on Builder for Splunk to improve compatibility with things like Splunk Enterprise Security Adaptive Response.

This is meant to send a modest number of events from one Splunk instance to another using HEC. Although the code is threaded it is not meant for high volume or real time sending of data.

**All materials in this project are provided under the MIT software license. See license.txt for details.**

## Dependencies

* Splunk 6.3+
* Supported on Windows, Linux, MacOS, Solaris, FreeBSD, HP-UX, AIX
* A Splunk receiving instance with HTTP Event Collector configured.
* The HTTP Event Collector token

## Setup

* Install to your $SPLUNK_HOME/etc/apps directory
* Restart Splunk


## Using

Perform a search in Splunk and then navigate to : Save As -> Alert -> Trigger Actions -> Add Actions -> Send to HEC 

On this dialogue you can enter the Splunk server and HTTP Event Collector token.

The fields _time, index, source, sourcetype and _raw are pulled from the search results and used in constructing the HEC payload. If you wish to override these fields for a different value at the destination you should set them in the alert gui settings. _time still comes from the event time.

The alert defaults to taking the JSON of the search results to form the payload sent to HEC. All _ hidden fields are removed. If you want _raw then just eval it to another field like orig_raw. You now have the option to select RAW as the HEC methodwhen configuring the alert. This ignores all fields except _raw which it sends to the HEC receiver. With RAW the HEC receiver determines the parsing, and index time fields.

Keep in mind that credentials stored in a Modular Alert are NOT encrypted. And users with permissions to the saved alert can view them. The Add-on builder obscures the stored API key but it is still unencrypted in the conf file.

## Logging

Browse to : Settings -> Alert Actions -> Send to HEC -> View Log Events

Or you can search directly in Splunk : index=_internal sourcetype=splunkd component=sendmodalert action="sendtohec"



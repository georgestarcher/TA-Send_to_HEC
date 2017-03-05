
# encoding = utf-8

def process_event(helper, *args, **kwargs):
    """
    # IMPORTANT
    # Do not remove the anchor macro:start and macro:end lines.
    # These lines are used to generate sample code. If they are
    # removed, the sample code will not be updated when configurations
    # are updated.

    [sample_code_macro:start]

    # The following example gets the alert action parameters and prints them to the log
    u_splunkserver = helper.get_param("u_splunkserver")
    helper.log_info("u_splunkserver={}".format(u_splunkserver))

    u_splunkserverport = helper.get_param("u_splunkserverport")
    helper.log_info("u_splunkserverport={}".format(u_splunkserverport))

    u_hectoken = helper.get_param("u_hectoken")
    helper.log_info("u_hectoken={}".format(u_hectoken))

    u_senddatatype = helper.get_param("u_senddatatype")
    helper.log_info("u_senddatatype={}".format(u_senddatatype))

    u_destindex = helper.get_param("u_destindex")
    helper.log_info("u_destindex={}".format(u_destindex))

    u_destsourcetype = helper.get_param("u_destsourcetype")
    helper.log_info("u_destsourcetype={}".format(u_destsourcetype))

    u_host = helper.get_param("u_host")
    helper.log_info("u_host={}".format(u_host))

    u_destsource = helper.get_param("u_destsource")
    helper.log_info("u_destsource={}".format(u_destsource))


    # The following example adds two sample events ("hello", "world")
    # and writes them to Splunk
    # NOTE: Call helper.writeevents() only once after all events
    # have been added
    helper.addevent("hello", sourcetype="sample_sourcetype")
    helper.addevent("world", sourcetype="sample_sourcetype")
    helper.writeevents(index="summary", host="localhost", source="localhost")

    # The following example gets the events that trigger the alert
    events = helper.get_events()
    for event in events:
        helper.log_info("event={}".format(event))

    # helper.settings is a dict that includes environment configuration
    # Example usage: helper.settings["server_uri"]
    helper.log_info("server_uri={}".format(helper.settings["server_uri"]))
    [sample_code_macro:end]
    """

    try:
        from splunk_http_event_collector import http_event_collector
        import json
    except ImportError as err_message:
        helper.log_error("{}".format(err_message))
        return 1
        
    helper.log_info("Alert action sendtohec started.")

    u_splunkserver = helper.get_param("u_splunkserver")
    u_splunkserverport = helper.get_param("u_splunkserverport")
    helper.log_info("splunkserver={0}:{1}".format(u_splunkserver,u_splunkserverport))

    u_hectoken = helper.get_param("u_hectoken")
    helper.log_info("u_hectoken={}".format(u_hectoken))

    u_senddatatype = helper.get_param("u_senddatatype")
    helper.log_info("u_senddatatype={}".format(u_senddatatype))

    u_destindex = helper.get_param("u_destindex")
    u_destsourcetype = helper.get_param("u_destsourcetype")
    u_host = helper.get_param("u_host")
    u_destsource = helper.get_param("u_destsource")

    searchResults = helper.get_events()

    if searchResults is None:
        helper.log_error("FATAL Empty Search Results, nothing to send.")
        return 1

    if u_senddatatype=="raw":
        destCollector = http_event_collector(u_hectoken, u_splunkserver, 'raw', '', u_splunkserverport)
    else:
        destCollector = http_event_collector(u_hectoken, u_splunkserver, 'json', '', u_splunkserverport)

    if u_senddatatype=="raw":
        for entry in searchResults:
            payload = entry.get('_raw')
            destCollector.batchEvent("{}".format(payload))
        destCollector.flushBatch()
        helper.log_info("Alert action sendtohec completed.")
        return 0
            
    for entry in searchResults:

        payload = {}
        if u_destindex:
            payload['index'] = u_destindex
        else: 
            payload['index'] = entry.get('index')
        if u_destsourcetype:
            payload['sourcetype'] = u_destsourcetype
        else:
            payload['sourcetype'] = entry.get('sourcetype')
        if u_destsource:
            payload['source'] = u_destsource
        else:
            payload['source'] = entry.get('source')
        if u_host:
            payload['host'] = u_host
        else:
            payload['host'] = entry.get('host')
        payload['time'] = entry.get('_time')
        if 'index' in entry: entry.pop('index')
        if 'sourcetype' in entry: entry.pop('sourcetype')
        if 'source' in entry: entry.pop('source')
        if 'host' in entry: entry.pop('host')

        entry = {k:entry.get(k) for k,v in entry.items() if not k.startswith('_')}
        
        payload['event'] = json.dumps(entry)
            
        destCollector.batchEvent(payload)

    destCollector.flushBatch()
    helper.log_info("Alert action sendtohec completed.")
    
    return 0

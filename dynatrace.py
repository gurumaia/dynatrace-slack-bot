#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import requests
from requests.auth import HTTPBasicAuth
from slackclient import SlackClient
import xml.etree.ElementTree as ET
import re
import datetime


def get_dynatrace_data(dashboard, timeframe):
    """
        Calls Dynatrace API to get information from dashboard and return the raw data.
    """
    user = os.environ.get('DYNATRACE_USER')
    password = os.environ.get('DYNATRACE_PASSWORD')

    auth = HTTPBasicAuth(user,password)

    url=os.environ.get("DYNATRACE_URL")
    api="/rest/management/reports/create/"+dashboard
    query="?type=xml&filter=tf:OffsetTimeframe?"+str(timeframe)+":SECONDS"

    response = requests.get(url+api+query,verify=False, auth=auth)
    print response.content
    if response.status_code == 200:
        return response
    else:
        raise 'Error talking to dynatrace' # I think this will cause problems

def get_dashboard_chart(dashboard,timeframe):
    """
        Gets information from a dashboard containing various single axis chart dashlets.
        This is the horrible part of the code that should be completely refactored.
        There are a whole bunch of assumptions that will not hold true for everyone.
    """
    dashboard_data = get_dynatrace_data(dashboard, timeframe)
    table='-------------------------------------------------------------------------------\n'
    root = ET.fromstring(dashboard_data.content)
    data = list(root.find('data'))
    for dashlet in data:
        measurelist = list(dashlet)
        measures = list(measurelist[0])
        measurename = re.search('^([^-]*)',measures[0].get('measure')).group(0)
        unit = measures[0].get('unit')

        row_format = "| {}{:>9} | {:>45} | {:>15} |\n"
        table += row_format.format("", *['time',measurename,'value ('+unit+')'])

        for measure in measures:
            measurement = measure.find('measure').findall('measurement')[-1]
            rawname = measure.get('measure')
            processedname = re.search('^.* - ([a-zA-Z_]+\[[^]]*\]).*',rawname)
            split=processedname.group(1)
            time=datetime.datetime.fromtimestamp(int(measurement.get('timestamp'))/1000).strftime('%H:%M:%S')
            value=measurement.get('avg')
            try:
                val=str("%.2f" % float(value))
            except:
                val=value
            table += row_format.format("", *[str(time),split,val])
        table += '-------------------------------------------------------------------------------\n'
    return table

def get_dashboard_dualchart(dashboard,timeframe):
    """
        Gets information from a dashboard containing various single axis chart dashlets.
        This is the second horrible part of the code that should be completely refactored.
        There are a whole bunch of assumptions that will not hold true for everyone.
    """
    dashboard_data = get_dynatrace_data(dashboard, timeframe)
    root = ET.fromstring(dashboard_data.content)
    data = list(root.find('data'))
    table=''
    for dashlet in data:
        measureslist = list(dashlet)
        for measures in measureslist:
            for measure in measures:
                if len(measure) > 0:
                    measurename = measure.get('measure')
                    unit = measure.get('unit')
                    row_format = "| {}{:>17} | {:>13} |\n"
                    table+= '--------- '+measurename+' ---------\n'
                    table+='-------------------------------------\n'
                    table += row_format.format("", *['time','value ('+unit+')'])
                    total = 0
                    val = 0
                    for measurement in measure:
                        value=measurement.get('sum')
                        try:
                            val = float(value)
                            total += val
                        except:
                            print 'Oh Shit!'
                    time=datetime.datetime.fromtimestamp(int(measure[0].get('timestamp'))/1000).strftime('%y-%m-%d %H:%M:%S')
                    table += row_format.format("", *[time,total])
                    table+='-------------------------------------\n'
    return table

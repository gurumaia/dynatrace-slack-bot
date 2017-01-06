#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dynatrace

dashboards = {
    'command': {
        'name': 'Dashboard%20Name',
        'timeframe': 900,
        'function': dynatrace.get_dashboard_chart
    },
    'command2': {
        'name': 'Other%20Dashboard%20Name',
        'timeframe': 900,
        'function': dynatrace.get_dashboard_dualchart
    }
}

import plotly
import pandas as pd
import plotly.graph_objs as go

from collections import OrderedDict
from datetime import datetime, timezone, timedelta

from .base import get_client

POSSIBLE_STATISTICS = {'SampleCount', 'Average', 'Sum', 'Minimum', 'Maximum'}


def plot_metric(namespace, metric_name, **kwargs):
    client = get_client('cloudwatch', **kwargs)
    statistics = 'Average'  # default stat we'll be using for plotting
    markers = kwargs.get('markers', [])

    if kwargs.get('start_time') and not isinstance(kwargs.get('start_time'), datetime):
        raise ValueError('start_time argument should be of type datetime.datetime')

    if kwargs.get('end_time') and not isinstance(kwargs.get('end_time'), datetime):
        raise ValueError('end_time argument should be of type datetime.datetime')

    if kwargs.get('statistics'):
        statistics = kwargs.get('statistics')

        if not isinstance(statistics, str):
            raise ValueError('statistics argument should be a string')

        if statistics not in POSSIBLE_STATISTICS:
            raise ValueError('Invalid statistics argument. statistics can only take following values: %s', POSSIBLE_STATISTICS)

    if kwargs.get('dimensions') and not isinstance(kwargs.get('dimensions'), list):
        raise ValueError('Cloudwatch Metric Dimensions should be specificed as a list.')

    if not isinstance(markers, list):
        raise ValueError('Markers should be of type list')

    dimensions = kwargs.get('dimensions') or []
    utc_dt = datetime.now(timezone.utc)  # UTC time
    default_end_time = utc_dt.astimezone()
    end_time = kwargs.get('end_time') or default_end_time
    default_start_time = end_time - timedelta(seconds=3600 * 12)
    start_time = kwargs.get('start_time') or default_start_time

    for marker in markers:

        if not isinstance(marker, datetime):
            raise ValueError('Marker %s should be of type datetime.datetime' % marker)

    # ignore markers not falling between start and end time
    markers = [marker for marker in markers if (start_time <= marker <= end_time)]

    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Dimensions=dimensions,
        Period=300,
        Statistics=[statistics],
    )
    ds = response['Datapoints']

    if not ds:
        raise ValueError('No metric data received from cloudwatch. Make sure that the resource exist. Check namespace, metric name, dimensions, region.')

    title = namespace + ' ' + metric_name
    ds2 = {}
    max_timestamp = ds[0]['Timestamp']
    max_value = ds[0][statistics]

    for d in ds:
        new_val = d[statistics]
        ds2[d['Timestamp']] = new_val

        if new_val > max_value:
            max_timestamp = d['Timestamp']
            max_value = new_val

    ds3 = OrderedDict(sorted(ds2.items(), key=lambda t: t[0]))
    ds4 = pd.DataFrame.from_dict(ds3, orient="index")
    ds4.index.name = 'timestamp'
    ds4.columns = ['count']

    plotly.offline.init_notebook_mode(connected=True)
    data = [go.Scatter(x=ds4.index.tolist(), y=ds4['count'].tolist(), name=title)]

    # let's draw marker lines
    shapes = []

    for marker in markers:
        shapes.append({
            'type': 'line',
            'x0': marker,
            'y0': 0,
            'x1': marker,
            'y1': max_value,
            'line': {
                'color': 'rgb(50, 171, 96)',
                'width': 4,
                'dash': 'dashdot',
            }
        })

    layout = {
        'title': title,
        'shapes': shapes
    }

    plotly.offline.iplot({
        "data": data,
        "layout": layout,
    })

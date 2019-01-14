#!/usr/bin/python3
#
# Create a summary of a machine observation dataset, aggregating observations by day and calculating the footprint of those observations.
#

import os, time
import pandas as pd
from shapely.geometry import MultiPoint

# Calculate all aggregations.
def aggregate_occurrences(group):

    # Create collections of all points in this group
    lats = group['decimalLatitude']
    lngs = group['decimalLongitude']
    points = list(zip(lngs, lats))
    all_points = MultiPoint(points)

    # Calculate centroid. Possible improvement: add an uncertainty, or move this to a point the animal was actually observed at
    centroid = all_points.centroid
    # Calculate the footprint. Possible improvement: add uncertainties of points; make sure this is always a polygon and not just a point or line
    footprint = all_points.convex_hull

    # Calculate and format date range for this group.
    earliest_date = group['eventDate'].min()
    latest_date = group['eventDate'].max()
    if (earliest_date == latest_date):
        event_date_range = earliest_date.isoformat() + 'Z'
    else:
        event_date_range = group['eventDate'].min().isoformat() + 'Z/' + group['eventDate'].max().isoformat() + 'Z'

    # Occurrence id chosen based on the date.  Consider carefully what it should be.
    occurrence_id = ":".join(group['occurrenceID'].min().split(":")[0:2]) + ':' + earliest_date.strftime('%Y-%m-%d')

    # Minimum row numbers (from the order of the original CSV) form an index, so the output CSV is in the same order as the input.
    row_number = group['___row_index'].min()

    return pd.Series([event_date_range, footprint.wkt, centroid.y, centroid.x, occurrence_id, row_number],
                     index=['eventDateRange', 'footprintWKT', 'decimalLatitude', 'decimalLongitude', 'occurrenceID', '___row_index'])

# I'm not sure how the group-by-date thing works, this might or might not do anything useful.
os.environ['TZ'] = 'UTC'

# Read in the data
occ = pd.read_csv("occurrence.txt", sep='\t', lineterminator='\r', parse_dates=['eventDate'], infer_datetime_format=True, na_filter=False)

# Add an index, so the data can be kept in order.
occ['___row_index'] = pd.np.arange(len(occ))

# print(occ)

# Group by day, other columns are included so they are available to output.
agg_occurrences = occ.groupby([pd.Grouper(freq='1d',key='eventDate'),'id','type','license','datasetID','basisOfRecord','occurrenceRemarks','sex','lifeStage','reproductiveCondition','organismName','samplingProtocol','geodeticDatum','scientificNameID','scientificName','taxonRank']).apply(aggregate_occurrences)

# Column order of DWC meta file.
output_columns=['id','type','license','datasetID','basisOfRecord','occurrenceID','occurrenceRemarks','sex','lifeStage','reproductiveCondition','organismName','samplingProtocol','eventDateRange','decimalLatitude','decimalLongitude','geodeticDatum','scientificNameID','scientificName','taxonRank','footprintWKT']

# print(agg_occurrences)

# Output to CSV; format latitude and longitude with specified precision.
agg_occurrences.sort_values(by=['___row_index']).reset_index()[output_columns].to_csv("aggregated-occurrences.txt", sep='\t', index=False, line_terminator='\r', float_format='%.6f')

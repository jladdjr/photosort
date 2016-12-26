#!/usr/bin/env python

# 1. Get general configuration

# Locate import folder

# Locate library

# 2. Prepare to sort

# Flatten folder if necessary

# 3. Sort

# for each event

    # given remaining set of photos, use photo meta-data to 
    # form group of photos representing next event

    # get type of event

    # get any additional information required for
    # event type

    # move event to library


import os
import datetime
import subprocess
import time  # Todo: remove

def get_library_location():
    return '/Users/jladd/Desktop/imported_photos'

def get_photos_metadata(library_path):
    # TODO: Confirm that library path is accessible

    photo_metadata = []
    for file in os.listdir(library_path):
        # TODO: Filter out files that do not match list of
        # recognized file types

        stat = os.stat(os.path.join(library_path, file))
        timestamp = stat.st_mtime # creation time

        dt = datetime.datetime.fromtimestamp(timestamp)
        time = (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        photo_metadata.append((timestamp, time, library_path + '/' + file))

    photo_metadata.sort(key=lambda md: md[0]) # sort by timestamp
    return photo_metadata

def _get_timedelta_in_minutes(delta):
    """http://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python"""
    gap_in_seconds = 24 * 60 * 60 * delta.days + delta.seconds
    return divmod(gap_in_seconds, 60)[0]
    

def find_natural_break(photos_metadata, start=0):
    # Note: assumes metadata has already been sorted

    PHOTO_SESSION_TIMEOUT = 20  # In minutes

    index = start
    while index + 1 < len(photos_metadata):
        current_photo = datetime.datetime.fromtimestamp(photos_metadata[index][0])
        next_photo = datetime.datetime.fromtimestamp(photos_metadata[index + 1][0])
        gap = next_photo - current_photo
        gap_in_minutes = _get_timedelta_in_minutes(gap)

        if gap_in_minutes > PHOTO_SESSION_TIMEOUT:
            return index + 1
        index += 1

    return None

def _print_photo_metadata(photo_metadata):
    print('{0[1]} - {0[2]}'.format(photo_metadata))

def show_natural_breaks(photos_metadata):
    if not len(photos_metadata):
        return

    #_print_photo_metadata(photos_metadata[0])

    index = 0
    while True:
        break_index = find_natural_break(photos_metadata, start=index)
        if not break_index:
            break
        _print_photo_metadata(photos_metadata[break_index])
        subprocess.call(['open', photos_metadata[break_index][2]]) 
        index = break_index
        time.sleep(5)

library_path = get_library_location()
import_photos_metadata = get_photos_metadata(library_path)
show_natural_breaks(import_photos_metadata)

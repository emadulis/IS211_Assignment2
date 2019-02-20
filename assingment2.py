#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Week2 module"""

import urllib2
import csv
import datetime
import logging
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help="Enter a URL linking to a .csv file.")
args = parser.parse_args()

logging.basicConfig(filename='errors.log', level=logging.ERROR)
logger = logging.getLogger('assignment2')


def downloadData(url):
    """Function fetches csv data.
    Args:
        url(str): url where contents is found.
    
    Returns:
           url_file: A link to an datafile.
    """
    url_file = urllib2.urlopen(url)
    return url_file


def processData(url_file):
    """Retrieves contents and created a new dictionary.
        Args:
            csv_file: contents 
            my_dict: new dictionary of contents
            date_format: formate used to display contents
        Return:
            A new dictionsary with contents (id, name, bday)
        """
    readcsv = csv.DictReader(url_file)
    newfile = {}

    for num, line in enumerate(readcsv):
        try:
            born = datetime.datetime.strptime(line['birthday'], '%d/%m/%Y')
            newfile[line['id']] = (line['name'], born)
        except:
            logging.error('Error processing line #{} for ID# {}'.format(
                num, line['id']))

    return newfile


def displayPerson(id, personData):
    """Function display the output from CSV file."""
    
    name_id = str(id)
    if name_id in personData.keys():
        print 'Person #{} is {} with a birthday of {}'.format(
            id, personData[name_id][0],
            datetime.datetime.strftime(personData[name_id][1], '%Y-%m-%d'))
    else:
        print 'No user found with that ID.'


def main():
    """This function downloadData, processData, and displayPerson."""

    if args.url:
        url_data = downloadData(args.url)
        personData = processData(url_data)
        message = 'Please enter an ID #. Enter 0 or a negative # to exit. '

        while True:
            try:
                user = int(raw_input(message))
            except ValueError:
                print 'Invalid input. Please try again.'
                continue
            if user > 0:
                displayPerson(user, personData)
            else:
                print 'Thank you.'
                sys.exit()
    else:
        print 'Please use --url parameter'

if __name__ == '__main__':
    main()

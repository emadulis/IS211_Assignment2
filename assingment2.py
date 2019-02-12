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
           url_file(various): A variable linked to an applicable datafile found at
           the supplied URL, if valid.
    Example:
        >>> downloaddata('https://s3.amazonaws.com/cuny-is211-spring2015
        /birthdays100.csv')
        <addinfourl at 3043697004L whose fp = <socket._fileobject object at
        0xb5682f6c>>
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
    """Looks up the id number and returns the name and
       date of birth associated with the id number.
       Args:
           id(int, str): The number to be checked against the dictionary and
           return the associated person.
           persondata(dict): A dictionary containing a tuple of the username
           and date of birth.
        Returns:
            (str): A string displaying either the person and date of birth which
            which corresponds with the input id number, or a string indicating
            the id is not associated with anyone in the supplied dictionary.
        Examples:
            >>>Please enter an ID# for lookup:1
               Person #1 is Charles Paige with a birthday of 1963-01-06
            >>>Please enter an ID# for lookup:2
               Person #2 is Andrew Bell with a birthday of 1972-03-29
            >>>Please enter an ID# for lookup:3
               Person #3 is Charles Reid with a birthday of 2009-06-14
        """
    name_id = str(id)
    if name_id in personData.keys():
        print 'Person #{} is {} with a birthday of {}'.format(
            id, personData[name_id][0],
            datetime.datetime.strftime(personData[name_id][1], '%Y-%m-%d'))
    else:
        print 'No user found with that ID.'


def main():
    """This function downloadData, processData, and displayPerson into one program to
    be run from the command line.
    """
    if not args.url:
        raise SystemExit
    try:
        url_data = downloadData(args.url)
    except urllib2.URLError:
        print 'Please enter a valid URL.'
        raise
    else:
        personData = processData(url_data)
        chooseid = raw_input('Please enter an ID# for lookup:')
        print chooseid
        chooseid = int(chooseid)
        if chooseid <= 0:
            print 'Number equal to or less than zero entered. Exiting program.'
            raise SystemExit
        else:
            displayPerson(chooseid, personData)
            main()

if __name__ == '__main__':
    main()

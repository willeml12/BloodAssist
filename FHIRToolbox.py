#!/usr/bin/env python3

# Copyright (c) 2024, Sebastien Jodogne, ICTEAM UCLouvain, Belgium
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import requests


# Class that implements an iterator of a FHIR search result
class FHIRCursor:

    # Construct an iterator given the URL for the search, together
    # with an optional set of GET arguments
    def __init__(self, url, args = {}):
        self.entries = None
        self.next_url = url
        self.next_args = args

    # This method returns the list of entries that have been currently
    # retrieved by the iterator. This method cannot be called before
    # calling "read_next()".
    def get_entries(self):
        if self.entries == None:
            raise Exception('You first have to call "read_next()"')
        else:
            return self.entries

    # Returns true iff. the iterator has reached the end of the search result
    def is_done(self):
        return (self.next_url == None)

    # Query the FHIR server for the next page of search results
    def read_next(self):
        if self.is_done():
            raise Exception('Cursor has reached the end')
        else:
            r = requests.get(self.next_url, params = self.next_args)
            r.raise_for_status()
            
            answer = r.json()
            
            self.entries = answer.get('entry', [])
            
            n = list(filter(lambda x: x['relation'] == 'next', answer['link']))
            if len(n) == 0:
                self.next_url = None
            elif len(n) == 1:
                self.next_url = n[0]['url']
                self.next_args = {}
            else:
                assert(False)


# Given one Observation resource or one item in the "component" field
# of some Observation resource, retrieve the name of the observed
# parameter.
def get_observed_parameter_name(resource):
    code = resource.get('code', {})
    name = code.get('text')
    if name != None:
        return name

    for coding in code.get('coding', []):
        name = coding.get('display')
        if name != None:
            return name

    return 'Not implemented'


# Given one Observation resource or one item in the "component" field
# of some Observation resource, retrieve the value of the observed
# parameter. Only the most common data types in FHIR Observations are
# implemented.
def get_observed_parameter_value(resource):
    d = resource.get('valueInteger')
    if d != None:
        return str(d)

    d = resource.get('valueCodeableConcept', {}).get('coding', [])
    if len(d) > 0:
        s = d[0].get('code')
        if s != None:
            return s

    d = resource.get('valueQuantity')
    if d != None:
        value = str(d.get('value', '?'))
        unit = d.get('unit', d.get('code'))
        if unit != None:
            return '%s [%s]' % (value, unit)
        else:
            return value

    d = resource.get('valueDateTime')
    if d != None:
        return str(d)

    d = resource.get('valueSampledData', {}).get('data')
    if d != None:
        crop = 64
        if len(d) > crop:
            return d[:crop] + '...'
        else:
            return d

    # TODO - Feel free to add support for more data types!
    dataType = list(filter(lambda x: x.startswith('value'), resource.keys()))

    if len(dataType) > 0:
        return 'Not implemented (%s)' % dataType[0]
    else:
        return ''


# Given one Observation resource, retrieve the recording time of this
# observation.
def get_time(resource):
    s = resource.get('issued')
    if s != None:
        return s
    else:
        # Fallback
        return resource['meta']['lastUpdated']

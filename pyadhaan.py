"""PyAdhaan is Python module for Al-Adhaan which is online adhaan web-application, link - "https://aladhan.com/"
specifically designed for Adhaan times only and library provides adhaan times from city and address
and can generate calendar data from city and address aswell in both Gregorian and Hijri format.
Its a small library with no overhead and easy to use.

Features.
1.Shows adhaan timing from different countries and city.
2.Generate calendar for adhaan times.
3.Support for both gregorian to hijri calendar.
4.Error and exceptions management.
5.Easy to use and understand.
6.Support for Python 3.0 and lower versions.

@Note : All the module funtions with _underscore are private and rest are public.
PyAdhaan : V 1.0
written by Haseeb mir (haseebmir.hm@gmail.com)  
"""

#Import url and json modules.
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # For Python 2.0 and lowe
    from urllib2 import urlopen
import json

"""Private Methods for parsing json data from URL."""
TIMINGS_CITY_URL = "http://api.aladhan.com/v1/timingsByCity"
TIMINGS_ADDRESS_URL = "http://api.aladhan.com/v1/timingsByAddress"
CALENDAR_CITY_URL = "http://api.aladhan.com/v1/calendarByCity"
CALENDAR_CITY_HIJRI_URL = "http://api.aladhan.com/v1/hijriCalendarByCity"
CALENDAR_ADDRESS_URL = "http://api.aladhan.com/v1/calendarByAddress"
CALENDAR_ADDRESS_HIJRI_URL = "http://api.aladhan.com/v1/hijriCalendarByAddress"

#@Private Method to parse json data.
def _parse_json(url):
    json_obj = {}
    try:
        response = urlopen(url)
        data = response.read().decode("utf-8")
        json_obj = json.loads(data)
    except Exception as ex:
        print("Exception occured while parsing JSON : ",ex)
    return json_obj    

#@Private Method to get ahdaan data for single day.
def  _get_day_data(url,data_key):
    json_data = {}
    json_obj = _parse_json(url)
    if json_obj:
        json_obj = json_obj['data']
        json_data = dict(json_obj)[data_key]
    return json_data

#@Private Method to get ahdaan data for whole month.
def _get_calendar_data(url,data_key,key_val):
    data_list = []
    hijri_data,hijri_date = "",""
    json_obj = _parse_json(url)

    if json_obj:
        for data in json_obj['data']:
            json_data = dict(data)[data_key]
            if key_val == "hijri":
                hijri_data = json_data["hijri"]
                if hijri_data:
                    hijri_date = hijri_data["date"]
                    data_list.append(hijri_date)
            else:
                json_data = dict(data)[data_key]
                data_list.append(json_data[key_val])    
    return data_list

"""INFO : Method to get ahdaan data day data from city.
ARGS : city - Provide desired city. 
country - Provide desired country.
method - Adhaan type calcutation see methods list here "https://aladhan.com/calculation-methods"
data_key - Get data for selected data_key, ex : data_key = "timings","date" etc
RETURN : Adhaan data in dictionary format.
"""
def prayer_day_city(city,country,method,data_key):
    url = TIMINGS_CITY_URL + "?city=" + city + "&country=" + country + "&method=" + method
    return _get_day_data(url,data_key)

"""INFO : Method to get ahdaan data day data from address.
ARGS : address - Provide desired address of Mosque with country. 
method - Adhaan type calcutation see methods list here "https://aladhan.com/calculation-methods"
data_key - Get data for selected data_key, ex : data_key = "timings","date" etc
RETURN : Adhaan data in dictionary format.
"""
def prayer_day_address(address,method,data_key):
    address = address.replace(" ","%20")
    url = TIMINGS_ADDRESS_URL + "?address=" + address
    return _get_day_data(url,data_key)

"""INFO : Method to get ahdaan data for whole month by city.
ARGS : city - Provide desired city. 
country - Provide desired country.
method - Adhaan type calcutation see methods list here "https://aladhan.com/calculation-methods"
month - Provide desired month.
year - Provide desired year.
data_key - Get data for selected data_key, ex : data_key = "timings","date" etc
key_val - Same as data_key but its inner data_key for nested data. ex : key_val = "hijri date"
is_hijri - Is the date in hijri format, Provide True or False.
RETURN : Adhaan data in list format.
"""
def prayer_calendar_city(city,country,method,month,year,data_key,key_val,is_hijri):
    if is_hijri:
        url = CALENDAR_CITY_HIJRI_URL
    else:
        url = CALENDAR_CITY_URL
    url = url + "?city=" + city + "&country=" + country + "&method=" + method + "&month=" + month + "&year=" + year
    return _get_calendar_data(url,data_key,key_val)

"""INFO : Method to get ahdaan data for whole month by address.
ARGS :
address - Provide desired address of Mosque with country. 
method - Adhaan type calcutation see methods list here "https://aladhan.com/calculation-methods"
month - Provide desired month.
year - Provide desired year.
data_key - Get data for selected data_key, ex : data_key = "timings","date" etc
key_val - Same as data_key but its inner data_key for nested data. ex : key_val = "hijri date"
is_hijri - Is the date in hijri format, Provide True or False.
RETURN : Adhaan data in list format.
"""
def prayer_calendar_address(address,method,month,year,data_key,key_val,is_hijri):
    address = address.replace(" ","%20")
    if is_hijri:
        url = CALENDAR_ADDRESS_HIJRI_URL
    else:
        url = CALENDAR_ADDRESS_URL    
    url = url + "?address=" + address + "&method=" + method + "&month=" + month + "&year=" + year
    return _get_calendar_data(url,data_key,key_val)  

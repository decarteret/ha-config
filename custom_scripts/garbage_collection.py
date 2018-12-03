import sys
import requests
import datetime
import json
import urllib
import pytz

Address = str( sys.argv[1] )
Encoded = urllib.parse.urlencode( { "pAddress": Address, "start": 0 } )
Url = "https://www.seattle.gov/UTIL/WARP/CollectionCalendar/GetCollectionDays?&" + Encoded

Response = requests.get( Url )

Json = {}

if Response.ok:
        Results = Response.json()

        if Results[0]["start"] is not None:
                TimeZone = pytz.timezone( "America/Los_Angeles" )
                CurrentDate = datetime.datetime.now( TimeZone ).date()

                for Result in Results:
                        WeekDate = datetime.datetime.strptime( Result["start"], "%a, %d %b %Y" ).date()
                        print( str( WeekDate ) + " - " + str( CurrentDate ) )

                        if ( WeekDate >= CurrentDate ):
                                RemainingDays = ( WeekDate - CurrentDate ).days

                                Json = { 
                                        "recycling": Result["Recycling"],
                                        "yard_waste": Result["FoodAndYardWaste"],
                                        "garbage": Result["Garbage"],
                                        "remaining_days": RemainingDays,
                                        "next_collection_day": WeekDate.strftime( "%A" ),
                                        "next_collection_date": WeekDate.strftime( "%D" ),
                                        "address": Address
                                }

                                break

print( json.dumps( Json ) )
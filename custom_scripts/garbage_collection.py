import sys
import requests
import datetime
import json
import urllib

Address = str( sys.argv[1] )
Encoded = urllib.parse.urlencode( { "pAddress": Address, "start": 0 } )
Url = "https://www.seattle.gov/UTIL/WARP/CollectionCalendar/GetCollectionDays?&" + Encoded

Response = requests.get( Url )

if Response.ok:
        Results = Response.json()

        if Results[0]["start"] is None:
                print( { } )

        else:

                CurrentDate = datetime.datetime.now()

                for Result in Results:
                        WeekDate = datetime.datetime.strptime( Result["start"], "%a, %d %b %Y" )
                        if ( WeekDate > CurrentDate ):
                                RemainingDays = ( WeekDate - CurrentDate ).days + 1

                                Json = { 
                                        "recycling": Result["Recycling"],
                                        "yard_waste": Result["FoodAndYardWaste"],
                                        "garbage": Result["Garbage"],
                                        "remaining_days": RemainingDays,
                                        "next_collection_day": WeekDate.strftime( "%A" ),
                                        "next_collection_date": WeekDate.strftime( "%D" ),
                                        "address": Address
                                }

                                print( json.dumps( Json ) )

                                break

else:
        print( {} )
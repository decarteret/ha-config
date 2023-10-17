import sys
import requests
import datetime
import json
import urllib
import pytz

def GetCollectionDays( currentDate, startDate ):

    Address = str( sys.argv[1] )
    Encoded = urllib.parse.urlencode( { "pAddress": Address, "start": startDate.strftime( "%s" ) } )
    Url = "https://www.seattle.gov/UTIL/WARP/CollectionCalendar/GetCollectionDays?&" + Encoded

    Response = requests.get( Url )

    Json = {}

    if Response.ok:
        Results = Response.json()

        if Results[0]["start"] is not None:
            for Result in Results:
                WeekDate = datetime.datetime.strptime( Result["start"], "%a, %d %b %Y" ).date()

                if ( WeekDate >= currentDate ):
                    RemainingDays = ( WeekDate - currentDate ).days
                    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
                    friendlyDay = ordinal( int( WeekDate.strftime( "%d" ) ) )

                    Json = { 
                        "query_date": datetime.datetime.now().strftime( "%c" ),
                        "recycling": Result["Recycling"],
                        "yard_waste": Result["FoodAndYardWaste"],
                        "garbage": Result["Garbage"],
                        "remaining_days": RemainingDays,
                        "next_collection_day": WeekDate.strftime( "%A the " ) + friendlyDay,
                        "next_collection_date": WeekDate.strftime( "%D" ),
                        "address": Address
                    }

                    break

    return Json


TimeZone = pytz.timezone( "America/Los_Angeles" )
CurrentDate = datetime.datetime.now( TimeZone ).date()
StartDate = CurrentDate

Json = GetCollectionDays( CurrentDate, StartDate )

if( Json == {} ):
    StartDate = CurrentDate + datetime.timedelta( days=7 )
    Json = GetCollectionDays( CurrentDate, StartDate )

print( json.dumps( Json ) )

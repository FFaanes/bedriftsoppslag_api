import urllib3
import pickle
import os
import datetime

from flask import Flask, request
from flask_restful import Api, Resource

from OrgOppslag.Search import search_company
from OrgOppslag.UpdateData import update_brreg_files
from managers import Manager


app = Flask(__name__)
api = Api(app)
api_keys = ["test_api_key"]

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# -------------------------------- Get company info  ------------------------------------------------------#
class Bedrift(Resource):
   def get(self, nr_or_name):
        if "api-key" in request.headers and request.headers["api-key"] in api_keys:

            # Save History for statistics on admin page
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            search_history_manager.manage[1][str(current_time)] = {"user": request.headers["current-user"], "search" : nr_or_name}
            search_history_manager.save()

            # Use search count manager to increment searches made by user
            search_count_manager.manage[1].setdefault(request.headers["current-user"], 0)
            search_count_manager.manage[1][request.headers["current-user"]] += 1
            search_count_manager.save()

            # Return cached data if it exists.
            if nr_or_name in cache_manager.manage[1]:
                return cache_manager.manage[1][nr_or_name]

            # Search the company
            company_info = search_company(nr_or_name, validate_emails=request.headers["validate-emails"], similar_results=5, google_search_count=int(request.headers["google-search-count"]))
            
            # Add company to cache
            if type(company_info) == dict:
                cache_manager.manage[1][nr_or_name.lower()] = company_info
                cache_manager.save()

            return company_info
        else:
            return {"error":"access restricted"}


# -------------------------------- Update BRREG files  ------------------------------------------------------#
class OppdaterData(Resource):
    def get(self):
        if "api-key" in request.headers and request.headers["api-key"] in api_keys:
            update_brreg_files()
        else:
            return {"error":"access restricted"}
        


# -------------------------------- Clear JSON cache  ------------------------------------------------------#
class ClearCache(Resource):
    def get(self):
        if "api-key" in request.headers and request.headers["api-key"] in api_keys:
            cache_manager.clear()
        else:
            return {"error":"access restricted"}


# -------------------------------- Retrieve Search History  ------------------------------------------------------#
class SearchHistory(Resource):
    def get(self):
        if "api-key" in request.headers and request.headers["api-key"] in api_keys:
            
            if "mode" in request.headers and request.headers["mode"] == "load":
                return search_history_manager.manage
            else:
                search_history_manager.clear()
                return "history deleted!"

        else:
            return {"error":"access restricted"}


class SearchCounts(Resource):
    def get(self):
        if "api-key" in request.headers and request.headers["api-key"] in api_keys:
            return search_count_manager.manage
        else:
            return {"error":"access restricted"}


# -------------------------------- Prepare and run app  ------------------------------------------------------#

api.add_resource(Bedrift, "/bedrift/<nr_or_name>")
api.add_resource(OppdaterData, "/api/oppdaterdata")
api.add_resource(ClearCache,"/api/clearcache")
api.add_resource(SearchHistory,"/api/searchhistory")
api.add_resource(SearchCounts, "/api/searchcounts")

search_history_manager = Manager("cache")
cache_manager = Manager("history")
search_count_manager = Manager("count")


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)
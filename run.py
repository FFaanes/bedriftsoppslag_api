import urllib3
import pickle
import os

from flask import Flask, request
from flask_restful import Api, Resource

from OrgOppslag.Search import search_company
from OrgOppslag.UpdateData import update_brreg_files


app = Flask(__name__)
api = Api(app)
base_path = os.path.realpath(os.path.dirname(__file__))
api_keys = ["test_api_key"]

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# -------------------------------- Cache management  ------------------------------------------------------#
class CacheManager:
    def __init__(self):
        try:
            self.cache = self.load_cache_pickle()
        except FileNotFoundError:
            with open(f"{base_path}/cache.dat", "wb") as cachefile:
                self.cache = ["cache", {}]
                pickle.dump(self.cache, cachefile)
    
    def clear_cache(self):
        with open(f"{base_path}/cache.dat", "wb") as cachefile:
            self.cache = ["cache", {}]
            pickle.dump(self.cache, cachefile)


    def save_cache(self):
        with open(f"{base_path}/cache.dat", "wb") as cachefile:
            pickle.dump(self.cache, cachefile)

    
    def load_cache_pickle(self):
        with open(f"{base_path}/cache.dat", "rb") as cachefile:
            return pickle.load(cachefile)

  



# -------------------------------- Get company info  ------------------------------------------------------#
class Bedrift(Resource):
   def get(self, nr_or_name):
        if "api-key" in request.headers and request.headers["api-key"] in api_keys:
            # Return cached data if it exists.
            if nr_or_name in cachemanager.cache[1]:
                return cachemanager.cache[1][nr_or_name]

            # Search the company
            company_info = search_company(nr_or_name, validate_emails=request.headers["validate-emails"], similar_results=5, google_search_count=int(request.headers["google-search-count"]))
            
            # Add company to cache
            if type(company_info) == dict:
                cachemanager.cache[1][nr_or_name.lower()] = company_info
                cachemanager.save_cache()

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
            cachemanager.clear_cache()
        else:
            return {"error":"access restricted"}



# -------------------------------- Prepare and run app  ------------------------------------------------------#

api.add_resource(Bedrift, "/bedrift/<nr_or_name>")
api.add_resource(OppdaterData, "/api/oppdaterdata")
api.add_resource(ClearCache,"/api/clearcache")

if __name__ == "__main__":
    # Create Cache Manager object
    cachemanager = CacheManager()

    app.run(debug=True, host="127.0.0.1", port=5001)
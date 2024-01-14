import urllib3

from flask import Flask, request
from flask_restful import Api, Resource

from OrgOppslag.Search import search_company

api_keys = ["test_api_key"]

app = Flask(__name__)
api = Api(app)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Bedrift(Resource):
   def get(self, nr_or_name):
        if "api-key" in request.headers and request.headers["api-key"] in api_keys:
            return search_company(nr_or_name, validate_emails=request.headers["validate-emails"], similar_results=5, google_search_count=int(request.headers["google-search-count"]))
        else:
            return {"error":"access restricted"}


api.add_resource(Bedrift, "/bedrift/<nr_or_name>")

if __name__ == "__main__":
    app.run(debug=True)
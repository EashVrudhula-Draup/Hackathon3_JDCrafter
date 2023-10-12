import json

import requests
jd = "data engineer in bangalore with 5+ years of experience in python and spark"
input_payload = {
    'input_description': jd,
    'return_unsynonimised_entities':True, # To get unsynonimised result this flag should be true.
    'return_all_entities': True, ## To get all the Unsynonimised Entities predicted by Model
#     'entities_requested': ["JOB COMMITMENT TYPE", "WORK LOCATION MODE", "WORK TIMING STRUCTURE", "DEGREE", "FIELD OF STUDY", "YEARS OF EXPERIENCE"]
}

## Complete Entity List:`
# ["JOB TITLE", "CERTIFICATIONS", "SOFT SKILL", "TOOLS", "SKILL", "COMPETENCIES",
# "LOCATION", "JOB COMMITMENT TYPE", "WORK LOCATION MODE", "WORK TIMING STRUCTURE",
# "DEGREE", "FIELD OF STUDY", "YEARS OF EXPERIENCE", "SENIORITY LEVEL", "COMPANY", "TEAM NAME",
# "COMPANY CULTURE/VALUES", "MISSION STATEMENT", "INDUSTRY", "BENEFITS", "SALARY",
# "VISA", "NOC/CLEARANCE"]

headers = {
  'Content-Type': 'application/json'
}

env = "qa"

# url = f"http://universal-jd-entity-extractor.draup-{env}-microservices.com:8080/entity_extraction/"
url = "http://localhost:8080/entity_extraction/"
# url = "http://127.0.0.1:5000/entity_extraction/"
print("sending request to url: ", url)
response = requests.request("POST", url, headers=headers, data=json.dumps(input_payload))
print(response.json())
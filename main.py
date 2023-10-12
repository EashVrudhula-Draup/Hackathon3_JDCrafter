from flask import Flask
from flask import request, jsonify
import json
import requests
from api_functions.query_data import execute_query
from api_functions.hit_chatGPT import hit_chatGPT
app = Flask(__name__)

def calculate_all_data(response_dict):
    responsibilites_and_skills = response_dict.get('responsibilites_and_skills', None)
    about_company = response_dict.get('about_company', None)
    if responsibilites_and_skills:
        job_title = responsibilites_and_skills[0][0]
        job_role_description = responsibilites_and_skills[0][1]
        responsibility = responsibilites_and_skills[0][2]
        skillset = responsibilites_and_skills[0][3]
        core_skills = json.loads(skillset)["skills"]
        soft_skills = json.loads(skillset)["soft_skills"]

    if about_company:
        company_description = about_company[0][2]


    # write job_role_description to job_role_description.txt
    with open('job_role_description.txt', 'w') as f:
        f.write(job_role_description)
    with open('responsibilities.txt', 'w') as f:
        f.write(responsibility)
    with open('about_company.txt', 'w') as f:
        f.write(company_description)
    final_response = {}
    final_response["job_role_description"] = hit_chatGPT("clean and explain the job role - {}".format(job_title), "job_role_description.txt")
    final_response["responsibilities"] = hit_chatGPT("clean and explain the responsibilities - {}".format(responsibility), "responsibilities.txt")
    final_response["about_company"] = hit_chatGPT("clean and explain the company - {}".format(company_description), "about_company.txt")
    final_response["core_skills"] = core_skills
    final_response["soft_skills"] = soft_skills
    return final_response
def get_all_data(response_json):
    company = response_json.get('unsynonimised_results').get('COMPANY', [None])[0]
    job_title = response_json.get('unsynonimised_results').get('JOB TITLE', [None])[0]
    locations = response_json.get('results').get('location', None)
    if locations:
        out_list = lambda x: [i.get('synonimised_location', None) for i in x]
        location = out_list(locations)
    else:
        location = response_json.get('unsynonimised_results').get('LOCATION', [None])
    years_of_experience = response_json.get('unsynonimised_results').get('YEARS OF EXPERIENCE', [None])[0]

    skills = response_json.get('results').get('skill', None)
    if skills:
        out_list = lambda x: [i.get('synon_skill', None) for i in x]
        skill = out_list(skills)
    else:
        skill = response_json.get('unsynonimised_results').get('TOOLS', [None])

    print(job_title)
    company_first = company.split(" ")[0]
    print(company_first)
    query_skills = "SELECT DISTINCT job_role, job_description, responsibility, skillset from job_data WHERE lower(job_role) = '{}'".format(
        job_title.lower())
    query_about_company = "SELECT * from company_description_table WHERE LOWER(SPLIT_PART(company_name, ' ', 1)) = '{}'".format(
        company_first.lower())
    # if not years_of_experience:
    #     query_salary = "SELECT talent_cost FROM job_data WHERE job_role = '{}' and location_name= '{}'".format(job_title, location)
    # else:
    #     # query_salary = "SELECT talent_cost FROM job_data WHERE job_role = '{}' and location_name= '{}'".format(
    #         job_title, location)
    query_dict = {
        "responsibilites_and_skills": query_skills,
        "about_company": query_about_company
    }
    return calculate_all_data(execute_query(query_dict))
    # return execute_query(query_dict)
    # results = execute_query(query_dict)
    # responsibilites_and_skills = results.get('responsibilites_and_skills', None)
    # about_company = results.get('about_company', None)
    #
def get_entities(jd):
    input_payload = {
        'input_description': jd.title(),
        'return_unsynonimised_entities':True,
        'return_all_entities': True
    }
    headers = {
      'Content-Type': 'application/json'
    }
    url = "http://localhost:8080/entity_extraction/"
    print("sending request to url: ", url)
    response = requests.request("POST", url, headers=headers, data=json.dumps(input_payload))
    return get_all_data(response.json())
    # return response.json()

@app.route('/',methods=['POST'])
def hello_post():
    json_req = request.get_json()
    json_req_name = json_req["jd"]
    entities_response = get_entities(json_req_name)
    return entities_response

app.run()

if __name__ == "__main__":
    app.run(debug=True)

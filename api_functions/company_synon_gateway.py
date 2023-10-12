import requests
import json
def get_company_synon(company):
    # company = "apple"
    url = f"https://prod-draup-services.draup.technology/api/company-search/search/by-rank?query={company}&filter_keys=ALL&similarity_threshold=0.75"
    payload = {}
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjb21wYW55X3NlYXJjaF9pbnRlcm5hbEBkcmF1cC5jb20iLCJleHAiOjE2OTc3NDcwMTB9.k2rQrqfvxicY5-3DfiwOAnH4k66QOp-5svuchqPdIw8'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res = response.json()
    most_probable_company = res.get('most_probable_company', None)
    return most_probable_company

def job_role_synon(input_title):
    url = "http://localhost:8081/title-to-role"

    payload = json.dumps({
        "input_titles": input_title,
        "top_k": 1,
        "return_score": True,
        "base_threshold": False
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    res = response.json()
    # final_role = res["results"][0]["predicted_roles"][0]["job_role"])
    results = res.get("results", None)
    if results:
        predicted_roles = results[0].get("predicted_roles", None)
        if predicted_roles:
            job_role = predicted_roles[0].get("job_role", None)
            return job_role
if __name__ == "__main__":
    print(job_role_synon("software engineer"))
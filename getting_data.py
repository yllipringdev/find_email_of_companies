import csv
from googlesearch import search
import time
from urllib.parse import urlparse
import requests


HUNTER_API_KEY = "INSERT YOUR HUNTER.IO KEY HERE"

def get_email_from_company(domain):
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&limit=1&api_key={HUNTER_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "data" in data and "emails" in data["data"] and len(data["data"]["emails"]) > 0:
        first_email = data["data"]["emails"][0]["value"]
        print(first_email)
        return first_email
    else:
        print("No emails found.")
        return None

def get_email_from_hunterio(domain, first_name, last_name):
    url = f"https://api.hunter.io/v2/email-finder?domain={domain}&first_name={first_name}&last_name={last_name}&api_key={HUNTER_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "data" in data and "email" in data["data"]:
        return data["data"]["email"]
    return None

def search_company_websites(query, num_results=10):
    results = []
    try:
        search_results = search(query, num_results=num_results)
        
        for i, result in enumerate(search_results):
            results.append(result)
            if i >= num_results:
                break
    except Exception as e:
        print("An error occurred:", str(e))
    return results

def search_company_ceos(query, num_results=10, max_results=10):
    results = []
    try:
        search_results = search(query, num_results=num_results)
        
        for i, result in enumerate(search_results):
            results.append(result)
            if i >= max_results:
                break
    except Exception as e:
        print("An error occurred:", str(e))
    return results

def format_ceo_name(ceo_name):
    formatted_name = "Not Found"
    if ceo_name != "Not Found":
        formatted_name = " ".join([part.capitalize() for part in ceo_name.split("-")])
    return formatted_name

def main():
    input_csv_filename = "company_list.csv"
    output_csv_filename = "combined_results.csv"
    num_results_to_display = 1
    max_ceo_results = 5  # Set the maximum number of CEO results to collect

    try:
        with open(input_csv_filename, 'r') as input_csvfile:
            csvreader = csv.reader(input_csvfile)
            
            results = []
            for row in csvreader:
                if row:
                    company_name = row[0]  # Assuming company names are in the first column
                    
                    # Search for company website
                    website_query = f"{company_name} official website"
                    print(f"Searching for website of {company_name}...")
                    website_results = search_company_websites(website_query, num_results_to_display)

                    company_domain = ""  # Initialize company domain

                    if website_results:
                        parsed_url = urlparse(website_results[0])
                        if parsed_url.netloc:
                            company_domain = parsed_url.netloc
                    
                    # Search for CEO name
                    ceo_query = f"{company_name} CEO"
                    print(f"Searching for CEO of {company_name}...")
                    ceo_results = search_company_ceos(ceo_query, num_results_to_display, max_ceo_results)
                    
                    ceo_name = "Not Found"
                    ceo_email = "Not found"

                    if "linkedin.com" in ceo_results[0]:
                        ceo_name = ceo_results[0].split("/")[-1]
                        ceo_name = ceo_name.rsplit("-", 1)[0]

                    # Call Hunter.io API to find CEO email
                    
                    formatted_ceo_name = format_ceo_name(ceo_name)
                    # print(formatted_ceo_name,formatted_ceo_name)
                    names = formatted_ceo_name.split()

                    first_name = names[0]
                    last_name = names[-1]
                    print(website_results[0])
                    if "Not Found" in formatted_ceo_name:
                        print("Not found")
                    else:
                        ceo_email = get_email_from_hunterio(company_domain, first_name, last_name)
                        # print(ceo_email)
                        if ceo_email is None:
                            company_email = get_email_from_company(company_domain)
                            # print("Ceo is None")
                            # print(company_email)
                            # print("NoneFound")
                            results.append((company_name, formatted_ceo_name, company_email, website_results[0] if website_results else "Not Found", f"\"{','.join(ceo_results)}\""))
                        else:
                            # print("FoundNone")
                            results.append((company_name, formatted_ceo_name, ceo_email, website_results[0] if website_results else "Not Found", f"\"{','.join(ceo_results)}\""))

            # Write results to output CSV
            with open(output_csv_filename, 'w', newline='') as output_csvfile:
                csvwriter = csv.writer(output_csvfile)
                for result in results:
                    csvwriter.writerow(result)
            print(f"Results written to {output_csv_filename}")
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()


The CEO Email Finder project is designed to automate the process of finding email addresses for CEO positions within companies listed in the company_list.csv file. This tool leverages the power of Python to streamline the email discovery process, providing an efficient solution for gathering CEO contact information.

Getting Started
To utilize the CEO Email Finder project, follow these steps:

Installation: Make sure you have Python installed on your system. Additionally, ensure that the Flask and googlesearch Python packages are installed. You can install them using the following commands:

- pip install Flask
- pip install googlesearch-python
API Key Generation: The project utilizes the hunter.io API to retrieve CEO email addresses. To make this project work, you need to generate a new API key from hunter.io. This key will enable the tool to access hunter.io's services. Keep the generated API key secure and follow best practices for API key management.

Running the Project:

Launch the application by running app.py.
The service will start on http://127.0.0.1:5000.
Access this URL using a web browser.
Uploading the Company List:

Once the service is running, you can upload a CSV file named company_list.csv containing a list of company names.
The script will automatically find the CEO of each company by utilizing available online resources.

Email Retrieval and Display:

After identifying the CEOs, the script will further query hunter.io to retrieve the associated email addresses.
The results will be neatly organized and displayed in the index.html file.
Note:
This project demonstrates the capabilities of automating CEO email discovery, streamlining what can otherwise be a time-consuming and manual process. It serves as an example of leveraging Python, Flask, and external APIs to create a valuable tool.

Ensure that you handle generated API keys and sensitive information responsibly, following industry best practices for security and privacy.

Feel free to modify and extend the project according to your needs and requirements.

For more information on how the project works and its internal mechanisms, refer to the source code and comments provided.

Happy email hunting!

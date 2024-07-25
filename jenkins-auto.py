
import jenkins
import requests

# Update the host variable to point to your AWS instance
host = "http://localhost:8080/"
username = "henpe"
api_token = "1184bd898ee74b23cfc6e0fa86e83dafd3"

try:
    # Check if the Jenkins server is reachable
    response = requests.get(f"{host}/login")
    if response.status_code != 200:
        raise Exception(f"Unable to reach Jenkins server: {response.status_code}")

    # Initialize the Jenkins server
    server = jenkins.Jenkins(host, username, api_token)

    # Test the API communication
    user = server.get_whoami()
    version = server.get_version()
    print('Hello %s from Jenkins %s' % (user['fullName'], version))

    # Jobs 
    jobs = server.get_jobs()
    if jobs:
        job_name = jobs[0]['name']
        server.build_job(job_name)
        job_number = server.get_job_info(job_name)['lastCompletedBuild']['number']

        print(f'Job {job_name} has been started!')
        print(server.get_build_console_output(job_name, job_number))
    else:
        print("No jobs found on the Jenkins server.")

except requests.exceptions.RequestException as e:
    print(f"Network error: {e}")
except jenkins.JenkinsException as e:
    print(f"Jenkins connection error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
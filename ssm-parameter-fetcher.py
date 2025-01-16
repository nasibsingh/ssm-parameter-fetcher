import os
import subprocess
import logging
from datetime import datetime
import json

# Function to set up logging
def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
    logging.basicConfig(
        filename=log_file,
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logging.getLogger().addHandler(console_handler)
    print(f"Logs will be stored in {log_file}")

# Function to list sub-folders in a directory
def list_folders(path):
    return [f.name for f in os.scandir(path) if f.is_dir()]

# Function to choose an option from a list
def choose_option(options, prompt):
    print(prompt)
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    while True:
        try:
            choice = int(input("Select an option (by number): "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice. Please choose a valid number.")
        except ValueError:
            print("Please enter a valid number.")

# Function to fetch AWS CLI profiles
def fetch_aws_profiles():
    try:
        result = subprocess.run(["aws", "configure", "list-profiles"], capture_output=True, text=True, check=True)
        profiles = result.stdout.splitlines()
        if not profiles:
            print("No AWS profiles found. Please configure at least one profile.")
            exit(1)
        return profiles
    except subprocess.CalledProcessError as e:
        logging.error(f"Error fetching AWS profiles: {e}")
        print("Error fetching AWS profiles. Ensure AWS CLI is configured.")
        exit(1)

# Function to set the AWS CLI profile
def set_aws_profile(profile):
    os.environ['AWS_PROFILE'] = profile
    print(f"AWS CLI profile set to: {profile}")
    logging.info(f"AWS CLI profile set to: {profile}")

# Function to fetch and save parameter store values
def fetch_parameter_store_values(project_path, environment):
    env_file_path = os.path.join(project_path, environment, ".env")
    output_file_path = os.path.join(project_path, environment, "fetched_parameters.json")
    kv_file_path = os.path.join(project_path, environment, "fetched_parameters.env")

    parameters = {}
    print(f"\nFetching parameters for project: {os.path.basename(project_path)}, environment: {environment}\n")
    try:
        # Fetch parameters from AWS SSM Parameter Store
        prefix = f"/{os.path.basename(project_path)}/{environment}/"
        result = subprocess.run(
            ["aws", "ssm", "get-parameters-by-path", "--path", prefix, "--recursive", "--with-decryption"],
            capture_output=True, text=True, check=True
        )
        response = json.loads(result.stdout)
        with open(kv_file_path, 'w') as kv_file:
            for param in response.get("Parameters", []):
                key = param["Name"].split("/")[-1]
                value = param["Value"]
                parameters[key] = value
                kv_file.write(f"{key}={value}\n")
                print(f"{key}: {value}")

        # Save parameters to JSON file
        with open(output_file_path, 'w') as output_file:
            json.dump(parameters, output_file, indent=4)
        print(f"\nParameters saved to: {output_file_path} and {kv_file_path}")
        logging.info(f"Parameters saved to: {output_file_path} and {kv_file_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error fetching parameters from AWS: {e}")
        print("Error fetching parameters. Ensure AWS CLI is configured correctly and has the necessary permissions.")

# Main execution function
def main():
    setup_logging()

    # Fetch and choose AWS profile
    aws_profiles = fetch_aws_profiles()
    selected_profile = choose_option(aws_profiles, "Available AWS Profiles:")
    set_aws_profile(selected_profile)

    # Choose project
    environments_base_path = "environments"
    available_projects = list_folders(environments_base_path)
    if not available_projects:
        print("No projects found in the environments directory.")
        return

    selected_project = choose_option(available_projects, "Available Projects:")
    project_path = os.path.join(environments_base_path, selected_project)

    # Choose environment
    available_environments = list_folders(project_path)
    if not available_environments:
        print(f"No environments found for project '{selected_project}'.")
        return

    selected_environment = choose_option(available_environments, f"Available Environments for {selected_project}:")

    # Fetch and save parameters
    fetch_parameter_store_values(project_path, selected_environment)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")
    finally:
        logging.info("Script execution finished.")

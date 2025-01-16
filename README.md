# AWS SSM Parameter Fetcher

## Overview

This script is designed to streamline the management of AWS environments and projects. It allows users to:

- Select AWS CLI profiles dynamically.
- Fetch and save AWS SSM Parameter Store parameters into environment files.
- Organize projects and environments in a structured directory format.
- Log all activities for better traceability.

## Prerequisites

### 1. Python

Ensure you have Python 3.6+ installed. This script is tested with Python 3.11.3.

### 2. AWS CLI

Install and configure the AWS CLI. At least one AWS profile should be set up beforehand.

### 3. Required Permissions

Ensure your AWS IAM user or role has the following permissions:

- `ssm:GetParameter`
- `ssm:GetParametersByPath`

### 4. Directory Structure

- Create a base directory named `environments` in the script's location.
- Inside `environments`, store project-specific folders with environment sub-folders (e.g., `dev`, `stg`, `prod`).

### 5. Dependencies

No external Python libraries are required. Ensure Python's standard library is available.

## Features

### 1. **AWS Profile Management**

- Dynamically list and choose AWS CLI profiles during script execution.
- Set the chosen profile for the session.

### 2. **Parameter Store Management**

- Fetch parameters from AWS SSM Parameter Store using the `/project/environment/KEY` naming convention.
- Save parameters into:
  - JSON files for structured data.
  - `.env` files for easy integration with applications.

### 3. **Logging**

- Logs are saved in a `logs/` directory.
- Log filenames include timestamps for better traceability.
- Console logging is enabled for real-time feedback.

## Usage

### Step 1: Run the Script

Execute the script:

```bash
python script_name.py
```

### Step 2: Select AWS Profile

Choose an AWS CLI profile from the dynamically listed options.

### Step 3: Select Project and Environment

Navigate through available projects and environments stored under the `environments/` directory.

### Step 4: Fetch and Save Parameters

The script will:

1. Fetch parameters from AWS SSM Parameter Store based on the project and environment.
2. Save the parameters to both JSON and `.env` files.
3. Display fetched parameters in the console.

### Step 5: Logging

Logs are automatically generated and saved in the `logs/` directory.

## Sample Directory Structure

```
project-folder/
|-- environments/
|   |-- ProjectA/
|   |   |-- dev/
|   |   |   |-- .env
|   |   |   |-- fetched_parameters.json
|   |   |-- stg/
|   |   |-- prod/
|-- logs/
    |-- log_2025-01-16_12-00-00.log
```

## Environment File Format

The `.env` file will contain key-value pairs in the following format:

```
KEY=value
ANOTHER_KEY=another_value
```

## Error Handling

- Logs all errors in the log file.
- Provides user-friendly error messages in the console.

## Future Enhancements

- Add functionality to update parameters interactively.
- Support advanced tagging for parameters.
- Enable fetching parameters across multiple projects in a single execution.

## Troubleshooting

- Ensure the `environments` directory and its structure are correctly set up.
- Verify AWS CLI configuration and permissions.
- Check the logs for detailed error messages.


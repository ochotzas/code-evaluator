# Code Evaluator

A simple web-based Python code evaluator using Flask.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The **Code Evaluator** is a web-based application developed using the Flask framework. Its primary functionality revolves around the evaluation of Python code, facilitating a comparative analysis between the resultant output and the anticipated output. This application has been meticulously crafted to serve as a valuable instrument for the automated testing and validation of Python code fragments. Furthermore, it offers a distinctive feature in the form of a visual differentiation tool that enables users to discern disparities between the actual and expected output. Additionally, users can also employ file upload capabilities to specify the anticipated output.

## Features

- Evaluate Python code snippets.
- Compare the actual output with the expected output.
- Visual diff between actual and expected output.
- Option to upload an expected output file.
- Option to manually enter the expected output.
- Create an assignment with a description and the expected output ([see below](#createpost-an-assignment-using-the-api)).

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed.
- A virtual environment for managing project dependencies (optional but recommended).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ochotzas/code-evaluator.git
    ```
2. Navigate to the project directory:

   ```bash
   cd code-evaluator
   ```
3. Create a virtual environment:

   ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:

   ```bash
    source venv/bin/activate
    ```
5. Install the project dependencies:

   ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the Flask application:

   ```bash
    python app.py
    ```

2. Open a web browser and go to http://localhost:8080 to access the Code Evaluator.
3. Enter your Python code in the "Enter Python Code" textarea.
4. Optionally, upload an expected output file or manually enter the expected output in the "Expected Output" textarea.
5. Click the "Evaluate Code" button to run the code and see the evaluation results.

_or (see below [Evaluate Code](#createpost-an-assignment-using-the-api) & [Post/Create Assignment](#createpost-an-assignment-using-the-api))_

### Evaluate code using the API

Use the API by calling the endpoint `/evaluate` with a POST request and passing the Python code and expected output as
form data.

Example:

```bash
curl --location 'http://localhost:8080/evaluate' \
--header 'Content-Type: application/json' \
--data '{
  "code": "print(\"Hello, World!\")",
  "expected_output": "Hello, World!\n"
}'
```

In this case, the response will be a JSON object with the following structure:

```json
{
    "message": "Output matches the expected output.",
    "success": true
}
```

### ![NEW](https://img.shields.io/badge/-New-green) Create/Post an assignment using the API

Use the API by calling the endpoint `/post-assignment` with a POST request
and passing the assignment description and expected output like the following example:

```json
{
  "description": "Write a Python program to print \"Hello, World!\".",
  "expected_output": "Hello, World!\n"
}
```

In this case, the response will be a JSON object with the following structure:

```json
{
    "key": "uid",
    "message": "Assignment created successfully.",
    "success": true
}
```

The `key` is a unique identifier for the assignment.
You can use this key to retrieve the assignment details by calling the http://localhost:8080/?assigment=uid for example.


## Screenshots

1. Home page.

   ![Code Evaluator home page](https://gcdnb.pbrd.co/images/Rv6bUmhMDg22.png)

2. Assignment page with the description and expected output.

   ![Code Evaluator assignment page](https://gcdnb.pbrd.co/images/YDQLDrr2MHBI.png)

3. Assignment page with user's wrong output.

   ![Code Evaluator with wrong output](https://gcdnb.pbrd.co/images/Zghnrm87RAlE.png?o=1)

4. Assignment page with user's correct output.

    ![Code Evaluator with correct output](https://gcdnb.pbrd.co/images/0Wf1GwP96u10.png)

5. Assignment page with user's syntax error.

    ![Code Evaluator with syntax error](https://gcdnb.pbrd.co/images/rf72OqDZ8hKK.png)

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Create a pull request describing your changes.

## License

This project is licensed under the MIT License.
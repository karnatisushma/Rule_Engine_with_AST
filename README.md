# Rule Engine API

This project is a RESTful API for creating, combining, and evaluating rules based on Abstract Syntax Trees (ASTs). It is designed to provide an efficient way to define and manage conditional rules programmatically, suitable for applications such as data validation, filtering, and business logic automation.

## Table of Contents

- [Overview](#overview)
- [Design Choices](#design-choices)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Examples](#examples)

## Overview

This rule engine API provides three primary functionalities:
- **Create Rules**: Define logical rules with Python syntax, which get converted to AST representations.
- **Combine Rules**: Merge multiple rules to form complex conditions.
- **Evaluate Rules**: Check the validity of data against defined rules, returning a boolean result.

## Design Choices

### Framework

- **Flask**: A lightweight, flexible web framework for building RESTful APIs. Flask was chosen for its simplicity, ease of use, and strong community support.

### Rule Representation

- **Abstract Syntax Trees (AST)**: The rules are parsed into ASTs to allow safe evaluation and easy manipulation of logical expressions. ASTs allow for secure handling of rule logic without executing arbitrary code directly, which enhances safety and reusability.

### Data Exchange

- **JSON**: JSON is used for input and output as it is easy to work with in REST APIs, well-supported across various languages, and allows complex data structures to be serialized and deserialized easily.

## Dependencies

The core dependencies for the project include:
- **Python 3.x**: Main programming language
- **Flask**: Web framework
- **astor**: For AST handling and transformations
- **SQLAlchemy**: If a database connection is required, SQLAlchemy can be added as an ORM.


## Installation

### Step 1: Clone the Repository


```bash
git clone https://github.com/yourusername/rule-engine-api.git
cd rule-engine-api 
```

### Step 2: Install Required Python Packages

```bash
pip install -r requirements.txt
```
### Step 3: Verify Installation

```bash
python app.py
```

#### The API should be available at http://127.0.0.1:5000.

## API Endpoints

### 1. Create Rule
- **POST** `/create_rule`: Creates a rule and returns its AST representation.
- **Request Payload**:
  ```json
  {
      "rule": "x > 10 and y < 20"
  }

  Response:
      json
    {
        "ast": "<AST_representation>"
    }

### 2. Combine Rules
- **POST** `/combine_rules`: Combines multiple rules into a single AST.
- **Request Payload**:
  ```json
  {
      "rules": ["x > 10", "y < 20"]
  }

  Response:
      json
    {
        "combined_ast": "<Combined_AST_representation>"
    }

### 3. Evaluate Rules
- **POST** `/evaluate_rule`: Evaluates an AST against provided data.
- **Request Payload**:
  ```json
  {
      "ast": "<AST_representation>",
      "data": { "x": 15, "y": 5 }
  }

  Response:
      json
    {
        "result": true
    }


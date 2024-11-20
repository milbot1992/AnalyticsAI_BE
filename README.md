# Local Authority Statistical Analysis API

Overview
--------

This project provides an API that delivers statistical analysis and insights for different Local Authorities, focusing on specific indicators. The API integrates with OpenAI's GPT model to generate commentary and insights based on statistical data.

Features
--------

-   Fetch specific statistical data and commentary for a given Local Authority and Indicator.
-   Analyse mortality rates, confidence intervals, z-scores, and other statistical metrics for insights.
-   Generate GPT-powered commentary with succinct and research-style bullet points on the selected data.

Requirements
------------

-   Python 3.8+
-   FastAPI for building the API
-   [Uvicorn](https://www.uvicorn.org/) as the ASGI server for running the API
-   Pandas for data processing
-   [OpenAI API](https://platform.openai.com/) for GPT-based commentary

Setup Instructions
------------------

1.  **Clone the Repository**:

    `git clone [<repository-url>](https://github.com/milbot1992/AnalyticsAI_BE)
    cd <repository-directory>`

2.  **Install Dependencies**: Make sure you have Python 3.8 or later. Install the required packages using pip:


    `pip install -r requirements.txt`

3.  **Environment Variables**:

    -   Create a `.env` file in the project root directory.
    -   Add your OpenAI API key to the `.env` file:

        `GPT_API_KEY=your_openai_api_key`

    -   Ensure that `.env` is added to `.gitignore` to keep your API key secure.

Testing
----------------------
The tests are saved in:
be_ruby_health/
└── tests/
    ├── __init__.py 
    └── test_api.py

To run the tests run the following command:

    `pytest tests`

Running the API Server
----------------------

To start the server locally, use the following command:

`uvicorn app:app --reload`

-   The `--reload` option enables automatic reload on code changes, ideal for development.

The server will run locally at `http://127.0.0.1:8000`.

Endpoints
---------

### 1\. Get Data for Local Authority and Indicator

-   **Endpoint**: `/local_authority/{la_name}`
-   **Method**: GET
-   **Description**: Fetches the statistical data and GPT commentary for the specified Local Authority and Indicator.
-   **Parameters**:
    -   `la_name` (Path Parameter): The name of the Local Authority (e.g., "York").
    -   `indicator_name` (Query Parameter): The name of the Indicator (e.g., "Under 75 mortality rate from cancer").

**Example Request**:

`GET /local_authority/York?indicator_name=Under 75 mortality rate from cancer`

**Example Response**:

`{
    "Area Name": "York",
    "Indicator Name": "Under 75 mortality rate from cancer",
    "GPT Commentary": "- The Under 75 mortality rate from cancer in Local Authority York is 131.0, with a z-score of 0.72...",
    "Data Points": {
        "Value": 130.99759,
        "Lower CI 95.0 limit": 121.33137,
        "Upper CI 95.0 limit": 141.22793,
        "Compared to England value or percentiles": "Similar"
    }
}`

Additional Information
----------------------

### Data Security

-   The `.env` file contains sensitive information and should be kept secure and out of version control. Ensure that `.env` is listed in `.gitignore`.

### Notes

-   Ensure your `GPT_API_KEY` has sufficient API usage limits to handle requests for generating commentary.
-   All data is from PHE Fingertips API
-   Customise the project by choosing the Indicators that you are interested in analysing from PHE Fingertips (https://fingertips.phe.org.uk/profile/health-profiles/data#page/1)

# Problem Link 
[website](https://goatlys.notion.site/BE-engineer-testing-assigment-f1890cf18af343f7b737ee95575f98dd)

## FastAPI Scraper

Here, we have created a web scraping using FASTAPI framework as per the given requirements.  


## Usage

1. Git Clone the Repository

2. Create a virtual environment and activate it

    ````
    python -m venv ~/.scraper
    source ~/.scrasper/bin/activate  

3. Install the dependencies:

    ````
    pip install -r requirements.txt

    ````

4. if you want ot use postgres, update the settings.py file with the database URL. Currently we are using sqlite db.

    ```
    from pydantic_settings import BaseSettings

    class Settings(BaseSettings):
        database_url: str = "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
        static_auth_token: str = "MY_AUTH_TOKEN"
    ```

5. Run the application:

    ```
    uvicorn app.main:app --reload
    ```


## Testing


1. Use an API client like Postman to test the endpoint http://127.0.0.1:8000/scrape/?pages=2&proxy=http://your-proxy.com.

2. Add the Authorization header with the value Token "MY_AUTH_TOKEN".

3. Example request in Postman:

    ```
    Method: GET
    URL: http://127.0.0.1:8000/scrape/?pages=2&proxy=http://your-proxy.com
    Headers:
    Authorization: Token MY_AUTH_TOKEN
    ```
    
    Result should be like
    ```
    {
    "status": "success",
    "updated_count": 3,
    "total_count": 48
    }
    ```
# Ingesting the Canadian Common CV
The Canadian Common CV (CCV) is a tool that allows Canadian researchers to input their resume in a standardized format. It is used by multiple organizations such as granting agencies, federal, provincial and academic instituions. The tool enable users to output results in an XML document, that can be used in external applications. 


This repository contains the **Selection Tests** for the Ingesting the Canadian Common CV project.

## **Technologies Used**

### **Server-side**
* [Python 3.5+](http://www.python.org): The language of choice.
* [Flask](https://flask.palletsprojects.com/en/1.1.x/): Framework used in this project.

### **Database**
* [Sqlite3](https://www.sqlite.org/index.html): Database of choice.


## Installation 
* Create a virtual environment
```
virtualenv venv -p python3
```
* Activate the virtual enviornment
```
. ./venv/bin/activate
```
* Install the python packages required for this project 
```python3 
pip3 install -r requirements.txt
``` 
* [**Optional**]: If you want to use your own sqlite database, then create a new sqlite3 database and update the path in the *config.cfg* file in the root directory. After this, run the following commad to migrate the existing schema in the database.
```
python3 manage.py db upgrade

```

## Running server
After following all installation steps, Run the flask server
```
python3 manage.py runserver
```


## Endpoints & their usage with examples

All the endpoints have pagination enabled to reduce the load on the database. By default *10* posts will be available in the response. If you want to query more than the default value use *per_page* as a query parameter in the endpoint. For example:
```
http://127.0.0.1:5000/api/get-posts?per_page=30
```

1. Endpoint to return the posts by ordering. By default, it's in chronological order. You can also order by View Count or Score.

    To order using the above params, use *order* as a query params in the endpoint and values as <i>**view_count**</i> or <i>**score**</i>. For example

    ```
    http://127.0.0.1:5000/api/get-posts
    http://127.0.0.1:5000/api/get-posts?order=view_count
    http://127.0.0.1:5000/api/get-posts?order=score
    http://127.0.0.1:5000/api/get-posts?order=score&per_page=20
    ```

2. Endpoint to search the posts by a keyword. Use *query* as a query parameter in the endpoint and value as the keyword which you want to search. For example
    ```
    http://127.0.0.1:5000/api/search-post?query=management
    http://127.0.0.1:5000/api/search-post?query=some%20of%20the%20
    ```

3. Endpoint to ingest the XML file into the Database. This ingests the data into the sqlite database.
    ```
    http://127.0.0.1:5000/api/ingest-data
    ```
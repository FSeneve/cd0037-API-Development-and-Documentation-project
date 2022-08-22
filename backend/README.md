Trivia APP Backend
Trivia App is a website built by a restful API, which permits you to create questions, see different categories and questions, and play a quiz to test your knowledge.
Game mechanism: Currently, when a user plays the game they play up to five questions of the chosen category. If there are fewer than five questions in a category, the game will end when there are no more questions in that category.
This app project demonstrates my skills in building REST APIs with Flask.

Table of Contents
Trivia APP Backend
Table of Contents
1. Getting Started
1.1. Backend Structure : Main Files
1.2. Installing Dependencies
1.2.1. Python 3.8
1.2.2. Virtual Environment
1.2.3. PIP Dependencies
1.2.4. Project Key Dependencies
2. setting up
2.1. setting up the environment variables
2.2. Database Setup
3. Running the server
4. Testing
5. API Reference
5.1. General
5.2. error Handlers
5.3. Endpoints
5.3.1. GET /categories
5.3.2. GET /questions
5.3.3. GET /categories/<int:id>/questions
5.3.4. POST /questions
5.3.5. POST /questions/search
5.3.6. POST /quizzes
5.3.7. DELETE /questions/<int:id>
1. Getting Started
1.1. Backend Structure : Main Files
all the backend code is following pip8.

├── trivia.psql  *** sql script to create database
├── run.py *** Instance of the app. to run is use `` python app.py ``
├── README.md
├── config.py *** Configurations file containing Database URLs, ... etc
├── models.py *** Contains SQLAlchemy models.
├── test_flaskr.py *** Containing unittest functions
├── requirements.txt *** The dependencies we need to install with `` pip3 install -r requirements.txt ``
├── .env *** create this file for the environment variables
└── flaskr
    └── __init__.py *** Contains routes and controllers
1.2. Installing Dependencies
1.2.1. Python 3.8
Follow instructions to install the latest version of python for your platform in the python docs

1.2.2. Virtual Environment
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the python docs

1.2.3. PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by navigating to the /backend directory and running:

pip install -r requirements.txt
This will install all the required packages we selected within the requirements.txt file.

1.2.4. Project Key Dependencies
Flask is a lightweight backend micro-services framework. Flask is required to handle requests and responses.

SQLAlchemy is the Python SQL toolkit and ORM. You'll primarily work in flaskr/__init__.py and can reference models.py.

Flask-CORS is the extension we'll use to handle cross origin requests from our frontend server.

2. setting up
Follow these setup instructions to get the project up and running

2.1. setting up the environment variables
Before running the project, you have to set in a .env file in the backend folder the environment variables below:

PROD_DATABASE_URI, DEV_DATABASE_URI, and TEST_DATABASE_URI: Set the database URIs for SQLAlchemy for the different configuration classes.
SECRET_KEY: set the secret key for the configuration classes
API_ENV: set each configuration class you want the app to run on it
# Production DB URI
PROD_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/trivia'
# development DB URI
DEV_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/trivia_dev'
# testing DB URI
TEST_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/trivia_test'
# the secret key
SECRET_KEY='+\xec\xaa\xddN)$\xdb"\xed\x9e\xcb\xc0\xe2\xab'
# specify if you want to run the app on [development, testing, production]
API_ENV='development'
2.2. Database Setup
With Postgres running and our trivia database created, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

psql trivia_dev < trivia.psql
notice that I've used the trivia_dev database, as I want to run the app in the development environment. For more information, checkout the PostgreSQL Docs

3. Running the server
From within the backend directory first ensure you are working using your created virtual environment.

To run the server, execute:

python run.py
4. Testing
In this project we are using unittest to test all functionalities. Create a testing database and store the URI in the TEST_DATABASE_URI environment variable. To run the tests, run

# if exists, drop the testing database and create it again
dropdb trivia_test
createdb trivia_test
# restore the trivia dump file to the testing database
psql trivia_test < trivia.psql
# finally, from the `backend` directory, run
python test_flaskr.py
5. API Reference
5.1. General
Base URL: this app is hosted locally under the port 5000. The API base URL is http://localhost:5000/api/v1.0
Authentication: this app doesn't require any authentication or API tokens.
You must set the header: Content-Type: application/json with every request.
you can use Postman, Curl or the vscode extension Thunter Client to test manually this API.

5.2. error Handlers
if any errors occurred, the API will return a json object in the following format:

{
    "success": false,
    "error": 404,
    "message": "resource not found"
}
The following errors will be reported:

400: bad request || The request was unacceptable, often due to missing a required parameter.
404: resource not found || The requested resource doesn't exist.
405: method not allowed || the request method is known by the server but is not supported by the target resource.
422: unprocessible || indicates that the server understands the content type of the request entity, and the syntax of the request entity is correct, but it was unable to process the contained instructions.
500: internal server error || Something went wrong on Trivia App's end. (These are rare.)
5.3. Endpoints
5.3.1. GET /categories
Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.

Request Arguments: None

Returns: An object with two keys:

success (can be true or false; true if the request success)
categories: contains an object of:
id: category_string key:value pairs.
Example response:

{
  "categories": {
    "1": "history",
    "2": "art",
    "3": "sports",
    "4": "geography",
    "5": "science"
  },
  "success": true
}
5.3.2. GET /questions
Fetches a dictionary of paginated questions, as well as a dictionary of categories.

Request arguments:

optional URL queries:
page: an optional integer for a page number, which is used to fetch 10 questions for the corresponding page.
default: 1
Returns: An object with 4 keys:

categories: a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
id (str): id category
category (str): category text
questions: a list that contains paginated questions objects, that correspond to the page query.
id (int): Question id.
question (str): Question text.
difficulty (int): Question difficulty.
category (str): question category id.
total_questions (int): an integer that contains total questions
success (can be true or false; true if the request success)
Example response:

{
  "categories": {
    "1": "history",
    "2": "art",
    "3": "sports",
    "4": "geography",
    "5": "science"
  },
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": "1",
      "difficulty": 4,
      "id": 1,
      "question": "What boxers original name is Cassius Clay?"
    },
    {
      "answer": "Lake Victoria",
      "category": "1",
      "difficulty": 3,
      "id": 2,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Agra",
      "category": "2",
      "difficulty": 5,
      "id": 3,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Mona Lisa",
      "category": "3",
      "difficulty": 2,
      "id": 4,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "Alexander Fleming",
      "category": "4",
      "difficulty": 1,
      "id": 5,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Flask",
      "category": "5",
      "difficulty": 2,
      "id": 7,
      "question": "What is the application used to build great python backends?"
    },
    {
      "answer": "Flask",
      "category": "5",
      "difficulty": 2,
      "id": 8,
      "question": "What is the application used to build great python backends?"
    },
    {
      "answer": "younes",
      "category": "5",
      "difficulty": 5,
      "id": 9,
      "question": "who I am?"
    },
    {
      "answer": "younes",
      "category": "5",
      "difficulty": 5,
      "id": 10,
      "question": "who I am?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 11,
      "question": "when python is created?"
    }
  ],
  "success": true,
  "total_questions": 21
}
5.3.3. GET /categories/<int:id>/questions
Fetches a dictionary of paginated questions that are in the category specified in the URL parameters.

Request arguments:

optional URL queries:
page: an optional integer for a page number, which is used to fetch 10 questions for the corresponding page.
default: 1
Returns: An object with 4 keys:

current_category (str): a string that contains the category type for the selected category.
questions (list): a list that contains paginated questions objects, that correspond to the page query.
id (int): Question id.
question (str): Question text.
difficulty (int): Question difficulty.
category (str): question category id.
total_questions (int): an integer that contains total questions in the selected category.
success (can be true or false; true if the request success)
Example response:

{
  "current_category": "history",
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": "1",
      "difficulty": 4,
      "id": 1,
      "question": "What boxers original name is Cassius Clay?"
    },
    {
      "answer": "Lake Victoria",
      "category": "1",
      "difficulty": 3,
      "id": 2,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 11,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 12,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 13,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 14,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 17,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 18,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 19,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 20,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 21,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 23,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 24,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 26,
      "question": "when python is created?"
    }
  ],
  "success": true,
  "total_questions": 14
}
5.3.4. POST /questions
Posts a new question.

Request arguments:

Json object:
question (str): A string that contains the question text.
answer (str): A string that contains the answer text.
difficulty (str): An integer that contains the difficulty, please note that difficulty can be from 1 to 5.
category (int): An integer that contains the category id.
Returns: an object with the following keys:

id (int): an integer that contains the ID for the created question.
question (str): A string that contains the text for the created question.
questions (list): a list that contains paginated questions objects.
id (int): Question id.
question (str): Question text.
difficulty (int): Question difficulty.
category (str): question category id.
total_questions (int): an integer that contains total questions.
success (can be true or false; true if the request success)
Example response:
post this question:

{
    "question": "when python is created?",
    "answer": "1991",
    "difficulty": 3,
    "category": 1
}
response:

{
  "id": 27,
  "question": "when python is created?",
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": "1",
      "difficulty": 4,
      "id": 1,
      "question": "What boxers original name is Cassius Clay?"
    },
    {
      "answer": "Lake Victoria",
      "category": "1",
      "difficulty": 3,
      "id": 2,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Agra",
      "category": "2",
      "difficulty": 5,
      "id": 3,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Mona Lisa",
      "category": "3",
      "difficulty": 2,
      "id": 4,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "Alexander Fleming",
      "category": "4",
      "difficulty": 1,
      "id": 5,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Flask",
      "category": "5",
      "difficulty": 2,
      "id": 7,
      "question": "What is the application used to build great python backends?"
    },
    {
      "answer": "Flask",
      "category": "5",
      "difficulty": 2,
      "id": 8,
      "question": "What is the application used to build great python backends?"
    },
    {
      "answer": "younes",
      "category": "5",
      "difficulty": 5,
      "id": 9,
      "question": "who I am?"
    },
    {
      "answer": "younes",
      "category": "5",
      "difficulty": 5,
      "id": 10,
      "question": "who I am?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 11,
      "question": "when python is created?"
    }
  ],
  "success": true,
  "total_questions": 22
}
5.3.5. POST /questions/search
Search for a question.

Request arguments:

Json object:
searchTerm (str): a string that contains the search term to search with.
Returns: an object with the following keys:

questions (list): a list that contains paginated questions objects, derived from the search term.
id (int): Question's id.
question (str): Question text.
difficulty (int): Question's difficulty.
category (str): question category id.
total_questions (int): an integer that contains total questions returned from the search.
success (can be true or false; true if the request success)
Example response:
search with this:

{
    "searchTerm" : "python"
}
response :

{
  "questions": [
    {
      "answer": "Flask",
      "category": "5",
      "difficulty": 2,
      "id": 7,
      "question": "What is the application used to build great python backends?"
    },
    {
      "answer": "Flask",
      "category": "5",
      "difficulty": 2,
      "id": 8,
      "question": "What is the application used to build great python backends?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 11,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 12,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 13,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 14,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 17,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 18,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 19,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 20,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 21,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 23,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 24,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 26,
      "question": "when python is created?"
    },
    {
      "answer": "1991",
      "category": "1",
      "difficulty": 3,
      "id": 27,
      "question": "when python is created?"
    }
  ],
  "success": true,
  "total_questions": 15
}
5.3.6. POST /quizzes
Allows the user to play the quiz game, returning a random question that is not in the previous_questions list.

Request arguments:

Json object:
quiz_category: A dictionary that contains the category id.
id (int): the category id to get the random question from. use 0 to get a random question from all categories.
previous_questions (list): A list that contains the IDs of the previous questions.
Returns: an object with the following keys :

question (dict) that has the following data:
id (int): question's ID.
question (str): question's question text.
answer (str): question's answer text.
difficulty (int): question's difficulty
category (str): category's ID.
success (boolean): (can be true or false; true if the request success)
Example response:
try with this:

{
  "quiz_category" : {
      "id":5
  },
  "previous_questions" : [7, 10, 8]
}
response:

{
  "question": {
    "answer": "younes",
    "category": "5",
    "difficulty": 5,
    "id": 9,
    "question": "who I am?"
  },
  "success": true
}
try with this:

{
  "quiz_category" : {
      "id":5
  },
  "previous_questions" : [7, 10, 8, 9]
}
response:

{
  "question": null,
  "success": true
}
5.3.7. DELETE /questions/<int:id>
Deletes the question by the id specified in the URL parameters.

Request arguments: None

Returns: A dictionary that contain:

deleted (int): question_id
success (can be true or false; true if the request success)
Example response:

{
  "deleted": 7,
  "success": true
}
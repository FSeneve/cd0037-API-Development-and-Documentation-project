import os
from flask import Flask, request, abort, jsonify
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start: end]
    return current_questions

def create_app(config=None):
    app = Flask(__name__)

    app.config.from_object('config.DevConfig')
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTION')
        response.headers.add('Content-Type', 'application/json')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/api/v1.0/categories', methods=['GET'])
    def retreive_categories():
        ''' get all categories '''

        categories = Category.query.order_by(Category.id).all()
        if len(categories) == 0:
            abort(404)

        formatted_categories = {
            category.id: category.type for category in categories
        }

        return jsonify({
            'success': True,
            'categories': formatted_categories
        }), 200

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/api/v1.0/questions', methods=['GET'])
    def retreive_questions():
        ''' get 10 questions per page '''

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        categories = Category.query.order_by(Category.type).all()
        formatted_categories = {
            category.id: category.type for category in categories
        }

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': formatted_categories,
        }), 200

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/api/v1.0/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        ''' DELETE question from database using a question ID '''

        question = Question.query.filter(
            Question.id == int(question_id)).one_or_none()
        if question is None:
            abort(404)
        try:
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            }), 200

        except BaseException:
            db.session.rollback()
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/api/v1.0/questions", methods=['POST'])
    def new_question():
        ''' create a new question, which will require the question and
            answer text, category, and difficulty score
        '''

        body = request.get_json()

        if not body:
            abort(400)

        if (body.get('question') and body.get('answer')
                and body.get('difficulty') and body.get('category')):
            new_question = body.get('question')
            new_answer = body.get('answer')
            new_category = body.get('category')
            new_difficulty = body.get('difficulty')

            # insure that difficulty is only from 1 to 5
            if not 0 < int(new_difficulty) < 6:
                abort(400)
            try:
                question = Question(
                    new_question,
                    new_answer,
                    new_category,
                    new_difficulty)
                question.insert()

                selection = Question.query.order_by(Question.id).all()

                return jsonify({
                    'success': True,
                    'id': question.id,
                    'question': question.question,
                    'questions': paginate_questions(request, selection),
                    'total_questions': len(selection)
                })
            except BaseException:
                # creating the question failed, rollback and close the
                # connection
                db.session.rollback()
                abort(422)
        else:
            # anything else posted in the body should return a 400 error
            abort(400)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/api/v1.0/questions/search", methods=['POST'])
    def search_questions():
        ''' get questions based on a search term.
            It should return any questions for whom the search term is a
            substring of the question
        '''

        body = request.get_json()
        if not body:
            abort(400)
        search_term = body.get('searchTerm')
        if search_term:
            search_results = Question.query.filter(
                    Question.question.ilike(f"%{search_term}%")
                ).all()

            if len(search_results) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': [
                        question.format() for question in search_results
                    ],
                'total_questions': len(search_results),
            }), 200
        else:
            abort(400)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/api/v1.0/categories/<int:category_id>/questions',
               methods=['GET'])
    def retreive_questions_by_category(category_id):
        ''' get all questions based on a specific category '''

        category = Category.query.filter(
            Category.id == int(category_id)).one_or_none()

        # abort with a 404 error if category is unavailable
        if category is None:
            abort(404)
        questions_by_category = Question.query.filter(
            Question.category == str(category.id)).all()

        if len(questions_by_category) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': [
                    question.format() for question in questions_by_category
                ],
            'total_questions': len(questions_by_category),
            'current_category': category.type
        }), 200

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/api/v1.0/quizzes', methods=['POST'])
    def play_quiz():
        '''
        POST endpoint to get questions to play the quiz.
        This endpoint should take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.
        '''

        body = request.get_json()

        if (body.get('previous_questions') is None) or (
                body.get('quiz_category') is None):
            # if previous_questions or quiz_category are missing or None,
            # return bad request
            abort(400)

        category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')
        if not isinstance(previous_questions, list):
            # if previous_questions is not an instance of list return a bad
            # request
            abort(400)
        if int(category['id']) == 0:
            # if the category id is 0, query the database for a random question
            # of all questions
            available_questions = Question.query.order_by(func.random())
        else:
            available_questions = Question.query.filter(
                Question.category == str(category['id'])
            ).order_by(func.random())

        if len(available_questions.all()) == 0:
            abort(404)
        else:
            question = available_questions.filter(
                Question.id.notin_(previous_questions)).first()

        if question is None:
            return jsonify({
                'success': True,
                'question': None
            }), 200

        return jsonify({
            'success': True,
            'question': question.format()
        }), 200

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "method not allowed"
        }), 405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "internal server error"
        }), 500
    

    return app


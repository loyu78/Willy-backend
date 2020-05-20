import os
import django
import csv
import sys

os.chdir(".")
print("Current dir=", end=""), print(os.getcwd())

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR=", end=""), print(BASE_DIR)

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "willy.settings")
django.setup()

from product.models import *
from order.models import *
from information.models import *
from user.models import *
from survey.models import *

CSV_PATH = './willy_csv/homes.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Home.objects.create(
            image_url = row['image_url'],
            title = row['title'],
            content = row['content']
        )

CSV_PATH = './willy_csv/product_headers.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        ProductHeader.objects.create(
            image_url = row['image_url'],
            title = row['title'],
            content = row['content']
        )

CSV_PATH = './willy_csv/delivery_status.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        DeliveryStatus.objects.create(
            status = row['status']
        )

CSV_PATH = './willy_csv/payments.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Payment.objects.create(
            name = row['name']
        )

CSV_PATH = './willy_csv/explanations.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Explanation.objects.create(
            image_url = row['image_url'],
            title = row['title'],
            content = row['content']
        )

CSV_PATH = './willy_csv/categories.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Category.objects.create(
            name = row['name'],
            image_url = row['image_url']
        )

CSV_PATH = './willy_csv/products.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Product.objects.create(
            name = row['name'],
            subscribe = row['subscribe'],
            image_url = row['image_url'],
            sub_name = row['sub_name'],
            color = row['color'],
            price = row['price'],
            header_image_url = row['header_image_url'],
            header_description = row['header_description'],
            day = row['day'],
            pill_image_url = row['pill_image_url'],
            pill_description = row['pill_description'],
            pill_sub_description = row['pill_sub_description'],
            pill_sub_image_url = row['pill_sub_image_url'],
            ingredient = row['ingredient'],
            manual_url = row['manual_url']
        )

CSV_PATH = './willy_csv/sections.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Section.objects.create(
            product = Product.objects.get(id=row['products_id']),
            bottle = row['bottle'],
            title = row['title'],
            effects = row['effects'],
            point = row['point'],
            video_url = row['video_url']
        )

CSV_PATH = './willy_csv/products_categories.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        ProductCategory.objects.create(
            product = Product.objects.get(id=row['products_id']),
            category = Category.objects.get(id=row['categories_id'])
        )

CSV_PATH = './willy_csv/reviews.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Review.objects.create(
            name = row['name'],
            product_list = row['product_list'],
            image_url = row['image_url'],
            subscription = row['subscription'],
            created_at = row['created_at'],
            content = row['content']
        )

CSV_PATH = './willy_csv/products_reviews.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        ProductReview.objects.create(
            product = Product.objects.get(id=row['products_id']),
            review = Review.objects.get(id=row['reviews_id'])
        )

CSV_PATH = './willy_csv/product_explanations.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        ProductExplanation.objects.create(
            product = Product.objects.get(id=row['products_id']),
            content = row['content'],
            sub_content = row['sub_content'],
            product_content = row['product_content']
        )

CSV_PATH = './willy_csv/frequent_questions.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        FrequentQuestion.objects.create(
            product = Product.objects.get(id=row['products_id']),
            question = row['question'],
            answer = row['answer'],
            image_url = row['image_url']
        )

CSV_PATH = './willy_csv/materials.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Material.objects.create(
            product = Product.objects.get(id=row['products_id']),
            nutrial = row['nutrials'],
            image_url = row['image_url'],
            precautions = row['precautions']
        )

CSV_PATH = './willy_csv/survey_types.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        SurveyType.objects.create(
            name = row['name']
        )

CSV_PATH = './willy_csv/survey_questions.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        SurveyQuestion.objects.create(
            survey_type = SurveyType.objects.get(id=row['survey_types_id']),
            question = row['question'],
            sub_question = row['sub_question'],
            image_url = row['image_url'],
            limit = row['limit']
        )

CSV_PATH = './willy_csv/survey_answers.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        SurveyAnswer.objects.create(
            survey_question = SurveyQuestion.objects.get(id=row['survey_questions_id']),
            answer = row['answer']
        )

CSV_PATH = './willy_csv/next_questions.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        NextQuestion.objects.create(
            survey_answer = SurveyAnswer.objects.get(id=row['survey_answers_id']),
            survey_question = SurveyQuestion.objects.get(id=row['survey_questions_id'])
        )

CSV_PATH = './willy_csv/result_lists.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        ResultList.objects.create(
            title = row['title'],
            color = row['color']
        )

CSV_PATH = './willy_csv/recommended_products.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        RecommendedProduct.objects.create(
            product = Product.objects.get(id=row['products_id']),
            image_url = row['image_url'],
            title = row['title'],
            content = row['content'],
            highlight = row['highlight'],
            rating = row['rating']
        )

CSV_PATH = './willy_csv/suitable_pills.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        SuitablePill.objects.create(
            survey_answer = SurveyAnswer.objects.get(id=row['survey_answers_id']),
            recommended_product = RecommendedProduct.objects.get(id=row['recommended_products_id'])
        )

CSV_PATH = './willy_csv/image_descriptions.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        ImageDescription.objects.create(
            recommended_product = RecommendedProduct.objects.get(id=row['recommended_products_id']),
            content = row['content']
        )

CSV_PATH = './willy_csv/product_contents.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        ProductContent.objects.create(
            recommended_product = RecommendedProduct.objects.get(id=row['recommended_products_id']),
            title = row['title'],
            content = row['content'],
            highlight = row['highlight'],
            link = row['link']
        )

CSV_PATH = './willy_csv/point_products.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        PointProduct.objects.create(
            name = row['name'],
            price = row['price'],
            hashtag = row['hashtag'],
            image_url = row['image_url'],
            detail = row['detail'],
            brand = row['brand']
        )

CSV_PATH = './willy_csv/point_image_lists.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        PointImageList.objects.create(
            point_product = PointProduct.objects.get(id=row['point_products_id']),
            image_url = row['image_url']
        )

CSV_PATH = './willy_csv/news_types.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        NewsType.objects.create(
            name = row['name']
        )

CSV_PATH = './willy_csv/pilly_news.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        PillyNews.objects.create(
            news_type = NewsType.objects.get(id=row['news_types_id']),
            title = row['title'],
            content = row['content'],
            created_at = row['created_at']
        )

CSV_PATH = './willy_csv/question_types.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        QuestionType.objects.create(
            name = row['name']
        )

CSV_PATH = './willy_csv/questions.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Question.objects.create(
            question_type = QuestionType.objects.get(id=row['question_types_id']),
            title = row['title'],
            content = row['content'],
            created_at = row['created_at']
        )

CSV_PATH = './willy_csv/notices.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Notice.objects.create(
            title = row['title'],
            content = row['content'],
        )

CSV_PATH = './willy_csv/pilly_stories.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        PillyStory.objects.create(
            image_url = row['image_url'],
            name = row['name'],
        )

CSV_PATH = './willy_csv/story_informations.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        StoryInformation.objects.create(
            pilly_story = PillyStory.objects.get(id=row['pilly_stories_id']),
            title = row['title'],
            image_url = row['image_url'],
            content = row['content'],
            description = row['description']
        )



#product_notices.csv
#homes.csv
#products_headers.csv
#delivery_status.csv
#payments.csv
#explanations.csv
#categories.csv
#products.csv
#sections.csv
#products_categories.csv
#reviews.csv
#products_reviews.csv
#product_explanations.csv
#frequent_questions.csv
#materials.csv
#survey_types.csv
#survey_questions.csv
#survey_answers.csv
#next_questions.csv
#result_lists.csv
#recommended_products.csv
#suitable_pills.csv
#image_descriptions.csv
#products_contents.csv
#point_products.csv
#point_image_list.csv
#news_types.csv
#pilly_news.csv
#question_types.csv
#questions.csv
#notices.csv
#pilly_stories.csv
#story_informations.csv

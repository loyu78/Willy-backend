import json

from django.http        import JsonResponse, HttpResponse
from django.views       import View
import queue

from .models import SurveyType, SurveyQuestion, SurveyAnswer, CustomerInformation, CustomerAnswer, SuitablePill, SurveyComment, RecommendedProduct, ImageDescription, SurveyResult, ResultList, ProductContent
from product.models import Product, ProductExplanation

class SurveyView(View):

    def post(self, request):
        data = json.loads(request.body)

        try:
            question_id = data['question']
            answers = data['answer']
            box = data['box']
            person_id = data['person_id']

            if question_id == 27:           #마지막 문항일 때
                return JsonResponse({'message':'finish'}, status=200)

            nextQuestions=set()
            survey_object= SurveyQuestion.objects.select_related('survey_type').prefetch_related('surveyanswer_set')

            if box == 'textbox':            #textbox(서술형일 때)

                person = CustomerInformation.objects.get(id=person_id)
                if question_id == 1:
                    person.name = answers[0]
                    print(person.name)
                    person.save()

                elif question_id == 3:
                    person.age = answers[0]
                    person.save()

                elif question_id == 14:
                    person.height = answers[0]
                    person.save()

                elif question_id == 15:
                    person.weight = answers[0]
                    person.save()

                question_id+=1
                nextQuestions.add(SurveyAnswer.objects.get(id=question_id).id)

            else:                           #textbox가 아닐 때(객관식일 때)
                survey_object= SurveyQuestion.objects.select_related('survey_type').prefetch_related('surveyanswer_set')

                if question_id == 2:
                    person = CustomerInformation.objects.get(id=person_id)
                    person.gender = SurveyAnswer.objects.get(id=answers[0]).answer
                    person.save()

                if question_id == 4:
                    for answer in answers:
                        person_answer = CustomerAnswer.objects.create()
                        person_answer.customer_information_id = person_id
                        person_answer.question = 4
                        person_answer.answer = answer
                        person_answer.save()

                if data['answer']==[0]:     #설문조사의 시작
                    nextQuestions.add(1)
                    person = CustomerInformation.objects.create()

                else:
                    for answer in answers:
                        nextQuestions.add(SurveyAnswer.objects.get(id=answer).next_question)

                        person = CustomerInformation.objects.get(id=person_id)

            nextQuestions = list(nextQuestions)

            result=[]

            for nextQuestion in nextQuestions:
                survey = survey_object.get(id=nextQuestion)
                survey_list={
                    "person_id":person.id,
                    "id":survey.id,
                    "type":survey.survey_type.name,
                    "question":survey.question,
                    "detail_question":survey.detail_question,
                    "sub_question":survey.sub_question,
                    "image_url":survey.image_url,
                    "limit":survey.limit,
                    "percentage":survey.percentage,
                    "answer_list":list(survey.surveyanswer_set.values())
                }
                result.append(survey_list)
            return JsonResponse({"survey":result}, status=200)

        except KeyError:
            return HttpResponse(status=400)

class SurveyResultView(View):

    def post(self, request):
        data = json.loads(request.body)
        person_id = data['person_id']
        try:
            person = CustomerInformation.objects.get(id = person_id)

            person.bmi = int(person.weight)/(int(person.height)*2)
            person.save()

            person_answer = CustomerAnswer.objects.filter(customer_information_id=person_id)

            count=0

            person_comment_result=[]
            person_pills_result=set()

            for man in person_answer.values():
                mans = man['answer']
                person_comment = SurveyComment.objects.get(survey_answer_id=mans).comment
                person_pill = SuitablePill.objects.get(id=mans).recommended_product_id
                person_pills = RecommendedProduct.objects.select_related("product").prefetch_related("productcontent_set").prefetch_related("imagedescription_set").get(id=person_pill)
                person_pills_result.add(person_pills)
                person_comment_result.append(person_comment)
                count+=1

            [print(a.product_id)for a in person_pills_result]

            person_comment= SurveyComment.objects.filter()

            if len(person_answer)==0 or len(person_answer)==1:
                result_list = ResultList.objects.get(id=2)

            elif len(person_answer)==2:
                result_list = ResultList.objects.get(id=3)

            elif len(person_answer)==3:
                result_list = ResultList.objects.get(id=1)

            result = {
                "Banner":{
                    "name":person.name,
                    "type":result_list.color,
                    "summary":result_list.title,
                    "prescriptions":list(person_comment_result)
                },
                "UserInfo":{
                    "age":person.age,
                    "sex":person.gender,
                    "bmi":person.bmi
                },
                "Summary":{
                    "name":person.name,
                    "height":person.height
                },
                "Recommendations":{
                    "amount":count,
                    "name":person.name,
                    "nutrients":[
                                {
                                 "product_id":pill.product.id,
                                 "name":pill.product.name,
                                 "effects":list(ProductExplanation.objects.filter(product_id=pill.product_id).values('content','sub_content','product_content')),
                                 "point":pill.rating,
                                 "needs":list(pill.productcontent_set.values()),
                                 "importants":[
                                     {
                                        "title":pill.title,
                                        "description":pill.content,
                                        "highlights":pill.highlight
                                     }
                                 ],
                                 "nutrient":{
                                     "image":pill.image_url,
                                     "list":[description['content']for description in pill.imagedescription_set.values('content')]
                            }
                        }for pill in person_pills_result]
                }
            }
            return JsonResponse({"survey_result":result}, status=200)


        except KeyError:
            return HttpResponse(status=400)


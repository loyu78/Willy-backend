import json

from django.views       import View
from django.http        import HttpResponse, JsonResponse

from .models            import Product, Review, ProductReview, ProductExplanation, Category, ProductCategory, ProductExplanation, Review, Section, Material, FrequentQuestion, Explanation
from information.models import ProductHeader

# 고객 후기 리스트 api
class ReviewList(View):
	def get(self, request):
		product = request.GET.get('product', Review.objects.all())
		offset = int(request.GET.get('offset', 1))
		limit = int(request.GET.get('limit', 9))
		page = offset*limit

		try:
			reviews = Review.objects.values()
			data = [
				{
					'id':review['id'],
					'name':review['name'],
					'products':review['product_list'],
					'subscription':review['subscription'],
					'image':review['image_url'],
					'created_at':review['created_at'],
					'content':review['content']
				} for review in reviews[page-limit:page]
			]
			return JsonResponse({'reviews':data}, status=200)
		except KeyError:
			return JsonResponse({'message':'key error'}, status=400)

# 고객 후기 상세 api
class ReviewDetail(View):
	def get(self, request, review_id):
		try:
			product_list = ProductReview.objects.prefetch_related('product').filter(review_id=review_id)
			review = Review.objects.prefetch_related('productreview_set').get(id=review_id)
			data = [
				{
					'id':review.id,
					'name':review.name,
					'products':review.product_list,
					'subscription':review.subscription,
					'image':review.image_url,
					'created_at':review.created_at,
					'content':review.content,
				}
			]
			products = [
				{
					'name':product.product.name,
					'image':product.product.image_url,
					'content': list(ProductExplanation.objects.filter(product_id=product.product.id).values('content','sub_content','product_content'))
				} for product in product_list
			]
			return JsonResponse({'review':data, 'side_products':products}, status=200)
		except KeyError:
			return JsonResponse({'message':'KeyError'}, status=400)

class ProductView(View):
    def get(self, request):
        product_header = ProductHeader.objects.filter(id=1).values()
        result = [{'product_header':list(product_header)}]
        products = Product.objects.values('id','image_url','day','sub_name','name','price','color')

        for product in products:

            category_image = ProductCategory.objects.select_related("category").filter(product_id=product['id'])

            description = ProductExplanation.objects.filter(product_id=product['id']).values('content','sub_content','product_content')
            category_image_list = [image.category.image_url for image in category_image]

            product_list = {
                'id':product['id'],
                'image_url':product['image_url'],
                'day':product['day'],
                'sub_name':product['sub_name'],
                'name':product['name'],
                'price':product['price'],
                'color':product['color'],
                'description':list(description),
                'category_image':list(category_image_list)
            }
            result.append(product_list)

        return JsonResponse({'products':result}, status =200)

class ProductDetailView(View):
    def get(self, request, products_id):

        explanation_list = Explanation.objects.all().values()

        result = [{"explanation_list":list(explanation_list)}]

        product_category_list = Product.objects.prefetch_related("productcategory_set").get(id=products_id).product_category.values('image_url','name')
        result.append({"product_category":list(product_category_list)})

        section_list = Product.objects.prefetch_related("section_set").get(id=products_id).section_set.values()
        result.append({"section_list":list(section_list)})

        frequent_question_list = Product.objects.prefetch_related("frequentquestion_set").get(id=products_id).frequentquestion_set.values()
        result.append({"frequent_question_list":list(frequent_question_list)})

        material_list = Product.objects.prefetch_related("material_set").get(id=products_id).material_set.values()
        result.append({"material_list":list(material_list)})

        products = Product.objects.filter(id=products_id).values(
            'id',
            'header_image_url',
            'sub_name','name',
            'header_description',
            'header_description',
            'day',
            'price',
            'pill_image_url',
            'pill_description',
            'pill_sub_description',
            'pill_sub_image_url',
            'ingredient',
            'manual_url'
        )

        result.append({"product_list":list(products)})

        return JsonResponse({"product_detail":result}, status=200)


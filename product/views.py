import json

from django.http import JsonResponse, HttpResponse
from django.views import View

from .models import Product, Review, ProductReview, ProductExplanation

class ReviewList(View):
	def get(self, request):
		product = request.GET.get('product', Review.objects.all())
		offset = int(request.GET.get('page', 1))
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

class ReviewDetail(View):
	def get(self, request, review_id):
		try:
			product_list = ProductReview.objects.prefetch_related('product').filter(review_id=review_id)
			review = Review.objects.prefetch_related('productreview_set__product__productexplanation_set').get(id=review_id)
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
			return JsonResponse({'reviews':data, 'side_products':products}, status=200)
		except KeyError:
			return JsonResponse({'message':'KeyError'}, status=400)

import json

from django.http import JsonResponse, HttpResponse
from django.views import View

from .models import PointProduct, PointImageList


class PointProductList(View):
	def get(self, request):
		products = PointProduct.objects.values()
		point_products = [
			{
				'id':product['id'],
				'brand':product['brand'],
				'hashtag':product['hashtag'],
				'name':product['name'],
				'point':product['price'],
				'image_url':product['image_url']
			} for product in products
		]
		return JsonResponse({'point_products':point_products}, status=200)

class PointProductDetail(View):
	def get(self, request, product_id):
		try:
			product = PointProduct.objects.prefetch_related('pointimagelist_set').get(id=product_id)
			images = product.pointimagelist_set.filter(point_product_id=product_id)
			point_product = {
				'id':product.id,
				'brand':product.brand,
				'hashtag':product.hashtag,
				'name':product.name,
				'point':product.price,
				'image_url':product.image_url,
				'description':product.detail,
				'images':[image.image_url for image in images]
			}
			return JsonResponse({'detail':point_product}, status=200)
		except KeyError:
			return JsonResponse({'message':'KeyError'}, status=400)

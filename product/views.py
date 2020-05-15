import json

from django.http import JsonResponse, HttpResponse
from django.views import View

from .models import PointProduct, PointImageList


class PointProductList(View):
	def get(self, request):
		result = []
		products = PointProduct.objects.values()

		for product in products:
			point_products = {
				'id':product['id'],
				'brand':product['brand'],
				'hashtag':product['hashtag'],
				'name':product['name'],
				'point':product['price'],
				'image_url':product['image_url']
			}
			result.append(point_products)
		return JsonResponse({'point_products':result}, status=200)

class PointProductDetail(View):
	def get(self, request, product_id):
		result = []
		result_images = []
		images = PointImageList.objects.filter(point_product_id=product_id).select_related('point_product')

		for product in images:
			result_images.append(product.image_url)

		point_products = {
			'id':product.point_product.id,
			'brand':product.point_product.brand,
			'hashtag':product.point_product.hashtag,
			'name':product.point_product.name,
			'point':product.point_product.price,
			'image_url':product.point_product.image_url,
			'description':product.point_product.detail,
			'images':result_images
		}
		result.append(point_products)

		return JsonResponse({'detail':result}, status=200)


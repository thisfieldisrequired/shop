import redis
from django.conf import settings
from .models import Product

r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


class Recommender:
    """Рекомендации товаров на основе предыдущих покупок"""

    def get_product_key(self, id):
        return f"product:{id}:purchased_with"

    def product_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for (
                with_id
            ) in product_ids:  # получить другие товары купление вместе с каждым товаром
                if product_id != with_id:
                    r.zincrby(
                        self.get_product_key(product_id), 1, with_id
                    )  # увеличить бал товара

    def suggest_products_for(self, products, max_results=6):
        """Рекомндуемые товары"""
        products_ids = [p.id for p in products]
        if len(products) == 1:
            suggestions = r.zrange(
                self.get_product_key(products_ids[0]), 0, -1, desc=True
            )[:max_results]
        else:
            flat_ids = "".join([str(id) for id in products_ids])
            tmp_key = f"tmp_{flat_ids}"
            keys = [self.get_product_key(id) for id in products_ids]
            r.zinterstore(tmp_key, keys)
            r.zrem(tmp_key, *products_ids)
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list("id", flat=True):
            r.delete(self.get_product_key(id))

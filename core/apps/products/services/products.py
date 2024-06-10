from abc import ABC, abstractmethod
import typing

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.products.filters import ProductFilters
from core.apps.products.entites.products import Product
from core.apps.products.models.products import Product as ProductDTO


class BaseProductService(ABC):

    @abstractmethod
    def get_product_list(self, filters: ProductFilters, pagination: PaginationIn) -> typing.Iterable[Product]:
        raise NotImplementedError

    @abstractmethod
    def get_product_count(self, filters: ProductFilters) -> int:
        raise NotImplementedError


class ORMProductService(BaseProductService):

    def _build_product_query(self, filters: ProductFilters) -> Q:
        query = Q(is_visible=True)

        if filters.search is not None:
            query &= Q(title__icontains=filters.search) | Q(
                description__icontains=filters.search,
            )

        return query

    def get_product_list(self, filters: ProductFilters, pagination: PaginationIn) -> typing.Iterable[Product]:
        query = self._build_product_query(filters=filters)
        qs = ProductDTO.objects.filter(query)[pagination.offset: pagination.offset + pagination.limit]

        return [product.to_entity() for product in qs]

    def get_product_count(self, filters: ProductFilters) -> int:
        query = self._build_product_query(filters=filters)

        return ProductDTO.objects.filter(query).count()

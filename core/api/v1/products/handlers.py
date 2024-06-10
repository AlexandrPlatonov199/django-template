from django.http import HttpRequest
from ninja import Router, Query

from core.api.filters import PaginationIn
from core.api.shemas import ApiResponse, ListPaginatedResponse, PaginationOut
from core.api.v1.products.filters import ProductFilters
from core.api.v1.products.shemas import ProductSchema
from core.apps.products.services.products import BaseProductService, ORMProductService

router = Router(
    tags=['Products']
)


@router.get('', response=ApiResponse[ListPaginatedResponse[ProductSchema]])
def get_product_list_handler(
        request: HttpRequest,
        filters: Query[ProductFilters],
        pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[ProductSchema]]:
    service: BaseProductService = ORMProductService()
    product_count = service.get_product_count(filters=filters)
    product_list = service.get_product_list(filters=filters, pagination=pagination_in)
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=product_count,
    )
    items = [ProductSchema.from_entity(obj) for obj in product_list]

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))

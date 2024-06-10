from django.urls import path
from django.http import HttpRequest
from ninja import NinjaAPI

from core.api.shemas import PingResponseModel
from core.api.v1.urls import router as v1_router

api = NinjaAPI()


@api.get("/ping", response=PingResponseModel)
def ping(request: HttpRequest) -> PingResponseModel:
    return PingResponseModel(result=True)


api.add_router('v1/', v1_router)


urlpatterns = [
    path("", api.urls),
]
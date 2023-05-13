from django.urls import path
from .views import CategoryViewSet, QusetionViewSet, AnswerViewSet



urlpatterns = [
    path('/category/', CategoryViewSet.as_view({
        "get" : "category_details",
        "post" : "create",
    }), name="category_view_set"),

    path('/category/<id>/', CategoryViewSet.as_view({
        "put" : "update",
    }), name="category_view_set"),

    path('/category/', QusetionViewSet.as_view({
        "get" : "all_questions",
        "post" : "create",
    }), name="category_view_set"),

    path('/category/<id>/', QusetionViewSet.as_view({
        "put" : "update",
    }), name="category_view_set_update"),

    path('/answer/', AnswerViewSet.as_view({
        "get" : "all_answers",
        "post" : "create",
    }), name="category_view_set"),

    path('/answer/<id>/', AnswerViewSet.as_view({
        "put" : "update",
    }), name="category_view_set_update"),
]

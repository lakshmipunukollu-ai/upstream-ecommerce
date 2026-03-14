from rest_framework import generics, filters
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductListSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at', 'title']

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related('category')
        category = self.request.query_params.get('category')
        grade_level = self.request.query_params.get('grade_level')
        if category:
            qs = qs.filter(category__slug=category)
        if grade_level:
            qs = qs.filter(grade_levels__contains=[grade_level])
        return qs


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

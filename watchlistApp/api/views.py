from watchlistApp.models import WatchList,StreamingPlatform, Review
from watchlistApp.api.serializers import WatchListSerializer,StreamPlatformSerializer ,ReviewSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status, mixins, generics, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from watchlistApp.api.permissions import ReviewUserOrReadOnly, IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlistApp.api.pagination import WatchlistPagination


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
       username = self.request.query_params.get('username', None)
       return Review.objects.filter(review_user__username=username)
       
    
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist= movie, review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError("Already reviewed on this watch list")
        
        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2 
        
        movie.number_rating = movie.number_rating + 1
        movie.save()
        
        serializer.save(watchlist= movie,review_user=review_user)
    
class ReviewList(generics.ListCreateAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes =[IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['rating']
    # filter_backends = [DjangoFilterBackend]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['active', 'description']
    # filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
        
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [ReviewUserOrReadOnly]
    serializer_class = ReviewSerializer



class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [ReviewUserOrReadOnly]
    serializer_class = ReviewSerializer


class StreamPlatformVS(viewsets.ModelViewSet):
    #   permission_classes =[IsAdminOrReadOnly]
      queryset = StreamingPlatform.objects.all()
      serializer_class = StreamPlatformSerializer
    
    
    
class StreamPlatformAv(APIView):
    # permission_classes =[IsAdminOrReadOnly]
    
    def get(self, request):
        platform = StreamingPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True) 
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

        
class StreamPlatformDetailAV(APIView):
    permission_classes =[IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            movie = StreamingPlatform.objects.get(pk=pk)
        except StreamingPlatform.DoesNotExist:
            return Response({'Error': 'WatchList not found'}, status=status.HTTP_404_NOT_FOUND)    
            
        serializer = StreamPlatformSerializer(movie)
        return Response(serializer.data)    
    
    def put(self, request, pk): 
        movie = StreamingPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(movie,data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request ,pk): 
        movie = StreamingPlatform.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
        

class WatchListAv(APIView):
    # permission_classes =[IsAdminOrReadOnly]
    pagination_class = WatchlistPagination
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
      
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class WatchDetailAV(APIView):
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'WatchList not found'}, status=status.HTTP_404_NOT_FOUND)    
            
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)    
    
    def put(self, request, pk): 
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie,data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request ,pk): 
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#      return self.retrieve(request, *args, **kwargs)
 
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
     
#     def post(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    

# class StreamPlatformVS(viewsets.ViewSet):
    
#     def list(self, request):
#         queryset = StreamingPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamingPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self,request):
#         serializer = StreamPlatformSerializer(data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
             
#     def destroy(self, request ,pk): 
#         movie = StreamingPlatform.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

# @api_view(['GET', 'POST'])
# def movie_list(request):
    
#     if request.method == 'GET':
#         movies = WatchList.objects.all()
#         serializer = WatchListSerializer(movies, many=True)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = WatchListSerializer(data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
        
# @api_view(['GET','PUT','DELETE'])
# def movie_details(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({'Error': 'WatchList not found'}, status=status.HTTP_404_NOT_FOUND)    
            
#         serializer = WatchListSerializer(movie)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         movie = WatchList.objects.get(pk=pk)
#         serializer = WatchListSerializer(movie,data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
#     if request.method == 'DELETE':
#         movie = WatchList.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
  

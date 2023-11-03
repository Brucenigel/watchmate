from rest_framework import serializers
from watchlistApp.models import WatchList, StreamingPlatform ,Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review 
        # fields = "__all__"
        exclude = ['watchlist']
        
        
class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = WatchList
        fields = "__all__"
        # fields = ['id', 'name', 'description']
        # exclude = ['active']
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    
    class Meta:
        model = StreamingPlatform
        fields = "__all__"
        

        

# def name_leght(value):
#         if len(value) < 2:
#             raise serializers.ValidationError("Name is too short")

# class WatchListSerializer(serializers.Serializer):
#     id  = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_leght])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self,validated_data):
#         return WatchList.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     def validate(seft, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("should not be the same")
#         else:
#             return data
            
    # def validate_name(self, value):
        
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short")
    #     else:
    #         return value
        
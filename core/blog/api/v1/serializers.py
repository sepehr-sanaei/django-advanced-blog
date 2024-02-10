from rest_framework import serializers
from ...models import Post, Category
from accounts.models import Profiles

# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     content = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.CharField(source="get_snippet", read_only=True)
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        many=False, slug_field="name", queryset=Category.objects.all()
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "category",
            "snippet",
            "status",
            "relative_url",
            "absolute_url",
            "created_date",
            "published_date",
        ]
        read_only_fields = ["author"]

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.id)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("snippet", None)
            rep.pop("absolute_url", None)
            rep.pop("relative_url", None)
        else:
            rep.pop("content", None)
        rep["category"] = CategorySerializer(instance.category).data
        return rep

    def create(self, validated_data):

        validated_data["author"] = Profiles.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)

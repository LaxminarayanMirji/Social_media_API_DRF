from rest_framework import serializers
from app.models import Post, PostComment, PostLike, User, UserFollow
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'profile_picture',
                  'username', 'password', 'bio', 'is_active']

    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    bio = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create_user(
            email=validated_data['email'],
            password=password,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            bio=validated_data.get('bio', ''),)
        user.profile_picture = validated_data.get('profile_picture', None)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'],
                            password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid login credentials")
        return {'user': user}


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'image', 'video',
                  'created_at', 'updated_at', 'user']

    title = serializers.CharField()
    description = serializers.CharField()
    image = serializers.ImageField(required=False)
    video = serializers.FileField(required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = "__all__"

    comment_text = serializers.CharField(max_length=264)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    def save(self, **kwargs):
        validated_data = self.validated_data
        validated_data['post'] = kwargs.get('post')
        return super().save(**validated_data)


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)


class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = "__all__"
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    follows_id = serializers.PrimaryKeyRelatedField(read_only=True)

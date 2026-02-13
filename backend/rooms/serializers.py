from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Room, Player


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ['id', 'user', 'role', 'is_ready', 'score', 'joined_at']


class RoomSerializer(serializers.ModelSerializer):
    player_count = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = [
            'id', 'name', 'creator', 'seed', 'max_players', 'is_public',
            'status', 'current_round', 'total_rounds', 'player_count',
            'is_full', 'players', 'created_at'
        ]
        read_only_fields = ['id', 'creator', 'status', 'current_round']


class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name', 'seed', 'max_players', 'is_public', 'total_rounds']


class JoinRoomSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=Player.ROLE_CHOICES, default='politician')

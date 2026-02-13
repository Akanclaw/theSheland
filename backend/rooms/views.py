import random
import string
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Room, Player
from .serializers import RoomSerializer, RoomCreateSerializer, JoinRoomSerializer, PlayerSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return RoomCreateSerializer
        return RoomSerializer

    def perform_create(self, serializer):
        # 如果没有提供种子，生成一个随机种子
        seed = serializer.validated_data.get('seed')
        if not seed:
            seed = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        serializer.save(creator=self.request.user, seed=seed)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        room = self.get_object()
        serializer = JoinRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 检查是否已在房间
        if Player.objects.filter(room=room, user=request.user).exists():
            return Response({'error': '您已经在该房间'}, status=status.HTTP_400_BAD_REQUEST)

        # 检查房间是否已满
        if room.is_full:
            return Response({'error': '房间已满'}, status=status.HTTP_400_BAD_REQUEST)

        # 检查游戏是否已开始
        if room.status != 'waiting':
            return Response({'error': '游戏已经开始'}, status=status.HTTP_400_BAD_REQUEST)

        role = serializer.validated_data.get('role', 'politician')

        # 检查是否已有上帝
        if role == 'god' and room.players.filter(role='god').exists():
            return Response({'error': '该房间已经有上帝'}, status=status.HTTP_400_BAD_REQUEST)

        player = Player.objects.create(
            room=room,
            user=request.user,
            role=role
        )

        return Response(PlayerSerializer(player).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        room = self.get_object()
        try:
            player = Player.objects.get(room=room, user=request.user)
            player.delete()
            return Response({'status': 'left'})
        except Player.DoesNotExist:
            return Response({'error': '您不在该房间'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def ready(self, request, pk=None):
        room = self.get_object()
        try:
            player = Player.objects.get(room=room, user=request.user)
            player.is_ready = not player.is_ready
            player.save()
            return Response(PlayerSerializer(player).data)
        except Player.DoesNotExist:
            return Response({'error': '您不在该房间'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        room = self.get_object()

        # 只有创建者可以开始游戏
        if room.creator != request.user:
            return Response({'error': '只有房主可以开始游戏'}, status=status.HTTP_403_FORBIDDEN)

        if not room.can_start():
            return Response({'error': '房间未满或所有玩家未准备'}, status=status.HTTP_400_BAD_REQUEST)

        room.status = 'playing'
        room.save()

        return Response(RoomSerializer(room).data)

    @action(detail=False, methods=['get'])
    def public(self, request):
        rooms = Room.objects.filter(is_public=True, status='waiting')
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_rooms(self, request):
        rooms = Room.objects.filter(players__user=request.user)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

import uuid
from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    """游戏房间"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='房间名称')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms', verbose_name='创建者')
    seed = models.CharField(max_length=64, blank=True, verbose_name='游戏种子')
    max_players = models.IntegerField(default=6, verbose_name='最大玩家数')
    is_public = models.BooleanField(default=False, verbose_name='公开房间')
    status = models.CharField(
        max_length=20,
        choices=[
            ('waiting', '等待中'),
            ('playing', '游戏中'),
            ('finished', '已结束'),
        ],
        default='waiting',
        verbose_name='状态'
    )
    current_round = models.IntegerField(default=1, verbose_name='当前回合')
    total_rounds = models.IntegerField(default=10, verbose_name='总回合数')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '游戏房间'
        verbose_name_plural = '游戏房间'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    @property
    def player_count(self):
        return self.players.count()

    @property
    def is_full(self):
        return self.player_count >= self.max_players

    def can_start(self):
        """检查是否可以开始游戏"""
        return self.status == 'waiting' and self.player_count >= 2


class Player(models.Model):
    """房间中的玩家"""
    ROLE_CHOICES = [
        ('politician', '政客'),
        ('god', '上帝'),
        ('observer', '观察者'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='players', verbose_name='房间')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_players', verbose_name='用户')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='politician', verbose_name='角色')
    is_ready = models.BooleanField(default=False, verbose_name='已准备')
    score = models.IntegerField(default=0, verbose_name='得分')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '玩家'
        verbose_name_plural = '玩家'
        unique_together = ['room', 'user']
        ordering = ['joined_at']

    def __str__(self):
        return f"{self.user.username} - {self.room.name} ({self.get_role_display()})"

    def is_god(self):
        return self.role == 'god'

    def is_politician(self):
        return self.role == 'politician'

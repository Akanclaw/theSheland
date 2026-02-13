import random
import hashlib
from django.db import models
from django.contrib.auth.models import User


class MapRegion(models.Model):
    """地图区域"""
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='regions')
    name = models.CharField(max_length=100, verbose_name='区域名称')
    x = models.FloatField(default=0, verbose_name='X坐标')
    y = models.FloatField(default=0, verbose_name='Y坐标')
    population = models.IntegerField(default=1000, verbose_name='人口')
    economy = models.IntegerField(default=50, verbose_name='经济水平')
    stability = models.IntegerField(default=50, verbose_name='稳定度')
    education = models.IntegerField(default=50, verbose_name='教育水平')
    culture_type = models.CharField(
        max_length=20,
        choices=[
            ('industrial', '工业型'),
            ('agricultural', '农业型'),
            ('commercial', '商业型'),
            ('mixed', '混合型'),
        ],
        default='mixed',
        verbose_name='文化类型'
    )

    class Meta:
        verbose_name = '地图区域'
        verbose_name_plural = '地图区域'

    def __str__(self):
        return f"{self.name} ({self.culture_type})"


class CultureParameter(models.Model):
    """文化参数"""
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='culture_params')
    region = models.ForeignKey(MapRegion, on_delete=models.CASCADE, related_name='culture_params')
    name = models.CharField(max_length=50, verbose_name='参数名称')
    value = models.FloatField(default=0, verbose_name='数值')

    class Meta:
        verbose_name = '文化参数'
        verbose_name_plural = '文化参数'


class Candidate(models.Model):
    """候选人（政客玩家）"""
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='candidates')
    player = models.OneToOneField('rooms.Player', on_delete=models.CASCADE, related_name='candidate')
    name = models.CharField(max_length=100, verbose_name='候选人名称')
    party = models.CharField(max_length=50, blank=True, verbose_name='党派')
    funds = models.IntegerField(default=10000, verbose_name='资金')
    reputation = models.IntegerField(default=50, verbose_name='声望')
    policy_economy = models.IntegerField(default=50, verbose_name='经济政策立场')
    policy_social = models.IntegerField(default=50, verbose_name='社会政策立场')
    policy_security = models.IntegerField(default=50, verbose_name='安全政策立场')

    class Meta:
        verbose_name = '候选人'
        verbose_name_plural = '候选人'

    def __str__(self):
        return f"{self.name} - {self.room.name}"


class GodPlayer(models.Model):
    """上帝玩家"""
    room = models.OneToOneField('rooms.Room', on_delete=models.CASCADE, related_name='god')
    player = models.OneToOneField('rooms.Player', on_delete=models.CASCADE, related_name='god_status')
    divine_power = models.IntegerField(default=100, verbose_name='神力值')
    interventions_used = models.IntegerField(default=0, verbose_name='已用干预次数')

    class Meta:
        verbose_name = '上帝玩家'
        verbose_name_plural = '上帝玩家'


class Round(models.Model):
    """游戏回合"""
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='rounds')
    round_number = models.IntegerField(verbose_name='回合数')
    phase = models.CharField(
        max_length=20,
        choices=[
            ('campaign', '竞选阶段'),
            ('god_intervention', '上帝干预'),
            ('voting', '投票阶段'),
            ('results', '结果公布'),
        ],
        default='campaign',
        verbose_name='阶段'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = '游戏回合'
        verbose_name_plural = '游戏回合'
        unique_together = ['room', 'round_number']


class CampaignAction(models.Model):
    """竞选行动"""
    ACTION_TYPES = [
        ('rally', '集会'),
        ('advertise', '广告'),
        ('promise', '政策承诺'),
        ('attack', '攻击对手'),
        ('visit', '地区访问'),
    ]

    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='actions')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='actions')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    target_region = models.ForeignKey(MapRegion, on_delete=models.CASCADE, related_name='campaign_actions', null=True, blank=True)
    target_candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='attacked_by', null=True, blank=True)
    cost = models.IntegerField(default=0)
    effectiveness = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '竞选行动'
        verbose_name_plural = '竞选行动'


class GodIntervention(models.Model):
    """上帝干预"""
    INTERVENTION_TYPES = [
        ('modify_map', '修改地图'),
        ('influence_culture', '影响文化'),
        ('swing_votes', '摇摆选票'),
        ('trigger_event', '触发事件'),
    ]

    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='interventions')
    god = models.ForeignKey(GodPlayer, on_delete=models.CASCADE, related_name='interventions')
    intervention_type = models.CharField(max_length=20, choices=INTERVENTION_TYPES)
    target_region = models.ForeignKey(MapRegion, on_delete=models.CASCADE, null=True, blank=True)
    target_candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    power_cost = models.IntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '上帝干预'
        verbose_name_plural = '上帝干预'


class VoteResult(models.Model):
    """投票结果"""
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='vote_results')
    region = models.ForeignKey(MapRegion, on_delete=models.CASCADE, related_name='vote_results')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='vote_results')
    votes = models.IntegerField(default=0)
    percentage = models.FloatField(default=0)

    class Meta:
        verbose_name = '投票结果'
        verbose_name_plural = '投票结果'
        unique_together = ['round', 'region', 'candidate']


class ElectionResult(models.Model):
    """选举最终结果"""
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='final_results')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='final_result')
    total_votes = models.IntegerField(default=0)
    vote_percentage = models.FloatField(default=0)
    is_winner = models.BooleanField(default=False)

    class Meta:
        verbose_name = '选举最终结果'
        verbose_name_plural = '选举最终结果'

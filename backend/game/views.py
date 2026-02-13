import random
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import MapRegion, CultureParameter, Candidate, GodPlayer, Round, CampaignAction, GodIntervention
from .serializers import (MapRegionSerializer, CultureParameterSerializer, CandidateSerializer,
                         GodPlayerSerializer, CampaignActionSerializer, GodInterventionSerializer, RoundSerializer)


class MapRegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MapRegion.objects.all()
    serializer_class = MapRegionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def generate(self, request):
        """根据种子生成地图"""
        import random
        import string

        room_id = request.query_params.get('room_id')
        seed = request.query_params.get('seed', ''.join(random.choices(string.ascii_uppercase + string.digits, k=16)))

        rng = random.Random(seed)
        regions = []

        # 生成5-10个区域
        region_count = rng.randint(5, 10)
        culture_types = ['industrial', 'agricultural', 'commercial', 'mixed']

        for i in range(region_count):
            region = {
                'name': f'区域{i+1}',
                'x': rng.uniform(0, 100),
                'y': rng.uniform(0, 100),
                'population': rng.randint(1000, 1000000),
                'economy': rng.randint(20, 100),
                'stability': rng.randint(20, 100),
                'education': rng.randint(20, 100),
                'culture_type': rng.choice(culture_types),
            }
            regions.append(region)

        return Response({
            'seed': seed,
            'regions': regions,
            'region_count': region_count
        })


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]


class GodPlayerViewSet(viewsets.ModelViewSet):
    queryset = GodPlayer.objects.all()
    serializer_class = GodPlayerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def intervene(self, request, pk=None):
        """上帝干预操作"""
        god = self.get_object()

        if god.divine_power <= 0:
            return Response({'error': '神力不足'}, status=status.HTTP_400_BAD_REQUEST)

        intervention_type = request.data.get('intervention_type')
        description = request.data.get('description', '')
        power_cost = request.data.get('power_cost', 20)

        if god.divine_power < power_cost:
            return Response({'error': '神力不足'}, status=status.HTTP_400_BAD_REQUEST)

        god.divine_power -= power_cost
        god.interventions_used += 1
        god.save()

        # 记录干预
        intervention = GodIntervention.objects.create(
            god=god,
            round_id=request.data.get('round_id'),
            intervention_type=intervention_type,
            description=description,
            power_cost=power_cost
        )

        return Response(GodInterventionSerializer(intervention).data)


class CampaignActionViewSet(viewsets.ModelViewSet):
    queryset = CampaignAction.objects.all()
    serializer_class = CampaignActionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        action = serializer.save()
        # 扣除费用
        candidate = action.candidate
        if candidate.funds >= action.cost:
            candidate.funds -= action.cost
            candidate.save()
        return action


class RoundViewSet(viewsets.ModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def advance_phase(self, request, pk=None):
        """推进回合阶段"""
        round_obj = self.get_object()

        phase_order = ['campaign', 'god_intervention', 'voting', 'results']
        current_index = phase_order.index(round_obj.phase)

        if current_index < len(phase_order) - 1:
            round_obj.phase = phase_order[current_index + 1]
        else:
            # 进入下一回合
            round_obj.phase = 'results'
            round_obj.ended_at = timezone.now()
            round_obj.save()

            # 创建新回合
            new_round = Round.objects.create(
                room=round_obj.room,
                round_number=round_obj.round_number + 1,
                phase='campaign'
            )
            return Response(RoundSerializer(new_round).data)

        round_obj.save()
        return Response(RoundSerializer(round_obj).data)

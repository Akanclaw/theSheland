from rest_framework import serializers
from .models import (MapRegion, CultureParameter, Candidate, GodPlayer, Round,
                    CampaignAction, GodIntervention, VoteResult, ElectionResult)


class MapRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapRegion
        fields = ['id', 'name', 'x', 'y', 'population', 'economy', 'stability', 
                  'education', 'culture_type']


class CultureParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CultureParameter
        fields = ['id', 'region', 'name', 'value']


class CandidateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='player.user.username', read_only=True)

    class Meta:
        model = Candidate
        fields = ['id', 'player', 'username', 'name', 'party', 'funds', 
                  'reputation', 'policy_economy', 'policy_social', 'policy_security']


class GodPlayerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='player.user.username', read_only=True)

    class Meta:
        model = GodPlayer
        fields = ['id', 'player', 'username', 'divine_power', 'interventions_used']


class CampaignActionSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.name', read_only=True)
    target_region_name = serializers.CharField(source='target_region.name', read_only=True)

    class Meta:
        model = CampaignAction
        fields = ['id', 'candidate', 'candidate_name', 'action_type', 'target_region',
                  'target_region_name', 'target_candidate', 'cost', 'effectiveness', 'created_at']


class GodInterventionSerializer(serializers.ModelSerializer):
    god_username = serializers.CharField(source='god.player.user.username', read_only=True)

    class Meta:
        model = GodIntervention
        fields = ['id', 'god', 'god_username', 'intervention_type', 'target_region',
                  'target_candidate', 'description', 'power_cost', 'created_at']


class VoteResultSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.name', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)

    class Meta:
        model = VoteResult
        fields = ['id', 'round', 'region', 'region_name', 'candidate', 'candidate_name', 
                  'votes', 'percentage']


class ElectionResultSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.name', read_only=True)
    party = serializers.CharField(source='candidate.party', read_only=True)

    class Meta:
        model = ElectionResult
        fields = ['id', 'candidate', 'candidate_name', 'party', 'total_votes', 
                  'vote_percentage', 'is_winner']


class RoundSerializer(serializers.ModelSerializer):
    actions = CampaignActionSerializer(many=True, read_only=True)
    interventions = GodInterventionSerializer(many=True, read_only=True)
    vote_results = VoteResultSerializer(many=True, read_only=True)

    class Meta:
        model = Round
        fields = ['id', 'round_number', 'phase', 'started_at', 'ended_at',
                  'actions', 'interventions', 'vote_results']

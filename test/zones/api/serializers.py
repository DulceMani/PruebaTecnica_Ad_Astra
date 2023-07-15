from rest_framework import serializers

from zones.models import Zone, Distribution


class DistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        fields = ['id', 'percentage']


class ZoneSerializer(serializers.ModelSerializer):
    distributions = DistributionSerializer(many=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S") # se formatea la fecha para mostrarla al cliente
    class Meta:
        model = Zone
        fields = ['id', 'name', 'distributions','updated_at']
        read_only_fields = ['updated_at']

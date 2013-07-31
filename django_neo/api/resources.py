import ast
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from django_neo.models import Block, Segment
from django_neo.models import RecordingChannelGroup, RecordingChannel, Unit
from django_neo.models import AnalogSignal, IrregularlySampledSignal, SpikeTrain, Event
from django_neo.models import EventType
from tastypie.serializers import Serializer
from tastypie.constants import ALL, ALL_WITH_RELATIONS

class BlockResource(ModelResource):
    segments = fields.ToManyField('django_neo.api.resources.SegmentResource','Segments',
                                  null=True,blank=True,full=True)
    recording_channel_groups = fields.ToManyField('django_neo.api.resources.RecordingChannelGroupResource',
                                                  'recording_channel_groups',
                                                  null=True,blank=True,full=True)

    class Meta():
        queryset = Block.objects.all()
        resource_name = 'block'
        filtering = {
            'name': ALL,
            'description': ALL,
            'file_origin': ALL,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class SegmentResource(ModelResource):
    block = fields.ToOneField(BlockResource,'block',
                              null=True,blank=True)
    analogsignals = fields.ToManyField('django_neo.api.resources.AnalogSignalResource','analogsignals',
                                        null=True,blank=True)
    irregularlysampledsignals = fields.ToManyField('django_neo.api.resources.IrregularlySampledSignalResource',
                                                     'irregularlysampledsignals',
                                                     null=True,blank=True)
    spiketrains = fields.ToManyField('django_neo.api.resources.SpikeTrainResource',
                                      'spiketrains',
                                      null=True,blank=True)
    events = fields.ToManyField('django_neo.api.resources.EventResource',
                                'events',
                                null=True,blank=True)

    class Meta:
        queryset = Segment.objects.all()
        resource_name = 'segment'
        filtering = {
            'name': ALL,
            'description': ALL,
            'file_origin': ALL,
            'block': ALL_WITH_RELATIONS,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class RecordingChannelGroupResource(ModelResource):
    recording_channels = fields.ToManyField('django_neo.api.resources.RecordingChannelResource',
                                            'recording_channels',
                                            null=True,blank=True,full=True)
    units = fields.ToManyField('django_neo.api.resources.UnitResource',
                               'units',
                               null=True,blank=True)

    class Meta:
        queryset = RecordingChannelGroup.objects.all()
        resource_name = 'recording_channel_group'
        filtering = {
            'name': ALL,
            'description': ALL,
            'file_origin': ALL,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class RecordingChannelResource(ModelResource):
    analog_signals = fields.ToManyField('django_neo.api.resources.AnalogSignalResource',
                                        'analog_signals',
                                        null=True,blank=True)
    recording_channel_groups = fields.ToManyField('django_neo.api.resources.RecordingChannelGroupResource',
                                                  'recording_channel_groups',
                                                  null=True,blank=True)
    class Meta:
        queryset = RecordingChannel.objects.all()
        resource_name = 'recording_channel'
        filtering = {
            'name': ALL,
            'description': ALL,
            'file_origin': ALL,
            'block': ALL_WITH_RELATIONS,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class UnitResource(ModelResource):
    recording_channel_group = fields.ToOneField('django_neo.api.resources.RecordingChannelGroupResource','recording_channel_groups')
    spike_trains = fields.ToManyField('django_neo.api.resources.SpikeTrainResource','spike_trains')

    class Meta:
        queryset = Unit.objects.all()
        resource_name = 'unit'
        filtering = {
            'name': ALL,
            'description': ALL,
            'file_origin': ALL,
            'spike_trains': ALL_WITH_RELATIONS,
            'recording_channel_group': ALL_WITH_RELATIONS,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class AnalogSignalResource(ModelResource):
    segment = fields.ToOneField('django_neo.api.resources.SegmentResource','segments')
    recording_channel = fields.ToOneField('django_neo.api.resources.RecordingChannelResource','recording_channels')

    class Meta:
        queryset = AnalogSignal.objects.all()
        resource_name = 'analog_signal'
        filtering = {
            'name': ALL,
            'description': ALL,
            'file_origin': ALL,
            'segment': ALL_WITH_RELATIONS,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class IrregularlySampledSignalResource(ModelResource):
    segment = fields.ToOneField('django_neo.api.resources.SegmentResource','segments')

    class Meta:
        queryset = IrregularlySampledSignal.objects.all()
        resource_name = 'irregularly_sampled_signal'
        filtering = {
            'name': ALL,
            'description': ALL,
            'file_origin': ALL,
            'segment': ALL_WITH_RELATIONS,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class SpikeTrainResource(ModelResource):
    segment = fields.ToOneField('django_neo.api.resources.SegmentResource','segment')
    unit = fields.ToOneField('django_neo.api.resources.UnitResource','units',
                             null=True,blank=True)

    class Meta:
        queryset = SpikeTrain.objects.all()
        resource_name = 'spike_train'
        filtering = {
            'name': ALL,
            'description': ALL,
            'file_origin': ALL,
            'segment': ALL_WITH_RELATIONS,
            'unit': ALL_WITH_RELATIONS
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

    def dehydrate_times(self,bundle):
        return ast.literal_eval(bundle.data['times'])
        

class EventTypeResource(ModelResource):
    events = fields.ToManyField('django_neo.api.resources.EventResource','events')

    class Meta:
        queryset = EventType.objects.all()
        resource_name = 'event_type'
        filtering = {
            'name': ALL,
            'description': ALL,
            'file_origin': ALL,
            'segment': ALL_WITH_RELATIONS,
            'events': ALL_WITH_RELATIONS,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class EventResource(ModelResource):
    segment = fields.ToOneField('django_neo.api.resources.SegmentResource','segments')
    event_type = fields.ToOneField('django_neo.api.resources.EventTypeResource','event_types')

    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'
        filtering = {
            'name': ALL,
            'description': ALL,
            'file_origin': ALL,
            'segment': ALL_WITH_RELATIONS,
            'event_type': ALL,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

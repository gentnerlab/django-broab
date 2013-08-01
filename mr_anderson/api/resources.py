import ast
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from mr_anderson.models import Block, Segment
from mr_anderson.models import RecordingChannelGroup, RecordingChannel, Unit
from mr_anderson.models import AnalogSignal, IrregularlySampledSignal, SpikeTrain, Event
from mr_anderson.models import EventType
from tastypie.serializers import Serializer
from tastypie.constants import ALL, ALL_WITH_RELATIONS

class BaseMeta(object):
    filtering = {
        'name': ALL,
        'description': ALL,
        'file_origin': ALL,
        'annotations': ALL,
    }
    authentication = BasicAuthentication()
    authorization = DjangoAuthorization()

class LookupMeta(object):
    filtering = {
        'name': ALL,
        'description': ALL,
    }
    authentication = BasicAuthentication()
    authorization = DjangoAuthorization()

class BlockResource(ModelResource):
    segments = fields.ToManyField('mr_anderson.api.resources.SegmentResource','Segments',
                                  null=True,blank=True,full=True)
    recording_channel_groups = fields.ToManyField('mr_anderson.api.resources.RecordingChannelGroupResource',
                                                  'recording_channel_groups',
                                                  null=True,blank=True,full=True)

    class Meta(BaseMeta):
        queryset = Block.objects.all()
        resource_name = 'block'
        filtering.update({
            'segments': ALL_WITH_RELATIONS,
            'recording_channel_groups': ALL_WITH_RELATIONS,
        })


class SegmentResource(ModelResource):
    block = fields.ToOneField(BlockResource,'block',
                              null=True,blank=True)
    analogsignals = fields.ToManyField('mr_anderson.api.resources.AnalogSignalResource','analogsignals',
                                        null=True,blank=True)
    irregularlysampledsignals = fields.ToManyField('mr_anderson.api.resources.IrregularlySampledSignalResource',
                                                     'irregularlysampledsignals',
                                                     null=True,blank=True)
    spiketrains = fields.ToManyField('mr_anderson.api.resources.SpikeTrainResource',
                                      'spiketrains',
                                      null=True,blank=True)
    events = fields.ToManyField('mr_anderson.api.resources.EventResource',
                                'events',
                                null=True,blank=True)

    class Meta(BaseMeta):
        queryset = Segment.objects.all()
        resource_name = 'segment'
        filtering.update({
            'block': ALL_WITH_RELATIONS,
            'analogsignals': ALL_WITH_RELATIONS,
            'irregularlysampledsignals': ALL_WITH_RELATIONS,
            'spiketrains': ALL_WITH_RELATIONS,
            'events': ALL_WITH_RELATIONS,
        })

class RecordingChannelGroupResource(ModelResource):
    recording_channels = fields.ToManyField('mr_anderson.api.resources.RecordingChannelResource',
                                            'recording_channels',
                                            null=True,blank=True,full=True)
    units = fields.ToManyField('mr_anderson.api.resources.UnitResource',
                               'units',
                               null=True,blank=True)

    class Meta(BaseMeta):
        queryset = RecordingChannelGroup.objects.all()
        resource_name = 'recording_channel_group'
        filtering.update({
            'recording_channels': ALL_WITH_RELATIONS,
            'units': ALL_WITH_RELATIONS,
        })

class RecordingChannelResource(ModelResource):
    analog_signals = fields.ToManyField('mr_anderson.api.resources.AnalogSignalResource',
                                        'analog_signals',
                                        null=True,blank=True)
    recording_channel_groups = fields.ToManyField('mr_anderson.api.resources.RecordingChannelGroupResource',
                                                  'recording_channel_groups',
                                                  null=True,blank=True)
    class Meta(BaseMeta):
        queryset = RecordingChannel.objects.all()
        resource_name = 'recording_channel'
        filtering.update({
            'analog_signals': ALL_WITH_RELATIONS,
            'recording_channel_groups': ALL_WITH_RELATIONS,
        })

class UnitResource(ModelResource):
    recording_channel_group = fields.ToOneField('mr_anderson.api.resources.RecordingChannelGroupResource','recording_channel_groups')
    spike_trains = fields.ToManyField('mr_anderson.api.resources.SpikeTrainResource','spike_trains')

    class Meta(BaseMeta):
        queryset = Unit.objects.all()
        resource_name = 'unit'
        filtering.update({
            'spike_trains': ALL_WITH_RELATIONS,
            'recording_channel_group': ALL_WITH_RELATIONS,
        })

class AnalogSignalResource(ModelResource):
    segment = fields.ToOneField('mr_anderson.api.resources.SegmentResource','segments')
    recording_channel = fields.ToOneField('mr_anderson.api.resources.RecordingChannelResource','recording_channels')

    class Meta(BaseMeta):
        queryset = AnalogSignal.objects.all()
        resource_name = 'analog_signal'
        filtering.update({
            'segment': ALL_WITH_RELATIONS,
            'recording_channel': ALL_WITH_RELATIONS,
        })

class IrregularlySampledSignalResource(ModelResource):
    segment = fields.ToOneField('mr_anderson.api.resources.SegmentResource','segments')

    class Meta(BaseMeta):
        queryset = IrregularlySampledSignal.objects.all()
        resource_name = 'irregularly_sampled_signal'
        filtering.update({
            'segment': ALL_WITH_RELATIONS,
        })

class SpikeTrainResource(ModelResource):
    segment = fields.ToOneField('mr_anderson.api.resources.SegmentResource','segment')
    unit = fields.ToOneField('mr_anderson.api.resources.UnitResource','units',
                             null=True,blank=True)

    class Meta(BaseMeta):
        queryset = SpikeTrain.objects.all()
        resource_name = 'spike_train'
        filtering.update({
            'segment': ALL_WITH_RELATIONS,
            'unit': ALL_WITH_RELATIONS
        })

    def dehydrate_times(self,bundle):
        return ast.literal_eval(bundle.data['times'])
        

class EventTypeResource(ModelResource):
    events = fields.ToManyField('mr_anderson.api.resources.EventResource','events')

    class Meta(LookupMeta):
        queryset = EventType.objects.all()
        resource_name = 'event_type'
        filtering.update({
            'events': ALL_WITH_RELATIONS,
        })

class EventResource(ModelResource):
    segment = fields.ToOneField('mr_anderson.api.resources.SegmentResource','segments')
    event_type = fields.ToOneField('mr_anderson.api.resources.EventTypeResource','event_types')

    class Meta(BaseMeta):
        queryset = Event.objects.all()
        resource_name = 'event'
        filtering.update({
            'segment': ALL_WITH_RELATIONS,
            'event_type': ALL,
        })

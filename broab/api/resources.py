import ast
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from broab.models import Block, Segment
from broab.models import RecordingChannelGroup, RecordingChannel, Unit
from broab.models import AnalogSignal, IrregularlySampledSignal, SpikeTrain, SpikeTrainFull, Event
from broab.models import EventLabel
from tastypie.serializers import Serializer
from tastypie.constants import ALL, ALL_WITH_RELATIONS


LOOKUP_FILTERING = {
    'id': ALL,
    'name': ALL,
    'description': ALL,
    }

BROAB_FILTERING = {
    'id': ALL,
    'name': ALL,
    'description': ALL,
    'file_origin': ALL,
    'annotations': ALL,
    'created': ALL,
    'modified': ALL,
    }

CONTAINER_FILTERING = {
    'file_datetime': ALL,
    'rec_datetime': ALL,
    'index': ALL,
}

DATA_FILTERING = {
    'segment': ALL_WITH_RELATIONS,
}

class BroabResource(ModelResource):

    annotations = fields.DictField(attribute='annotations')
    class Meta():
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class BlockResource(BroabResource):
    segments = fields.ToManyField(
        'broab.api.resources.SegmentResource',
        'segments',
        null=True,
        blank=True
        )
    recording_channel_groups = fields.ToManyField(
        'broab.api.resources.RecordingChannelGroupResource',
        'recording_channel_groups',
        null=True,
        blank=True
        )

    class Meta(BroabResource.Meta):
        queryset = Block.objects.all()
        resource_name = 'block'
        filtering = BROAB_FILTERING
        filtering.update(CONTAINER_FILTERING)
        filtering.update({
            'segments': ALL_WITH_RELATIONS,
            'recording_channel_groups': ALL_WITH_RELATIONS,
        })
        ordering = filtering.keys()


class SegmentResource(BroabResource):
    block = fields.ToOneField(
        BlockResource,
        'block',
        null=True,
        blank=True
        )
    analogsignals = fields.ToManyField(
        'broab.api.resources.AnalogSignalResource',
        'analogsignals',
        null=True,
        blank=True
        )
    irregularlysampledsignals = fields.ToManyField(
        'broab.api.resources.IrregularlySampledSignalResource',
        'irregularlysampledsignals',
        null=True,
        blank=True
        )
    spiketrains = fields.ToManyField(
        'broab.api.resources.SpikeTrainResource',
        'spiketrains',
        null=True,
        blank=True
        )
    events = fields.ToManyField(
        'broab.api.resources.EventResource',
        'events',
        null=True,
        blank=True
        )

    class Meta(BroabResource.Meta):
        queryset = Segment.objects.all()
        resource_name = 'segment'
        filtering = BROAB_FILTERING
        filtering.update(CONTAINER_FILTERING)
        filtering.update({
            'block': ALL_WITH_RELATIONS,
            'analogsignals': ALL_WITH_RELATIONS,
            'irregularlysampledsignals': ALL_WITH_RELATIONS,
            'spiketrains': ALL_WITH_RELATIONS,
            'events': ALL_WITH_RELATIONS,
        })
        ordering = filtering.keys()

class RecordingChannelGroupResource(BroabResource):
    recording_channels = fields.ToManyField(
        'broab.api.resources.RecordingChannelResource',
        'recording_channels',
        null=True,
        blank=True
        )
    units = fields.ToManyField(
        'broab.api.resources.UnitResource',
        'units',
        null=True,
        blank=True
        )

    class Meta(BroabResource.Meta):
        queryset = RecordingChannelGroup.objects.all()
        resource_name = 'recording_channel_group'
        filtering = BROAB_FILTERING
        filtering.update({
            'block': ALL_WITH_RELATIONS,
            'recording_channels': ALL_WITH_RELATIONS,
            'units': ALL_WITH_RELATIONS,
        })
        ordering = filtering.keys()

class RecordingChannelResource(BroabResource):
    analog_signals = fields.ToManyField(
        'broab.api.resources.AnalogSignalResource',
        'analog_signals',
        null=True,
        blank=True
        )
    recording_channel_groups = fields.ToManyField(
        'broab.api.resources.RecordingChannelGroupResource',
        'recording_channel_groups',
        null=True,
        blank=True
        )
    class Meta(BroabResource.Meta):
        queryset = RecordingChannel.objects.all()
        resource_name = 'recording_channel'
        filtering = BROAB_FILTERING
        filtering.update({
            'index': ALL,
            'x_coord': ALL,
            'y_coord': ALL,
            'z_coord': ALL,
            'analog_signals': ALL_WITH_RELATIONS,
            'recording_channel_groups': ALL_WITH_RELATIONS,
        })
        ordering = filtering.keys()

class UnitResource(BroabResource):
    recording_channel_group = fields.ToOneField(
        'broab.api.resources.RecordingChannelGroupResource',
        'recording_channel_groups',
        null=True,
        blank=True
        )
    spike_trains = fields.ToManyField(
        'broab.api.resources.SpikeTrainResource',
        'spike_trains',
        null=True,
        blank=True
        )

    class Meta(BroabResource.Meta):
        queryset = Unit.objects.all()
        resource_name = 'unit'
        filtering = BROAB_FILTERING
        filtering.update({
            'spike_trains': ALL_WITH_RELATIONS,
            'recording_channel_group': ALL_WITH_RELATIONS,
        })
        ordering = filtering.keys()

class AnalogSignalResource(BroabResource):
    segment = fields.ToOneField(
        'broab.api.resources.SegmentResource',
        'segment'
        )
    recording_channel = fields.ToOneField(
        'broab.api.resources.RecordingChannelResource',
        'recording_channels',
        null=True,
        blank=True
        )
    signal = fields.ListField(attribute='signal')

    class Meta(BroabResource.Meta):
        queryset = AnalogSignal.objects.all()
        resource_name = 'analog_signal'
        filtering = BROAB_FILTERING
        filtering.update(DATA_FILTERING)
        filtering.update({
            't_start': ALL,
            't_units': ALL,
            'signal': ALL,
            'signal_units': ALL,
            'sampling_rate': ALL,
            'recording_channel': ALL_WITH_RELATIONS,
        })
        ordering = filtering.keys()

class IrregularlySampledSignalResource(BroabResource):
    segment = fields.ToOneField(
        'broab.api.resources.SegmentResource',
        'segment'
        )

    class Meta(BroabResource.Meta):
        queryset = IrregularlySampledSignal.objects.all()
        resource_name = 'irregularly_sampled_signal'
        filtering = BROAB_FILTERING
        filtering.update(DATA_FILTERING)
        filtering.update({
            'times': ALL,
            't_units': ALL,
            'signal': ALL,
            'signal_units': ALL,
            'recording_channel': ALL_WITH_RELATIONS,
        })
        ordering = filtering.keys()

class SpikeTrainResource(BroabResource):
    segment = fields.ToOneField(
        'broab.api.resources.SegmentResource',
        'segment'
        )
    unit = fields.ToOneField(
        'broab.api.resources.UnitResource',
        'unit',
        null=True,
        blank=True
        )
    times = fields.ListField(attribute='times')
    full = fields.ToOneField(
        'broab.api.resources.SpikeTrainFullResource',
        'spiketrainfull',
        null=True,
        blank=True
        )

    class Meta(BroabResource.Meta):
        queryset = SpikeTrain.objects.all()
        resource_name = 'spiketrain'
        filtering = BROAB_FILTERING
        filtering.update(DATA_FILTERING)
        filtering.update({
            'times': ALL,
            't_start': ALL,
            't_stop': ALL,
            't_units': ALL,
            'unit': ALL_WITH_RELATIONS,
        })
        ordering = filtering.keys()


class SpikeTrainFullResource(SpikeTrainResource):

    waveforms = fields.ListField(attribute='waveforms')
    concise = fields.ToOneField(
        'broab.api.resources.SpikeTrainResource',
        'spiketrain_ptr'
        )

    class Meta(BroabResource.Meta):
        queryset = SpikeTrainFull.objects.all()
        resource_name = 'spiketrainfull'
        filtering = BROAB_FILTERING
        filtering.update(DATA_FILTERING)
        filtering.update({
            'waveforms': ALL,
            'waveform_units': ALL,
            'sampling_rate': ALL,
            'left_sweep': ALL,
            'sort': ALL,
        })
        ordering = filtering.keys()
        
class EventLabelResource(BroabResource):
    # events = fields.ToManyField(
    #     'broab.api.resources.EventResource',
    #     'event_set'
    #     )

    class Meta(BroabResource.Meta):
        queryset = EventLabel.objects.all()
        resource_name = 'label'
        filtering = LOOKUP_FILTERING
        filtering.update({
            'events': ALL_WITH_RELATIONS,
        })
        ordering = filtering.keys()

class EventResource(BroabResource):
    segment = fields.ToOneField(
        'broab.api.resources.SegmentResource',
        'segment'
        )
    label = fields.ToOneField(
        'broab.api.resources.EventLabelResource',
        'label',
        full=True
        )

    class Meta(BroabResource.Meta):
        queryset = Event.objects.all()
        resource_name = 'event'
        filtering = BROAB_FILTERING
        filtering.update(DATA_FILTERING)
        filtering.update({
            'time': ALL,
            'duration': ALL,
            'label': ALL_WITH_RELATIONS,
        })
        ordering = filtering.keys()
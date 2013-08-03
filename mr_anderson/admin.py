from django.contrib import admin
from django import forms
from mr_anderson.models import Block, Segment
from mr_anderson.models import RecordingChannelGroup, RecordingChannel, Unit
from mr_anderson.models import AnalogSignal, SpikeTrain, Event
from mr_anderson.models import EventType
from djorm_pgarray.fields import ArrayFormField

class SegmentInline(admin.StackedInline):
    model = Segment
    max_num = 10
    extra = 0

class RecordingChannelGroupInline(admin.StackedInline):
    model = RecordingChannelGroup
    max_num = 10
    extra = 0

class BlockAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [SegmentInline,
               RecordingChannelGroupInline,
               ]
admin.site.register(Block,BlockAdmin)

class EventInline(admin.TabularInline):
    model = Event
    extra = 0

class SpikeTrainInline(admin.TabularInline):
    model = SpikeTrain
    extra = 0

class AnalogSignalInline(admin.TabularInline):
    model = AnalogSignal
    extra = 0

class SegmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [EventInline,
               SpikeTrainInline,
               AnalogSignalInline,
               ]
admin.site.register(Segment,SegmentAdmin)

admin.site.register(RecordingChannelGroup)

admin.site.register(RecordingChannel)

admin.site.register(Unit)

admin.site.register(AnalogSignal)

class SpikeTrainAdmin(admin.ModelAdmin):
    fields = ('t_start','t_stop')
    readonly_fields = ('n_spikes',)

    def n_spikes(self,instance):
        return str(len(instance.times))

admin.site.register(SpikeTrain,SpikeTrainAdmin)

admin.site.register(Event)

admin.site.register(EventType)


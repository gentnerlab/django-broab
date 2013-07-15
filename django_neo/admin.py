from django.contrib import admin
from django_neo.models import Block, Segment
from django_neo.models import RecordingChannelGroup, RecordingChannel, Unit
from django_neo.models import AnalogSignal, SpikeTrain, Event
from django_neo.models import EventType
from django_neo.models import Annotation
from genericadmin.admin import GenericAdminModelAdmin, GenericStackedInline

class AnnotationInline(GenericStackedInline):
    model = Annotation
    extra = 0

class SegmentInline(admin.StackedInline):
    model = Segment
    max_num = 10
    extra = 0

class RecordingChannelGroupInline(admin.StackedInline):
    model = RecordingChannelGroup
    max_num = 10
    extra = 0

class BlockAdmin(GenericAdminModelAdmin):
    list_display = ('name', 'description')
    inlines = [SegmentInline,
               RecordingChannelGroupInline,
               AnnotationInline,
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
               AnnotationInline,
               ]
admin.site.register(Segment,SegmentAdmin)

admin.site.register(RecordingChannelGroup)

admin.site.register(RecordingChannel)

admin.site.register(Unit)

admin.site.register(AnalogSignal)

admin.site.register(SpikeTrain)

admin.site.register(Event)

admin.site.register(EventType)


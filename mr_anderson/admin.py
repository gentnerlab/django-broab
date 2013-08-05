from django.contrib import admin
from django import forms
from mr_anderson.models import Block, Segment
from mr_anderson.models import RecordingChannelGroup, RecordingChannel, Unit
from mr_anderson.models import AnalogSignal, SpikeTrain, Event
from mr_anderson.models import EventType
from djorm_pgarray.fields import ArrayFormField

SEARCH_FIELDS = ['name','description','annotations']

# inlines
class EventInline(admin.TabularInline):
    model = Event
    extra = 0

class SpikeTrainInline(admin.TabularInline):
    model = SpikeTrain
    extra = 0

class AnalogSignalInline(admin.TabularInline):
    model = AnalogSignal
    extra = 0

class SegmentInline(admin.StackedInline):
    model = Segment
    max_num = 10
    extra = 0

class RecordingChannelGroupInline(admin.StackedInline):
    model = RecordingChannelGroup
    max_num = 10
    extra = 0

# admin forms
class BlockAdmin(admin.ModelAdmin):
    list_display = ('name','index','rec_datetime')
    fieldsets = (
        (None, {
            'fields': ('index', 'rec_datetime'),
         }),
        ('Meta', {
            'fields': ('name','description','annotations'),
         }),
        ('File information', {
            'fields': ('file_origin','file_datetime'),
         }),
        )
    inlines = [
        RecordingChannelGroupInline,
        ]
    search_fields = [
        'name',
        'description',
        'annotations',
        ]
    # readonly_fields = ('created','modified')
admin.site.register(Block,BlockAdmin)

class SegmentAdmin(admin.ModelAdmin):
    list_display = ('name','index','rec_datetime')
    fieldsets = (
        (None, {
            'fields': ('block','index', 'rec_datetime',),
         }),
        ('Meta', {
            'fields': ('name','description','annotations'),
         }),
        ('File information', {
            'fields': ('file_origin','file_datetime'),
         }),
        )
    inlines = [
        EventInline,
        # SpikeTrainInline,
        # AnalogSignalInline,
    ]
    search_fields = [
        'name',
        'description',
        'annotations',
        'file_origin',
        'block__name',
        'block__description',
        'block__annotations',
        'block__file_origin',
        ]
admin.site.register(Segment,SegmentAdmin)

class RecordingChannelGroupAdmin(admin.ModelAdmin):
    list_display = ('pk','name','block',)
    fieldsets = (
        (None, {
            'fields': ('block','recording_channels'),
         }),
        ('Meta', {
            'fields': ('name', 'description', 'annotations'),
         }),
        ('File information', {
            'fields': ('file_origin',),
         }),
        )
    filter_horizontal = ['recording_channels']
    search_fields = [
        'name',
        'description',
        'annotations',
        'file_origin',
        'block__name',
        'block__description',
        'block__annotations',
        'block__file_origin',
        ]
admin.site.register(RecordingChannelGroup,RecordingChannelGroupAdmin)

class RecordingChannelAdmin(admin.ModelAdmin):
    list_display = ('index','x_coord','y_coord','z_coord','coord_units')
    fieldsets = (
        (None, {
            'fields': ('index',('x_coord','y_coord','z_coord'),'coord_units'),
         }),
        ('Meta', {
            'fields': ('name', 'description', 'annotations'),
         }),
        ('File information', {
            'fields': ('file_origin',),
         }),
        )
    search_fields = [
        'name',
        'description',
        'annotations',
        'file_origin',
        ]
    # inlines = [AnalogSignalInline,]
admin.site.register(RecordingChannel,RecordingChannelAdmin)

class UnitAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('recording_channel_group',),
         }),
        ('Event info', {
            'fields': ('name', 'description', 'annotations'),
         }),
        ('File information', {
            'fields': ('file_origin',),
         }),
        )
    search_fields = [
        'name',
        'description',
        'annotations',
        'file_origin',
        'recording_channel_group__name',
        'recording_channel_group__description',
        'recording_channel_group__annotations',
        'recording_channel_group__file_origin',
        'recording_channel_group__block__name',
        'recording_channel_group__block__description',
        'recording_channel_group__block__annotations',
        'recording_channel_group__block__file_origin',
        ]
    # inlines = [SpikeTrainInline,]
admin.site.register(Unit,UnitAdmin)

class AnalogSignalAdmin(admin.ModelAdmin):

    list_display = ('t_start','segment','recording_channel')
    fieldsets = (
        (None, {
            'fields': (
                ('t_start','t_units'),
                ('signal','signal_units'),
                'sampling_rate',
                'recording_channel',
                ),
         }),
        ('Meta', {
            'fields': ('name', 'description', 'annotations'),
         }),
        ('File information', {
            'fields': ('file_origin',),
         }),
        )
    search_fields = [
        'name',
        'description',
        'annotations',
        'file_origin'
        'segment__name',
        'segment__description',
        'segment__annotations',
        'segment__file_origin',
        'segment__block__name',
        'segment__block__description',
        'segment__block__annotations',
        'segment__block__file_origin',
        ]

admin.site.register(AnalogSignal,AnalogSignalAdmin)

class SpikeTrainAdmin(admin.ModelAdmin):
    readonly_fields = ('n_spikes',)

    list_display = ('n_spikes','segment',)
    fieldsets = (
        (None, {
            'fields': ('n_spikes','segment',('t_start','t_stop')),
         }),
        ('Meta', {
            'fields': ('name', 'description', 'annotations'),
         }),
        ('File information', {
            'fields': ('file_origin',),
         }),
        )
    search_fields = [
        'name',
        'description',
        'annotations',
        'file_origin'
        'segment__name',
        'segment__description',
        'segment__annotations',
        'segment__file_origin',
        'segment__block__name',
        'segment__block__description',
        'segment__block__annotations',
        'segment__block__file_origin',
        ]

    def n_spikes(self,instance):
        return str(len(instance.times))

admin.site.register(SpikeTrain,SpikeTrainAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ('time','duration','label','segment')
    fieldsets = (
        (None, {
            'fields': (('label','segment'),('time','duration')),
         }),
        ('Meta', {
            'fields': ('name', 'description', 'annotations'),
         }),
        ('File information', {
            'fields': ('file_origin',),
         }),
        )
    search_fields = [
        'name',
        'description',
        'annotations',
        'file_origin'
        'segment__name',
        'segment__description',
        'segment__annotations',
        'segment__file_origin',
        'segment__block__name',
        'segment__block__description',
        'segment__block__annotations',
        'segment__block__file_origin',
        'label__name',
        'label__description',
        ]
admin.site.register(Event,EventAdmin)

admin.site.register(EventType)


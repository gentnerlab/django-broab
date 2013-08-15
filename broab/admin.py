from django.contrib import admin
from django import forms
from broab.models import Block, Segment
from broab.models import RecordingChannelGroup, RecordingChannel, Unit
from broab.models import AnalogSignal, SpikeTrain, Event
from broab.models import EventLabel
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
        ('History', {
            'fields': (('created','modified'),),
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
    readonly_fields = ('created','modified')
admin.site.register(Block,BlockAdmin)

class SegmentAdmin(admin.ModelAdmin):
    list_display = ('name','index','rec_datetime')
    list_filter = ('block','events__label')
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
        ('History', {
            'fields': (('created','modified'),),
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
        'events__name',
        'events__description',
        'events__annotations',
        'events__label__name',
        'events__label__description',
        ]
    readonly_fields = ('created','modified')
admin.site.register(Segment,SegmentAdmin)

class RecordingChannelGroupAdmin(admin.ModelAdmin):
    list_display = ('pk','name','block',)
    list_filter = ('block',)
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
        ('History', {
            'fields': (('created','modified'),),
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
    readonly_fields = ('created','modified')
admin.site.register(RecordingChannelGroup,RecordingChannelGroupAdmin)

class RecordingChannelAdmin(admin.ModelAdmin):
    list_display = ('index','x_coord','y_coord','z_coord','coord_units')
    list_filter = ('recording_channel_groups__block','recording_channel_groups',)
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
        ('History', {
            'fields': (('created','modified'),),
         }),
        )
    search_fields = [
        'name',
        'description',
        'annotations',
        'file_origin',
        ]
    readonly_fields = ('created','modified')
    # inlines = [AnalogSignalInline,]
admin.site.register(RecordingChannel,RecordingChannelAdmin)

class UnitAdmin(admin.ModelAdmin):
    list_filter = ('recording_channel_group__block',)
    list_display = ('recording_channel_group','name')
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
        ('History', {
            'fields': (('created','modified'),),
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
    readonly_fields = ('created','modified')
admin.site.register(Unit,UnitAdmin)

class AnalogSignalAdmin(admin.ModelAdmin):
    list_filter = (
        'segment__block',
        'recording_channel__recording_channel_groups',
        'recording_channel',
        'segment',
        )

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
        ('History', {
            'fields': (('created','modified'),),
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
    readonly_fields = ('created','modified')

admin.site.register(AnalogSignal,AnalogSignalAdmin)

class SpikeTrainAdmin(admin.ModelAdmin):
    list_filter = (
        'segment__block',
        'segment',
        'segment__events',
        'segment__events__name',
        'segment__events__label',
        'unit',
        )

    list_display = ('num_spikes','unit','segment',)
    fieldsets = (
        (None, {
            'fields': ('unit','segment',('t_start','t_stop'),'spike_times',),
         }),
        ('Meta', {
            'fields': ('name', 'description', 'annotations'),
         }),
        ('File information', {
            'fields': ('file_origin',),
         }),
        ('History', {
            'fields': (('created','modified'),),
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
    readonly_fields = ('spike_times','created','modified','num_spikes')

    def num_spikes(self,instance):
        return str(len(instance.times))

    def spike_times(self,instance):
        return ',\n'.join([("%f" % t) for t in instance.times]).join(['[\n','\n]'])

admin.site.register(SpikeTrain,SpikeTrainAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ('time','duration','label','segment')
    list_filter = (
        'segment__block',
        'segment',
        'label',
        )
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
        ('History', {
            'fields': (('created','modified'),),
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
    readonly_fields = ('created','modified')
admin.site.register(Event,EventAdmin)

admin.site.register(EventLabel)


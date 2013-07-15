from django.contrib import admin
from django_neo.models import Block, Segment
from django_neo.models import RecordingChannelGroup, RecordingChannel, Unit
from django_neo.models import AnalogSignal, SpikeTrain, Event,
from django_neo.models import EventType

admin.site.register(Block)

admin.site.register(Segment)

admin.site.register(RecordingChannelGroup)

admin.site.register(RecordingChannel)

admin.site.register(Unit)

admin.site.register(AnalogSignal)

admin.site.register(SpikeTrain)

admin.site.register(Event)

admin.site.register(EventType)
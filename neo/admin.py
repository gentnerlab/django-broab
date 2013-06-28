from django.contrib import admin
from neo.models import Block, Segment
from neo.models import RecordingChannelGroup, RecordingChannel, Unit
from neo.models import AnalogSignal, AnalogSignalArray, Spike, SpikeTrain, Event, Epoch
from neo.models import EventType

admin.site.register(Block)

admin.site.register(Segment)

admin.site.register(RecordingChannelGroup)

admin.site.register(RecordingChannel)

admin.site.register(Unit)

admin.site.register(AnalogSignal)

admin.site.register(AnalogSignalArray)

admin.site.register(Spike)

admin.site.register(SpikeTrain)

admin.site.register(Event)

admin.site.register(Epoch)

admin.site.register(EventType)
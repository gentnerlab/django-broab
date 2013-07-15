from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from djorm_pgarray.fields import ArrayField
from model_utils.managers import InheritanceManager


DISTANCE_CHOICES = (
    ('m', 'meters'),
    ('mm', 'millimeters'),
    ('cm', 'centiimeters'),
    ('um', 'micrometers'),
    ('nm', 'nanometers'),
    )
TIME_CHOICES = (
    ('h', 'hours'),
    ('m', 'minutes'),
    ('s', 'seconds'),
    ('ms', 'milliseconds'),
    ('us', 'microseconds'),
    )
RATE_CHOICES = (
    ('Hz', 'hertz'),
    ('kHz', 'kilohertz'),
    )
POTENTIAL_CHOICES = (
    ('V', 'volts'),
    ('mV', 'millivolts'),
    ('uV', 'microvolts'),
    )
CURRENT_CHOICES = (
    ('A', 'amps'),
    ('mA', 'milliamps'),
    ('uA', 'microamps'),
    ('nA', 'nanoamps'),
    )

class Attribute(models.Model):
    """key for annotation"""
    name = models.CharField(max_length=255,blank=False)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class Annotation(models.Model):
    """annotation class"""
    attribute = models.ForeignKey(Attribute)
    # value_boolean = models.NullBooleanField(null=True)
    # value_text = models.TextField(blank=True)
    # value_integer = models.IntegerField(null=True,blank=True)
    # value_float = models.FloatField(null=True,blank=True)
    # value_date = models.DateField(null=True,blank=True)
    # value_time = models.TimeField(null=True,blank=True)
    # value_datetime = models.DateTimeField(null=True,blank=True)
    # value_array_text = ArrayField(dbtype="text",dimension=1)
    # value_array_integer = ArrayField(dbtype="integer",dimension=1)
    # value_array_float = ArrayField(dbtype="float(53)",dimension=1)
    value = models.TextField(blank=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return "%s:%s" & (self.key,self.value)

# Models modeled after those in Neo.core
class NeoModel(models.Model):
    """ abstract base class for all Neo Models"""
    name = models.CharField(max_length=255,blank=True)
    description = models.TextField(blank=True)
    file_origin = models.CharField(max_length=255,blank=True)
    annotations = generic.GenericRelation(Annotation)

    objects = InheritanceManager()

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


# Lookup Tables
class Lookup(models.Model):
    """ abstract base class for all lookup tables """
    name = models.CharField(max_length=255,blank=False,unique=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name   

    class Meta:
        abstract = True
        ordering = ['name'] 

class EventType(Lookup):
    """ a type of event """
    def __unicode__(self):
        return self.name 

# Container Models
class NeoContainer(NeoModel):
    """ abstract base class for Neo Containers """
    file_datetime = models.DateTimeField(null=True,blank=True)
    rec_datetime = models.DateTimeField(null=True,blank=True)
    index = models.PositiveIntegerField(null=True,blank=True)

    class Meta(NeoModel.Meta):
        abstract = True
        ordering = ['-rec_datetime','-file_datetime','index']

class Block(NeoContainer):
    """

    The top-level container gathering all of the data, discrete and
    continuous, for a given recording session. 

    Contains Segment and RecordingChannelGroup objects.

    """

    def list_units(self):
        pass
    def list_recordingchannels(self):
        pass

       
class Segment(NeoContainer):
    """ Segment

    A container for heterogeneous discrete or continous data sharing a 
    common clock (time basis) but not necessarily the same sampling rate, 
    start time or end time. 

    A Segment can be considered as equivalent to a "trial", "episode", 
    "run", "recording", etc., depending on the experimental context. 

    May contain any of the data objects 

    """

    block = models.ForeignKey(Block,null=True,blank=True,db_index=True)

# Grouping Models
class NeoGroup(NeoModel):
    """ abstract base class for Neo Grouping Objects """
    class Meta(NeoModel.Meta):
        abstract = True

class RecordingChannelGroup(NeoGroup):
    """A group for associated RecordingChannel objects. 

    This has several possible uses:
    - for linking several AnalogSignalArray objects across several Segment 
        objects inside a Block.
    - for multielectrode arrays, where spikes may be recorded on more than 
        one recording channel, and so the RecordingChannelGroup can be used 
        to associate each Unit with the group of recording channels from 
        which it was calculated.
    - for grouping several RecordingChannel objects. There are many use 
        cases for this. For instance, for intracellular recording, it is 
        common to record both membrane potentials and currents at the same 
        time, so each RecordingChannelGroup may correspond to the 
        particular property that is being recorded. For multielectrode 
        arrays, RecordingChannelGroup is used to gather all 
        RecordingChannel objects of the same array.
    
    """
    recordingchannels = models.ManyToManyField('RecordingChannel')

    def channel_names(self):
        """get names of associated recording channels"""
        pass
    def channel_indexes(self):
        """get indices of associated recording channels"""
        pass


class RecordingChannel(NeoGroup):
    """

    Links AnalogSignal, SpikeTrain objects that come from the same logical 
    and/or physical channel inside a Block, possibly across several Segment 
    objects.
    """

    index = models.PositiveIntegerField(blank=False,null=False)

    x_coord = models.FloatField(null=True,blank=True)
    y_coord = models.FloatField(null=True,blank=True)
    z_coord = models.FloatField(null=True,blank=True)


    coord_units = models.CharField(max_length=255,choices=DISTANCE_CHOICES,blank=True)

    def coordinate(self): 
        """ 

        TODO: might be better to define coordinate as a postgres array?

        """
        return (self.x_coord, self.y_coord, self.z_coord)

class Unit(NeoGroup):
    """

    A Unit gathers all the SpikeTrain objects within a common Block, 
    possibly across several Segments, that have been emitted by the same 
    cell. 

    A Unit is linked to RecordingChannelGroup objects from which it was detected.
    """
    block = models.ForeignKey(Block,null=True,blank=True)
    recording_channel_group = models.ManyToManyField('RecordingChannelGroup')

# Data Models
class NeoData(NeoModel):
    """ abstract base class for Neo Containers """
    segment = models.ForeignKey(Segment,db_index=True)

    class Meta(NeoModel.Meta):
        abstract = True

class AnalogSignal(NeoData):
    """A regular sampling of a continuous, analog signal."""

    t_start = models.FloatField(default=0.0)
    signal = ArrayField(dbtype="float(53)",dimension=1) # dimensions: [time]
    signal_units = models.CharField(max_length=255,choices=POTENTIAL_CHOICES+CURRENT_CHOICES)
    t_units = models.CharField(max_length=16,choices=TIME_CHOICES)

    # dtype = models.CharField(max_length=255,blank=True)
    # copy = models.BooleanField(default=True)

    recording_channel = models.ForeignKey(RecordingChannel,null=True,blank=True)

    sampling_rate = models.FloatField(blank=False)

    @property
    def sampling_period(self):
        """ 1/sampling_rate """
        return 1/self.sampling_rate

    @sampling_period.setter
    def sampling_period(self,value):
        self.sampling_rate = 1/value

    @property
    def duration(self):
        """ len(signal)*sampling_period """
        return float(len(self.signal))*self.sampling_period

    @property
    def t_stop(self):
        """ t_start + duration """
        return self.t_start + self.duration

    def __unicode__(self):
        return self.name

class AnalogSignalArray(NeoData):
    """A regular sampling of a multichannel continuous analog signal.


    ----
    not sure what to do with this... 

    I'm inclined to make this a ManyToManyField w/ AnalogSignal w/ a method 
    that will generate a numpy array on-the-fly.

    alternatively, Neo people were advocating making AnalogSignalArray the 
    default and letting AnalogSignal be a 1D array.
    """
    
    analog_signals = models.ManyToManyField('AnalogSignal')


class IrregularlySampledSignal(NeoData):
    """
    
    A representation of a continuous, analog signal acquired at time 
    t_start with a varying sampling interval.

    """

    recording_channel = models.ForeignKey(RecordingChannel)



class Spike(NeoData):
    """

    One action potential characterized by its time and waveform.

    """

    time = models.FloatField()
    t_units = models.CharField(max_length=255,choices=TIME_CHOICES)

    waveforms = ArrayField(dbtype="float(53)",dimension=2) # dimensions: [channel,time]
    waveform_units = models.CharField(max_length=255,choices=POTENTIAL_CHOICES)
    sampling_rate = models.FloatField(null=True,blank=True)
    left_sweep = models.FloatField(null=True,blank=True)
    sort = models.BooleanField(default=False)

    unit = models.ForeignKey('Unit')

    def __unicode__(self):
        return self.time    

class SpikeTrain(NeoData):
    """

    A set of action potentials (spikes) emitted by the same unit in a 
    period of time (with optional waveforms).

    """
    times = ArrayField(dbtype="float(53)",dimension=1) # dimensions: [spike_time]
    t_start = models.FloatField(default=0.0)
    t_stop = models.FloatField()
    t_units = models.CharField(max_length=255,)

    waveforms = ArrayField(dbtype="float(53)",dimension=3) #  dimensions: [spike,channel,time]
    waveform_units = models.CharField(max_length=255,choices=POTENTIAL_CHOICES)
    sampling_rate = models.FloatField(null=True,blank=True)
    left_sweep = models.FloatField(null=True,blank=True)
    sort = models.BooleanField(default=False)

    def __unicode__(self):
        return len(self.times) 


class Event(NeoData):
    """A time point representng an event in the data

    """
    time = models.FloatField()
    label = models.ForeignKey(EventType,db_index=True)
    duration = models.FloatField(null=True,blank=True)

    def __unicode__(self):
        return "%s:%s" % (self.label,self.time)    

class EventArray(NeoData):
    """An array of Events
    
    """
    events = models.ManyToManyField('Event')
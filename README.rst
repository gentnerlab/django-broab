django-mr-anderson
==========

Django package that implements the a set of models and an API for
neurophysiological data using the Neo model.

Key features
-----------

- takes advantage of Postgres' support for Arrays (e.g. for 
  AnalogSignal.signal and SpikeTrain.waveforms)

- takes advantage of Postgres' support for Hstore key-value pairs (for 
  annotations)

- models can be inherited to let developers define custom data models 
  with additional fields or relationships while still conforming to the 
  Neo data model (for example, see github.com/gentnerlab/sturnus)

- to maximize interoperability with Python, Matlab, & R, data is exposed 
  via a RESTful API 


Quick start (ha!)
-----------

1. install the dependencies

	  pip install -r requirements.txt

2. Add "mr_anderson" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'mr_anderson',
      )

2. Run `python manage.py syncdb` to create the models.

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to create mr_anderson objects (you'll need the Admin app enabled).

4. Visit http://127.0.0.1:8000/admin/mr_anderson/ to view objects available.

Notable deviations from Neo
-----------

A number of data models in Neo are simply "array" versions of unidimensional 
data structures, e.g. AnalogSignal/AnalogSignalArray, Spike/SpikeTrain, 
Event/EventArray, Epoch/EpochArray. In order to simplify the schema and take
advantage of a relational database implementation of Neo, there are some key 
differences between mr_anderson and Neo.

1. The "Array" form of most objects does not exist in MrAnderson. While arrays
   are more efficient for analysis, they make it more difficult to query within
   the array. (However, I've considered adding Array models as targets of 
   ForeignKeys from their respective data model to group Events & AnalogSignals)

2. The exception to this is SpikeTrain, which is maintained while Spike is not.
   This is because it is rare that one wants to filter a query of Spikes in a 
   SpikeTrain according to some Spike-specific feature. Maintaining only 
   SpikeTrains in the database should be sufficient for the vast majority of 
   queries while also keeping the size of the SpikeTrain table down by an order 
   of magnitude.

3. Epochs do not exist in django-mr-anderson. Rather, Events 
   have an optional "duration" field. This is consistent with proposed changes 
   to Neo. 

Future goals
-----------

1. Write a neo.io.MrAndersonIO for a clean export/import to and from any Neo-supported 
   file format
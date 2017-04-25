raise Exception('Do not try to use this module! This is just draft db models.')

from django.db import models

#TODO:
#   - verbose_names
#   - on_delete constraints
#   - other useful options...

class Station(models.Model):
    name = models.ChatField(max_length=200)
    code = models.ChatField(max_length=50)


class Segment(models.Model):
    """
    Segment between nearest connected Stations in concrete Voyage.
    There can be multiple Segments between two Stations, because there can be
    multiple Voyages through this Stations
    """
    voyage = models.ForeignKey(Voyage, related_name='segments',
                               related_query_name='segment')
    seq_in_route = models.IntegerField()
    start_station = models.ForeignKey(Station)
    end_station = models.ForeignKey(Station)
    duration = models.IntegerField() # Timespan field?


class Voyage(models.Model):
    """
    Not physical path between Stations,
    but voyage direction, like: Red Arrow (Msc - Spb)
    """
    name = models.CharField(max_length=200)


class Train(models.Model):
    """
    Not physical train, but concrete trip.
    Voyage with concrete departure time.
    """
    voyage = models.ForeignKey(Voyage)
    departure = models.DateTimeField()


class Wagon(models.Model):
    train = models.ForeignKey(Train)
    number = models.IntegerField()
    kind = models.CharField() #TODO: choices


class Seat(models.Model):
    wagon = models.ForeignKey(Wagon)
    number = models.IntegerField()


class Ticket(models.Model):
    passanger_info = models.TextField()
    price = models.IntegerField()
    purchased = models.DateTimeField()


class Reservation(models.Model):
    seat = models.ForeignKey(Seat, related_name='reservations',
                             related_query_name='reservation')
    ticket = models.ForeignKey(Ticket)
    segment = models.ForeignKey(Segment)



## USE CASES
# Achtung! This are just drafts of code!  Never ran them nor did test them

## What Voyages can I use to went from Station A to Station B?
#TODO: exclue voyages where end segment earlier then start segment
voyages = Voyage.objects \
    .filter(segment__start_station__name='Station A') \
    .filter(segment__end_station__name='Station B')
print voyages


## Ok. Show me iteranary for Voyage.
voyage = voyages[0] # pick first voyage (for example)

segments = voyage.segments.all().orged_by('seq_in_route')
print segments[0].start_station.name
for segment in segments:
    print segment.end_station.name


## Nice. Are there trains for particular date (23.07.2017)?
#First, we need to calc route time between route start and 'Station A'
my_start_segment = segments.get(start_station='Station A')
segments_before_my_start = segments.filter(seq_in_route__lt=my_start_segment.seq_in_route)
route_time = sum([to_timespan(segment.duration) for segment in segments_before_my_start])

trains = Train.objects.filter(
    voyage=voyage,
    depature__gt=date('23.07.2017').start_of_day - route_time,
    depature__lt=date('23.07.2017').end_of_day - route_time
)


## Great. Do we have available seats in VIP wagon in this train for my path?
train = trains[0] # pick first train (for example)

my_start_segment = segments.get(start_station='Station A')
my_end_segment = segments.get(end_station='Station B')
segments_in_my_path = segments.filter(
    seq_in_route__gte=my_start_segment.seq_in_route,
    seq_in_route__lte=my_end_segment.seq_in_route
).order_by('seq_in_route')

available_seats = Seat.obejcts.filter(
    wagon__train=train,
    wagon__kind='VIP',
    # without reservation           without reservations for segments in my path
    Q(reservation__isnull=True) | ~Q(reservation__segment__in=segments_in_my_path)
)

## I'll take it!
my_seat = available_seats[0] # pick first available seat (for example)

my_ticket = Ticket(passanger_info="Sergey", price=100)
my_ticket.save()
#reserve seat for segments
for segment in segments_in_my_path:
    Reservation(seat=my_seat, ticket=my_ticket, segment=segment).save()


##Done!
print 'Ticket: {0}'.format(my_ticket)


























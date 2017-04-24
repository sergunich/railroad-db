raise Exception('Do not try to use this module! This is just draft db models.')

from django.db import models

#TODO:
#   - verbose_names
#   - on_delete constraints
#   - 

class Station(models.Model):
    name = models.ChatField(max_length=200)
    code = models.ChatField(max_length=50)


class Segment(models.Model):
    """
    Segment between nearest connected Stations in concrete Voyage.
    There can be multiple Segments between two Stations, because there can be
    multiple Voyages through this Stations
    """
    voyage = models.ForeignKey(Voyage)
    seq_in_route = models.IntegerField()
    start_station = models.ForeignKey(Station)
    end_station = models.ForeignKey(Station)
    duration = models.IntegerField() # Timespan field?


class Voyage(models.Model):
    """
    Not physical path between Stations,
    but voyage direction, like: Red Arrow (Msc - Spb)
    """
    name = models.ChatField(max_length=200)


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
    seat = models.ForeignKey(Seat)
    passanger_info = models.TextField()
    price = models.IntegerField()
    purchased = models.DateTimeField()


class Reservation(models.Model):
    ticket = models.ForeignKey(Ticket)
    segment = models.ForeignKey(Segment)





















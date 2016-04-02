"""
Apartment object.
"""

import persistent
import datetime
import hashlib


class Address(persistent.Persistent):
    '''
    General address
    '''
    def __init__(self, city, street, housenumber):
        self.city = city
        self.street = street
        self.housenumber = housenumber

    def __str__(self):
        return "{street}, {house} {city}".format(street=self.street,
                                                 house=self.housenumber,
                                                 city=self.city)


class Contact(persistent.Persistent):
    '''
    Contact person.
    '''
    def __init__(self, phone, email, nickname, person_name):
        self.phone = phone
        self.email = email
        self.nickname = nickname
        self.person_name = person_name

    def __str__(self):
        return "{0}\n{1}\n{2}\n{3}".format(self.phone, self.email,
                                           self.nickname, self.person_name)


class Info(persistent.Persistent):
    '''
    General info about the apartment
    '''
    def __init__(self, price, memo, rooms, sqm, day=None, month=None, year=None):
        self.price = price
        today = datetime.datetime.utcnow()
        self.available_since = datetime.datetime(day=(day or today.day),
                                                 month=(month or today.month),
                                                 year=(year or today.year))
        self.memo = memo
        self.rooms = rooms
        self.sqm = sqm

    def __str__(self):
        return "Area (sqm): {0}\nRooms: {1}\nPrice: {2}\nAvailable: {3}\nOther: {4}".format(
            self.sqm, self.rooms, self.price, self.available_since, self.memo)


class Apartment(persistent.Persistent):
    '''
    Aparment object.
    '''
    def __init__(self, address, contact, info, rating):
        self.address = address
        self.contact = contact
        self.info = info
        self.available = True
        self.rating = rating

    def hash(self):
        sum = hashlib.sha256()
        for obj in [self.address, self.contact, self.info]:
            sum.update(str(obj))
        return sum.hexdigest()

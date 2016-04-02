from places import Places
from places import place


places = Places("db/places")
for x in range(10):
    address = place.Address('Erlangen', 'Scheissstrasse', x)
    contact = place.Contact('123-123-123', 'bla@google.com', 'foobar', 'N/A')
    info = place.Info(700, rooms=2, sqm=50, day=16, month=5, memo='some free text here, e.g. your mama is fat!')
    apartment = place.Apartment(address=address, contact=contact, info=info, rating=3)
    places.add_apartment(apartment)
places.commit()

print "-" * 80
print "Found apartments:"
print "-" * 80
for apartment in places.list_apartments():
    print "Address:", apartment.address
    print "Contact:", apartment.contact
    print "Info:", apartment.info
    print "." * 80

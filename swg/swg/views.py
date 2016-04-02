from pyramid.view import view_config
from pyramid_zodbconn import get_connection
from places import Places
from places import place


def _get_address(data):
    '''
    Get address object.

    :param data:
    :return:
    '''
    errors = list()
    addr_city = data.get('address', {}).get('city')
    if not addr_city:
        errors.append("city")

    addr_street = data.get('address', {}).get('street')
    if not addr_street:
        errors.append("street")

    addr_housenr = data.get('address', {}).get('housenumber')
    if not addr_housenr:
        errors.append("house number")

    return (place.Address(addr_city, addr_street, addr_housenr),
            (errors and "Missing {0} from address".format(', '.join(errors)) or None))


def _get_contact(data):
    '''
    Create contact object.

    :param data:
    :return:
    '''
    errors = list()
    cnt_phone = data.get('contact', {}).get('phone')
    if not cnt_phone:
        errors.append("phone number")
    cnt_nick = data.get('contact', {}).get('nickname', 'N/A')
    cnt_email = data.get('contact', {}).get('email', 'N/A')
    cnt_person_name = data.get('contact', {}).get('person_name', 'N/A')

    return (place.Contact(cnt_phone, cnt_email, cnt_nick, cnt_person_name),
            errors and "Missing {0} from contact".format(', '.join(errors) or None))


def _get_info(data):
    '''
    Get general info about the apartment

    :param data:
    :return:
    '''
    nfo_year = data.get('info', {}).get('year')
    nfo_month = data.get('info', {}).get('month')
    nfo_day = data.get('info', {}).get('day')
    nfo_sqm = data.get('info', {}).get('sqm', 'N/A')
    nfo_price = data.get('info', {}).get('price', 'N/A')
    nfo_rooms = data.get('info', {}).get('rooms', 'N/A')
    nfo_memo = data.get('info', {}).get('memo', '')
    return place.Info(price=nfo_price, rooms=nfo_rooms, sqm=nfo_sqm, day=nfo_day,
                       month=nfo_month, year=nfo_year, memo=nfo_memo)


def _get_apartment(data, address, contact, info):
    '''
    Get apartment.

    :param data:
    :param address:
    :param contact:
    :param info:
    :return:
    '''
    return place.Apartment(address=address, contact=contact, info=info,
                           rating=data.get('apartment', {}).get('rating', 0))


@view_config(route_name='add', renderer='json')
def add_apartment(request):
    ret = dict()
    places = Places(get_connection(request))

    if len(request.json_body) != 4:
        ret['error_code'] = 1
        ret['error_message'] = "JSON request is not correctly encoded"
    else:
        errors = list()
        rq_addr,rq_contact, rq_info, rq_apt = request.json_body

        rq_addr, err = _get_address(rq_addr)
        errors.append(err)
        rq_contact, err = _get_contact(rq_contact)
        errors.append(err)
        rq_info = _get_info(rq_info)
        if rq_addr and rq_contact and rq_info:
            rq_apt = _get_apartment(rq_apt, rq_addr, rq_contact, rq_info)
        else:
            rq_apt = None

        errors = [item for item in errors if item]
        if not errors and rq_apt:
            places.add_apartment(rq_apt)
            places.commit()
            ret['error_code'] = 0
            ret['error_message'] = 'Apartment has been added'
        else:
            ret['error_code'] = 2
            ret['error_message'] = ', '.join(errors)

    return ret


@view_config(route_name='list', renderer='json')
def list_apartment(request):
    places = Places(get_connection(request))
    ret = list()
    for apartment in places.list_apartments():
        data = {
            'address': {
                'city': apartment.address.city,
                'street': apartment.address.street,
                'housenumber': apartment.address.housenumber,
            },
            'contact': {
                'phone': apartment.contact.phone,
                'nickname': apartment.contact.nickname,
                'email': apartment.contact.email,
                'person_name': apartment.contact.person_name,
            },
            'info': {
                'memo': apartment.info.memo,
                'price': apartment.info.price,
                'available_since': str(apartment.info.available_since),
                'rooms': apartment.info.rooms,
                'sqm': apartment.info.sqm,
            },
        }
        ret.append(data)
    return ret

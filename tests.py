from parsers import parse_time

# test urls - with/without https://

TIMES = [
    ('1245', '1245',)
    ('1245', '12:45',)
    ('1245', '12h45',)
    ('1245', '12.45pm',)
    ('1245', '12.45',)
    ('1245', '12 45')
    ('1500', '3pm'), 
    ('0700', '7am')
]

DATES = [
    '3rd July',
    '03/07',
    '3 July'
    '3-Jul'
]

DATE_TIMES = [

]

def test_times():
    for target, timestring in TIMES: 
        assert parse_time(timestring) == target


if __name__ == "__main__":
    test_times()
from . import jalali

def jalali_converter(time):
	time_to_str = "{},{},{}".format(time.year, time.month, time.day)
	time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
	y = time_to_tuple[0]
	mo = time_to_tuple[1]
	d = time_to_tuple[2]-1
	if d==0:
		d=1
	output = "{}/{}/{}, ساعت  {}:{}".format(y, mo, d+1, time.hour, time.minute)
	return output
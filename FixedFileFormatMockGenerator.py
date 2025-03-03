import json
import random
import time
from faker import Faker

fake = Faker()
################################################################################
# https://pynative.com/python-weighted-random-choices-with-probability/
# https://pynative.com/python-random-randrange/


def get_random_string(length):
    # put your letters in the following string
    sample_letters = 'abcdefghi'
    result_str = ''.join((random.choice(sample_letters)
                          for i in range(length)))
    print("Random string is:", result_str)

#numberList = [111,222,333,444,555]
#print("random item from list is: ", random.choice(numberList))

# https://faker.readthedocs.io/en/master/providers/faker.providers.python.html


def get_random_int_for_length(width, min=-99, max=-9):
    width = width-1
    min_value = '0'
    max_value = '9'
    for val in range(width):
        min_value = min_value+'0'
        max_value = max_value+'9'
    if min != -99:
        min_value = min
#       print("***** min_value Val: "+str(min_value))
    if max != -9:
        max_value = max
#       print("***** max Val: "+str(max_value))

    random_int = fake.pyint(min_value=int(min_value), max_value=int(max_value))
    return random_int


def get_date_between(start_before_time):
    mydate = fake.date_between(start_date=start_before_time, end_date='now')
    dateString = mydate.strftime("%Y%m%d")
    return dateString


def getFillerValue(width):
    fillerString = ""
    for _ in range(width):
        fillerString = fillerString + "0"
    return fillerString


def randomTime():
    # generate random number scaled to number of seconds in a day
    # (24*60*60) = 86,400

    rtime = int(random.random()*86400)

    hours = int(rtime/3600)
    minutes = int((rtime - hours*3600)/60)
    seconds = rtime - hours*3600 - minutes*60

    time_string = '%02d%02d%03d' % (hours, minutes, seconds)
    return time_string


def padding(inputString, paddingCount):
    paddingString = ''
    for _ in paddingCount:
        paddingString = paddingString + "0"
    return paddingString+inputString


def getEnumValue(_prop_col_enum_values):
    val = fake.random_choices(
        elements=(tuple(_prop_col_enum_values)), length=1)
    return val[0]

################################################################################


# starting time
start = time.time()
print("Reading input config file...")
f_config = open(
    "C:\\fixed-format-file-generator\\input_config.json", "r")
schema = f_config.read()
schema = json.loads(schema)
f_config.close()

_output = []
_properties_array = schema['properties']
_count = schema['number-of-rows']
_output_file_absolute_path = schema['output-file-absolute-path']
_per_record_length = schema['per-record-length']
print("Number of rows to be generated: "+str(_count))
name_object = schema['name']


# for each count
# iterate over all props
filename = _output_file_absolute_path + "/" + name_object + ".dat"
print("Output will be written to "+(filename))
f = open(filename, "w")
faker_string = ''
isFirstRun = True
print("Starting with mock data generation",  end=" ")
for _ in range(_count):
    print(".", end=" ")
    print(" ****** faker_string len: "+ str(len(faker_string)))
    if isFirstRun == True:
        isFirstRun = False
    if len(faker_string) != 0:
        outLen = f.write(faker_string)
        f.write("\n")
    if len(faker_string) != _per_record_length and len(faker_string) != 0:
        print("!!!!!!!!!!!!!!!!!!!!! String generated is not correct!!!!!!!!!!!!!!!!!!!!!!")

    faker_string = ''

    for _prop_item in _properties_array:
        # print(_prop_item)
        _prop_col_name = _prop_item['column-name']
        _prop_col_width = _prop_item['width']
        _prop_col_data_type = _prop_item['data-type']
        _prop_col_min_value = _prop_item.get('min')
        _prop_col_max_value = _prop_item.get('max')
        _prop_col_enum_values = _prop_item.get('enum-values')

        if _prop_col_data_type == "string":
            stringValue = fake.fixed_width(
                data_columns=[(_prop_col_width, 'name')], align='right', num_rows=1)
            faker_string = faker_string + stringValue
        elif _prop_col_data_type == "date":
            dateValue = get_date_between("-60m")
            # print(dateValue)
            faker_string = faker_string + dateValue
        elif _prop_col_data_type == "number":
            min = -99
            max = -9
            if _prop_col_min_value is not None:
                min = _prop_col_min_value
            if _prop_col_max_value is not None:
                max = _prop_col_max_value
            randomNumber = get_random_int_for_length(_prop_col_width, min, max)
            length = len(str(randomNumber))
            diff = _prop_col_width - length
            padding = ''
            if(diff > 0):
                for _ in range(diff):
                    padding = padding + "0"
            numberValue = padding + str(randomNumber)
            faker_string = faker_string + numberValue
        elif _prop_col_data_type == "filler":
            fillerValue = getFillerValue(_prop_col_width)
            faker_string = faker_string + fillerValue
            # print(fillerValue)
        elif _prop_col_data_type == "time":
            # in hhmmsst format
            timeValue = randomTime()
            faker_string = faker_string + timeValue
        elif _prop_col_data_type == "enum":
            enumValue = ''
            if _prop_col_enum_values is not None:
                enumValue = (getEnumValue(_prop_col_enum_values))
            faker_string = faker_string + enumValue

    _output.append(faker_string)
    print(" ** faker String: "+ faker_string)


# print("final faker String: "+ str(_output))
f.close()
print()
print("Finshed with mock data generation*******************")
# end time
end = time.time()
# total time taken
print(f"Time taken for execution to generate {_count} of the program is {end - start} second")
# file1 = open(filename, 'r')
# print(file1.read())
# file1.close()

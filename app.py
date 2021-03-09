from os import rename
from typing import Iterable
import config as cfg
import sys
from constants import *
from datetime import date, datetime, timedelta
from math import ceil, sin
import csv


config = None

def setup():
    global config
    try:
        config = cfg.Config('config.cfg')
    except Exception as ex:
        print(ex)
        sys.exit(1)


def generate_pr_values(blank_sheet, rows_amount, first_value):
    pr_number = None
    for i in range(len(blank_sheet)):
        if i == 0:
            pr_number = pseudo_random_value(first_value)
        else:
            pr_number = pseudo_random_value(blank_sheet[i-1][-1])
        blank_sheet[i].append(pr_number)

        for j in range(1,rows_amount):
            pr_number = pseudo_random_value(blank_sheet[i][j-1])
            blank_sheet[i].append(pr_number)
    if len(blank_sheet) == 1:
        return blank_sheet[0] 
    return blank_sheet


def linear_congruent_method(a,c,m, number):
    return (a*number+c)%m 


def pseudo_random_value(number):
    return linear_congruent_method(A, C, M, number)


def generate_one_number_id(previous_id, previous_increment):
    increment = pseudo_random_value(previous_increment)
    current_id = previous_increment + previous_id
    return current_id, increment


def id_to_hex(number):
    id = str(hex(number))
    id=id[2:len(id)].upper()
    if len(id)<10:
        id = "0"*(10-len(id)) + id
    return id


def list_id_to_hex(list_id:list):
    for i in range(len(list_id)):
        list_id[i] = id_to_hex(list_id[i])
    return list_id


def generate_numbers_ids(first_id):
    identificators = list()
    current_id = first_id
    current_increment = pseudo_random_value(current_id)
    identificators.append(current_id)
    for i in range(ALL_RECORDS - 1):
        current_id, current_increment = generate_one_number_id(current_id, current_increment)
        identificators.append(current_id)
    return identificators


def generate_id(first_id):
    identificators =  generate_numbers_ids(first_id)
    identificators = list_id_to_hex(identificators)
    return identificators


def generate_old_dates_pr_numbers():
    return generate_pr_values([[],[],[]], OLD_RECORDS, config['first_values']['old_dates'])


def generate_cur_dates_pr_numbers():
    return generate_pr_values([[],[],[],[]], CURRENT_RECORDS, config['first_values']['current_dates'])


def generate_new_dates_pr_numbers():
    return generate_pr_values([[],[],[]], NEW_RECORDS, config['first_values']['new_dates'])


def get_time_increment(dates_pr):
    time_increments = []
    for i in range (len(dates_pr)):
        time_increments.append([])
        for j in range(len(dates_pr[i])):
            time_increments[i].append( (dates_pr[i][j] % config['date']['max_date_increment']) /1000)
    return time_increments


def get_time_increment_from_begining(time_increments):
    time_increments_from_begining = [[]]
    time_increments_from_begining[0].append(time_increments[0][0])
    
    for i in range(1,len(time_increments[0])):
        time_increments_from_begining[0].append(time_increments_from_begining[0][i-1]+time_increments[0][i])
    
    for i in range (1, len(time_increments)):
        time_increments_from_begining.append([])
        for j in range(len(time_increments[i])):
            time_increments_from_begining[i].append( time_increments_from_begining[i-1][j] + time_increments[i][j] )
    
    return time_increments_from_begining


def get_dates(time_increments, first_date:datetime):
    dates = []
    for i in range (len(time_increments)):
        dates.append([])
        for j in range (len(time_increments[i])):
            time_increment = timedelta(seconds=time_increments[i][j])
            dates[i].append(first_date + time_increment)
    return dates


def wipe_dates(pr_numbers, dates):
    #takes one-dimensional list of pseudo-random values for dates generating and one-dimensional list of dates
    if len(pr_numbers) !=  len(dates):
        return dates
    for i in range(len(pr_numbers)):
        if pr_numbers[i] % 5 == 0:
            dates[i] = ""
    return dates


def generate_old_dates():
    pr_numbers = generate_old_dates_pr_numbers()
    increments = get_time_increment(pr_numbers)
    increments = get_time_increment_from_begining(increments)
    first_date = datetime.strptime(config['date']['first_date'], config['date']['config_date_format'])
    dates = get_dates(increments, first_date)
    dates[0] = wipe_dates(pr_numbers[0],dates[0])
    dates.insert(0, ["" for i in range(OLD_RECORDS)])
    return dates


def generate_cur_dates():
    pr_numbers = generate_cur_dates_pr_numbers()
    increments = get_time_increment(pr_numbers)
    increments = get_time_increment_from_begining(increments)
    first_date = datetime.strptime(config['date']['first_date'], config['date']['config_date_format'])
    dates = get_dates(increments, first_date)
    return dates


def generate_new_dates():
    pr_numbers = generate_new_dates_pr_numbers()
    increments = get_time_increment(pr_numbers)
    increments = get_time_increment_from_begining(increments)
    first_date = datetime.strptime(config['date']['first_new_date'], config['date']['config_date_format'])
    dates = get_dates(increments, first_date)
    dates[-1] = wipe_dates(pr_numbers[-1],dates[-1])
    dates.append(["" for i in range(NEW_RECORDS)])
    return dates


def generate_dates():
    dates=[]
    old_dates = generate_old_dates()
    current_dates = generate_cur_dates()
    new_dates = generate_new_dates()
    for i in range(len(old_dates)):
        dates.append(old_dates[i]+current_dates[i]+new_dates[i])
    return dates


def generate_price_pr():
    return generate_pr_values([[]], ALL_RECORDS, config['first_values']['px_init'])


def get_instrument_number(price_pr:list):
    instruments_amount = len(config['instrument'])
    instrument_numbers = list()
    for i in range(len(price_pr)):
        instrument_numbers.append(price_pr[i] % instruments_amount) 
    return instrument_numbers


def get_price_koef(pr_number):
    number = sin(pr_number)
    if number >= 0:
        return 1
    return -1


def generate_price_increment(price_pr, instrument_numbers):
    price_increments = []
    for i in range(len(price_pr)):
        price_increment = price_pr[i] / M
        price_increment = ceil(price_increment*100)
        price_increment *= float(config['instrument'][instrument_numbers[i]]['min_deviation'])
        price_increment *= get_price_koef(price_pr[i])
        price_increments.append(price_increment)
    return price_increments


def generate_status_pr():
    return generate_pr_values([[]], ALL_RECORDS, config['first_values']['third_status'])


def generate_one_type_status(status_dates, status_number):
    statuses = []
    for i in range(len(status_dates)):
        if status_dates[i] != "":
            statuses.append(config['statuses'][status_number])
        else:
            statuses.append("")
    return statuses


def generate_3d_status(status_dates):
    pr_numbers = generate_status_pr()
    statuses = []
    for i in range(len(status_dates)):
        if status_dates[i] != "":
            statuses.append(config['statuses'][2][pr_numbers[i]%3])
        else:
            statuses.append("")
    return statuses


def generate_all_statuses(all_dates):
    statuses = []
    for i in range(4):
        if i == 2:
            statuses.append(generate_3d_status(all_dates[i]))
        else:
            statuses.append(generate_one_type_status(all_dates[i],i))
    return statuses


def generate_px_fill(third_statuses:list, instrument_numbers, price_pr):
    price_incremets = generate_price_increment(price_pr, instrument_numbers)
    prices =[[],[],[]]
    for i in range(ALL_RECORDS):
        prices[0].append(config['instrument'][instrument_numbers[i]]['quotation'])
        prices[1].append(config['instrument'][instrument_numbers[i]]['price'])
        if third_statuses[i] != config['statuses'][2][2]:
            prices[2].append(prices[1][i]+price_incremets[i])
        else: 
            prices[2].append("")
    return prices


def format_prices(prices, instrument_numbers):
    for i in range(len(prices[1])):
        prices[1][i] = format_price(prices[1][i], instrument_numbers[i])
        prices[2][i] = format_price(prices[2][i], instrument_numbers[i])
    return prices


def generate_prices(statuses):
    price_pr = generate_price_pr()
    instrument_numbers = get_instrument_number(price_pr)
    prices = generate_px_fill(statuses[2],instrument_numbers,price_pr)
    prices = format_prices(prices, instrument_numbers)
    return prices


def format_price(price, instrument_number):
    if price == "":
        return price
    decimal_amount = config['instrument'][instrument_number]['min_deviation']
    decimal_amount = len( str(decimal_amount) ) -2
    price = round(price,decimal_amount)
    price = str(price)
    price += '0'*(6-len(price)+1)
    return price


def generate_volume_pr_numbers():
    return generate_pr_values([[],[]], ALL_RECORDS, config['first_values']['volume'])
    

def generate_volume_init_lots(volume_init_pr):
    volume_init_lots = list()
    for i in range(len(volume_init_pr)):
        volume_init_lots.append(volume_init_pr[i]/M)
        volume_init_lots[i]*=config['volume']['max'] * 100
        volume_init_lots[i] = ceil(volume_init_lots[i])
        volume_init_lots[i] /= 100
    return volume_init_lots


def generate_volume_difference_in_lots(volume_fill_pr, volume_init):
    volume_diff = list()
    for i in range(len(volume_fill_pr)):
        max_diff = volume_init[i] * config['volume']['max_difference']
        volume_diff.append( volume_fill_pr[i] / M)
        volume_diff[i]*=max_diff
        volume_diff[i] = ceil(volume_diff[i] * 100) /100
    return volume_diff


def generate_side(pr_number):
    sides = []
    for i in range(len(pr_number)):
        sides.append(config['sides'][pr_number[i]%2])
    return sides


def generate_volumes(statuses):
    volumes = []
    pr_numbers = generate_volume_pr_numbers()
    volume_init = generate_volume_init_lots(pr_numbers[0])
    volume_diff = generate_volume_difference_in_lots(pr_numbers[1],volume_init)
    volumes.append ( get_volumes(volume_init))
    volumes.append(get_volume_fill(statuses[2], volume_init, volume_diff))
    volumes.append( generate_side(pr_numbers[1]))
    return volumes


def get_volumes(volume_lots):
    volumes = []
    for i in range(len(volume_lots)):
        volumes.append( volume_lots[i] * config['volume']['lot_size'])
        if volumes[i] != "":
            volumes[i] = ceil(volumes[i])
    return volumes


def get_volume_fill(third_statuses, volume_init, volume_diff):
    volumes = []
    for i in range(len(volume_init)):
        if third_statuses[i] == config['statuses'][2][2]:
            volumes.append("")
        elif third_statuses[i] == config['statuses'][2][0]:
            volumes.append(volume_init[i])
        else:
            volumes.append(volume_init[i] - volume_diff[i])
    return get_volumes(volumes)


def generate_notes_pr():
    return generate_pr_values([[]], ALL_RECORDS, config['first_values']['notes'])


def generate_notes():
    notes = []
    notes_pr = generate_notes_pr()
    for i in range(ALL_RECORDS):
        notes.append(config['notes'][notes_pr[i] % config['notes_amount']])
    return notes


def generate_tags_pr():
    return generate_pr_values([[] for i in range(config['tags_amount'])], ALL_RECORDS, config['first_values']['tags'])


def generate_tags():
    tags = []
    tags_pr = generate_tags_pr()
    for i in range(len(tags_pr[0])):
        row_tags = ''
        for j in range(len(tags_pr)):
            if tags_pr[j][i] % config['tag_divider'] == 0:
                row_tags += config['tags'][j] + ';'
        tags.append(row_tags.strip())
    return tags


def unite_data():
    id = generate_id(config['first_values']['id'])  # 1 field
    dates = generate_dates()                        # 4 fileds
    statuses = generate_all_statuses(dates)         # 4 fileds
    prices = generate_prices(statuses)              # 3 fileds: instrument, init, fill
    volumes = generate_volumes(statuses)            # 3 fileds: init, fill, side
    tags = generate_tags()                          # 1 filed
    notes = generate_notes()                        # 1 filed
    data = [id, *dates, *statuses, *prices, *volumes, tags, notes]
    formatted_data = []
    for i in range(ALL_RECORDS):
        row= []
        for j in range(len(data)):
            row.append(data[j][i])
        formatted_data.append(row)
    return formatted_data


def get_one_status_data(row_data, status_number):
    if row_data[1 + status_number - 1] == '':
        return []
    
    status_data = [row_data[0], row_data[9], row_data[10], row_data[11], row_data[14], row_data[12], row_data[13], 
        row_data[1 + status_number - 1], row_data[5 + status_number - 1], row_data[-1], row_data[-2]]
    
    if status_number == 1 or status_number == 2:
        status_data[3] = ''
        status_data[6] = ''

    return status_data 


def get_all_statuses_data(row_data):
    one_status_fields = []
    for i in range(4):
        field = get_one_status_data(row_data, i+1)
        if field != []:
            one_status_fields.append(field)
    return one_status_fields
    

def get_all_data():
    data = unite_data()
    all_data = []
    for row_data in data:
        all_data += get_all_statuses_data(row_data)
    all_data = sorted(all_data, key= lambda data: data[7])
    return all_data


def format_data_for_output(all_data):
    formatted_data = []
    for i in all_data:
        formatted_data.append(i)
        formatted_data[-1][7] = format_date(i[7],config['date']['result_date_format'])

    return formatted_data        


def format_date(in_date:datetime, format:str):
    formatted_date = in_date.strftime(format)
    formatted_date = formatted_date[0:-3]
    return formatted_date


def format_data_for_mysql(all_data):
    formatted_data = []
    for i in range(len(all_data)):
        formatted_data.append(all_data[i])
        formatted_data[-1][7] = format_date(formatted_data[-1][7], config['date']['db_date_format'])
        formatted_data[-1][7] = f"'{formatted_data[-1][7]}'"
        formatted_data[-1][0] = f"'{formatted_data[-1][0]}'"
        formatted_data[-1][1] = f"'{formatted_data[-1][1]}'"
        formatted_data[-1][4] = f"'{formatted_data[-1][4]}'"
        formatted_data[-1][8] = f"'{formatted_data[-1][8]}'"
        formatted_data[-1][9] = f"'{formatted_data[-1][9]}'"
        formatted_data[-1][10] = f"'{formatted_data[-1][10]}'"
        if formatted_data[-1][3] == '':
            formatted_data[-1][3] = 'NULL'
        if formatted_data[-1][6] == '':
            formatted_data[-1][6] = 'NULL'
    return formatted_data
            

def write_to_csv(filename:str, data:Iterable):
    try:
        with open(filename, mode='w') as employee_file:
            writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(data)
            
    except Exception as ex:
        print(f'Error while writing to CSV: {ex}')
        sys.exit(1)


def write_inserts(filename, data):
    data = make_inserts(data)
    try:
        with open(filename, 'w') as file:
            file.writelines(data)
    except Exception as ex:
        print(f'Error while writing to file: {ex}')
        sys.exit(1)


def make_inserts(data):
    inserts = []
    for i in range(len(data)):
        inserts.append(make_insert_string(i+1,data[i]))
    return inserts


def make_insert_string(id, data_row):
    insert = INSERT_BASE + str(id) + ','
    for i in data_row:
        insert+= str(i) + ','
    insert = insert[0:-1]
    insert += ');\n'
    return insert


def main():
    setup()
    data = get_all_data()
    write_inserts('order1.txt', format_data_for_mysql(data))


if __name__ == "__main__":
    main()
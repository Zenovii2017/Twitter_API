import folium
import copy
from geopy.geocoders import ArcGIS


def read_file(path, year):
    """
    (path, int) -> dict
    Reads file and delete all data that can cause problems, mistakes and
    errors.
    Read only data that is in year.
    return dictionary with keys of position and value with name of films
    """
    #make needed year, new dict and read file
    year = str('(' + str(year) + ')')
    output_dict = dict()
    with open(path, 'r', encoding='utf-8', errors='ignore') as open_file:
        lines = open_file.readlines()[15:-1]
        for line in lines:
            line = line.strip().split()
            for word in line:
                # check if film year is needed year
                if word.startswith(year):
                    line1 = []
                    j = 0
                    # next lot line delete unnecessary characters
                    for i in range(len(line)):
                        if i == j:
                            if line[i].startswith("{"):
                                while (line[j].endswith("}") is False):
                                    j += 1
                                else:
                                    j += 1
                            else:
                                line1.append(line[j])
                                j += 1
                    if line1[-1].endswith(')'):
                        while line1[-1].startswith('(') is False:
                            del line1[-1]
                        else:
                            del line1[-1]
                    string = ''
                    for i in range(len(line1)):
                        if line1[i] != year and \
                                    line1[i].startswith('(') is not True:
                            string += line1[i] + ' '
                        else:
                            value = copy.deepcopy(string)
                            string = ''
                        if i == (len(line1) - 1):
                            key = copy.deepcopy(string)
                    try:
                        lenght_dict = len(output_dict[key])
                        new_value = []
                        for i in range(len(output_dict[key])):
                            if output_dict[key][i] not in new_value:
                                new_value.append(output_dict[key][i])
                        if value not in new_value:
                            if "'" not in value:
                                new_value.append(value)
                            else:
                                value1 = ''
                                for i in range(len(value)):
                                    if value[i] != "'":
                                        value1 += value[i]
                                new_value.append(value1)
                        output_dict[key] = new_value
                    except:
                        try:
                            new_value = []
                            new_value.append(output_dict[key])
                            if value not in new_value:
                                if "'" not in value:
                                    new_value.append(value)
                                else:
                                    value1 = ''
                                    for i in range(len(value)):
                                        if value[i] != "'":
                                            value1 += value[i]
                                    new_value.append(value1)
                            output_dict[key] = new_value
                        except:
                            if "'" not in value:
                                output_dict[key] = value
                            else:
                                value1 = ''
                                for i in range(len(value)):
                                    if value[i] != "'":
                                        value1 += value[i]
                                output_dict[key] = value1
                    break
    return output_dict


def change_adress(adress):
    """
    (str) -> (list)
    Remake name of position in coordinates
    return list of two coordinates
    """
    geolocator = ArcGIS()
    try:
        location = geolocator.geocode(adress)
        Coordinates = [location.latitude, location.longitude]
        return Coordinates
    except:
        return change_adress(adress)


def write_file(dct, keys):
    """
    (dict, list) -> None
    Write dict and list of coordinates in file.
    return None
    """
    j = 0
    with open('result.txt', 'w') as result_file:
        for key in dct:
            sentence = str(key) + '\ncoordinates: ' + str(keys[j])
            result_file.write(sentence)
            result_file.write('\n')
            for i in range(len(dct[key])):
                result_file.write(dct[key][i])
            result_file.write('\n')
            j += 1


def create_map(input_dict, keys, n):
    """
    (dict,list, int) -> None
    input dict with data and list of keys with coordinates
    return None
    """
    map = folium.Map(tiles="Mapbox Bright")
    map = folium.Map()
    all_country = []
    all_count = []
    fg_pp = folium.FeatureGroup(name="Population")
    fg_pp.add_child(folium.GeoJson(data=open('World.json', 'r',
                                             encoding='utf-8-sig').read(),
                                   style_function=lambda x: {
                                       'fillColor': 'green'
                                       if x['properties']['POP2005'] < 15000000
                                       else 'orange' if 15000000 <=
                                       x['properties']['POP2005'] < 25000000
                                       else 'red'}))
    index = 0
    for key in input_dict:
        all_sentence = ''
        if type(input_dict[key]) != str:
            all_count.append(len(input_dict[key]))
        else:
            all_count.append(1)
        name_country = key[-2]
        j = -2
        while key[j] != ' ':
            if key[j] != ' ':
                name_country += key[j]
            j -= 1
        else:
            if key[j] != ' ':
                name_country += key[j]
            true_name_country = ''
            for i in range(len(name_country) - 1, 0, -1):
                true_name_country += name_country[i]
            all_country.append(true_name_country)
        for sentence in input_dict[key]:
            all_sentence += sentence
        map.add_child(folium.Marker(location=keys[index],
                                    popup=all_sentence,
                                    icon=folium.Icon()))
        index += 1
    top_country = []
    for i in range(n):
        while len(top_country) != n and len(all_country) != 0:
            max_count = max(all_count)
            index_max_count = all_count.index(max_count)
            if all_country[index_max_count] not in top_country:
                top_country.append(copy.deepcopy(all_country[index_max_count]))
            del all_count[index_max_count]
            del all_country[index_max_count]
            if len(all_country) == 0 or len(top_country) == n:
                break
                break
    fg_tc = folium.FeatureGroup(name="Top country")
    fg_tc.add_child(folium.GeoJson(data=open('World.json', 'r',
                                             encoding='utf-8-sig').read(),
                                   style_function=lambda x: {
                                    'fillColor': 'green'
                                    if x['properties']['NAME'] in top_country
                                    else 'red'}))
    fg_pa = folium.FeatureGroup(name="Population/Area")
    fg_pa.add_child(folium.GeoJson(data=open('World.json', 'r',
                                             encoding='utf-8-sig').read(),
                                   style_function=lambda x: {
                                      'fillColor': 'green'
                                       if x['properties']['AREA'] == 0
                                       or x['properties']['POP2005'] /
                                       x['properties']['AREA'] > 2000
                                       else 'orange' if 1000 <=
                                       x['properties']['POP2005'] /
                                       x['properties']['AREA'] < 2000
                                       else 'red'}))
    map.add_child(fg_tc)
    map.add_child(fg_pp)
    map.add_child(fg_pa)
    map.add_child(folium.LayerControl())
    map.save('Result_Map.html')


def main():
    """
    None -> None
    read year and make map with films place
    return None
    """
    print('Please input year.P.S.Year must be integer.At least 1883:')
    year = -1
    while year < 1883:
        try:
            year = int(input())
            if year < 1883:
                print("Input new year at least 1883 and integer")
        except:
            print("Input new year at least 1883 and integer")
    print("Do you want to write data to file?")
    indent = input()
    if indent == "Yes" or indent == indent == "yes":
        indent = 1
    else:
        print("We think you input no!")
    print("Start reading file...")
    readed_file = read_file('locations.list', year)
    print("End reading file and start remake coordinates...")
    keys = []
    for key in readed_file:
        key1 = change_adress(key)
        keys.append(key1)
    print("End remake coordinates")
    if indent == 1:
        print("Start writing data in file...")
        write_file(readed_file, keys)
        print("End writing in file")
    print("How many countries should be in the top")
    while True:
        try:
            count = int(input())
            break
        except:
            print("Input count must be integer")
    print("Start making map...")
    create_map(readed_file, keys, count)
    print("All done!")


main()

# -*- coding: utf-8 -*-


handler = open('C:/Users/carlos.dlheras/Desktop/HotelScan/hoteles y direcciones/new_cities_fr_EUR.csv', 'r',encoding="utf-8")
newfile = open('C:/Users/carlos.dlheras/Desktop/HotelScan/hoteles y direcciones/new_cities_fr_EUR transpose.csv', 'w')

def ifzero(string):
    try:
        correction = str(int(string))
    except ValueError:
        correction = '0'
    return correction



newfile.write('GeoId,property_en,number,min_price,Location\n')

lines = 4999
multiplier = 0
try:
    for line in handler:
        lines += 1
        if lines == 5000:
            lines = 0
            if multiplier == 0:
                multiplier += 1
                continue
            print('transposed line ' + str(multiplier * 5000))
            multiplier += 1
        try:
            # print(line)
            Ls = line.split('\t')
            newfile.write(Ls[0] + ',properties,' + ifzero(Ls[6]) + ',' + ifzero(Ls[7]) + ',' + Ls[1] + '\n')
            newfile.write(Ls[0] + ',apartment,' + ifzero(Ls[8]) + ',' + ifzero(Ls[9]) + ',' + Ls[1] + '\n')
            newfile.write(Ls[0] + ',bnb,' + ifzero(Ls[10]) + ',' + ifzero(Ls[11]) + ',' + Ls[1] + '\n')
            newfile.write(Ls[0] + ',guesthouse,' + ifzero(Ls[12]) + ',' + ifzero(Ls[13]) + ',' + Ls[1] + '\n')
            newfile.write(Ls[0] + ',hostel,' + ifzero(Ls[14]) + ',' + ifzero(Ls[15]) + ',' + Ls[1] + '\n')
            newfile.write(Ls[0] + ',hotel,' + ifzero(Ls[16]) + ',' + ifzero(Ls[17]) + ',' + Ls[1] + '\n')
            newfile.write(Ls[0] + ',motel,' + ifzero(Ls[18]) + ',' + ifzero(Ls[19]) + ',' + Ls[1] + '\n')
            newfile.write(Ls[0] + ',resort,' + Ls[20] + ',' + ifzero(Ls[21]) + ',' + Ls[1] + '\n')
        except UnicodeEncodeError:
            print('Unicode error -> ', line)
            pass
        except:
            print('Unexpected error -> ', line)
            pass
except UnicodeDecodeError:
    print(lines)
    print(line)
    pass



import csv

years = []
months = []
CO2_values = []
years_list = []
years_dictionary = {}
anomaly = {}
winter = []  # December, January, February
spring = []  # March, April, May
summer = []  # June, July, August
autumn = []  # September, October, November

with open("co2-ppm-daily.csv") as CO2:
    csv_file = csv.reader(CO2, delimiter=',')
    next(CO2)
    for line in csv_file:       # creates lists for years and C02 values
        year, month_irrelevant, day_irrelevant = line[0].split("-")
        if year not in years:
            years.append(year)
        CO2_values.append(float(line[1]))

C02_minimum = min(CO2_values)
C02_maximum = max(CO2_values)
C02_sum = sum(CO2_values)
C02_average = float(C02_sum)/len(CO2_values)

with open("co2-ppm-daily.csv") as CO2:      # creating lists for the average of each season
    csv_file = csv.reader(CO2, delimiter=',')
    next(CO2)
    for line in csv_file:       # seperate each month and put them into their seasons
        year_irrelevant, month, day_irrelevant = line[0].split("-")
        if month == '12':
            winter.append(float(line[1]))
        if month == '01':
            winter.append(float(line[1]))
        if month == '02':
            winter.append(float(line[1]))
        if month == '03':
            spring.append(float(line[1]))
        if month == '04':
            spring.append(float(line[1]))
        if month == '05':
            spring.append(float(line[1]))
        if month == '06':
            summer.append(float(line[1]))
        if month == '07':
            summer.append(float(line[1]))
        if month == '08':
            summer.append(float(line[1]))
        if month == '09':
            autumn.append(float(line[1]))
        if month == '10':
            autumn.append(float(line[1]))
        if month == '11':
            autumn.append(float(line[1]))
Winter_avg = sum(winter)/len(winter)
Spring_avg = sum(spring) / len(spring)
Summer_avg = sum(summer) / len(summer)
Fall_avg = sum(autumn) / len(autumn)

for year in years:      # creating a list for the average of each year
    with open("co2-ppm-daily.csv") as CO2:
        csv_file = csv.reader(CO2, delimiter=',')
        next(CO2)
        for line in csv_file:
            year_values, month_irrelevant, day = line[0].split("-")
            if year_values == year:
                years_list.append(float(line[1]))
    years_list_sum = sum(years_list)
    years_list_length = len(years_list)
    years_dictionary[year] = str(years_list_sum / years_list_length)

with open("co2-ppm-daily.csv") as CO2:
    csv_file = csv.reader(CO2, delimiter=',')
    next(CO2)
    for line in csv_file:                       # calculating the anomoly for each year
        year_CO2, month_irrelevant, day_irrelevant = line[0].split("-")
        anomaly[year_CO2] = float(line[1]) - C02_average

print("The maximum CO2 is " + str(C02_maximum) + " ppm.")
print("The minimum CO2 is " + str(C02_maximum) + " ppm.")
print("The average CO2 is " + str(C02_average) + " ppm.")

print("The winter average is " + str(Winter_avg) + " ppm.")
print("The spring average is " + str(Spring_avg) + " ppm.")
print("The summer average is " + str(Summer_avg) + " ppm.")
print("The autumn average is " + str(Fall_avg) + " ppm.\n")

print("The yearly average is:\n")
print(years_dictionary)
print()
print("The anomaly for each year is:\n")
print(anomaly)

#All looks great, well done.
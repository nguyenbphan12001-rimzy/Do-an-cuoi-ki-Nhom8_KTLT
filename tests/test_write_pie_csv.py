import csv

with open('../Datasets/pie_data.csv', mode='w', encoding='utf8') as f:
    gym_data = csv.writer(f, delimiter=',', quotechar='"')
    gym_data.writerow(['Gói tập', 'Số người'])
    gym_data.writerow(['Không chọn', '5'])
    gym_data.writerow(['2 tuần', '8'])
    gym_data.writerow(['1 tháng', '25'])
    gym_data.writerow(['3 tháng', '35'])
    gym_data.writerow(['6 tháng', '17'])
    gym_data.writerow(['12 tháng', '10'])


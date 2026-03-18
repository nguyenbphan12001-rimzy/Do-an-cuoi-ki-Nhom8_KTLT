import csv

with open('../Datasets/bar_data.csv', mode='w', encoding='utf8') as f:
    bar_data = csv.writer(f, delimiter=',', quotechar='"')
    bar_data.writerow(['Tháng', 'triệu đồng'])
    bar_data.writerow(['1', '60'])
    bar_data.writerow(['2', '55'])
    bar_data.writerow(['3', '70'])
    bar_data.writerow(['4', '150'])
    bar_data.writerow(['5', '110'])
    bar_data.writerow(['6', '100'])
    bar_data.writerow(['7', '105'])
    bar_data.writerow(['8', '105'])
    bar_data.writerow(['9', '120'])
    bar_data.writerow(['10', '100'])
    bar_data.writerow(['11', '110'])
    bar_data.writerow(['12', '90'])


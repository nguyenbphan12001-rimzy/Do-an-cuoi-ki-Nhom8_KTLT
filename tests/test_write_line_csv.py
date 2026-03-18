import csv

with open('../Datasets/line_data.csv', mode='w', encoding='utf8') as f:
    line_data = csv.writer(f, delimiter=',', quotechar='"')
    line_data.writerow(['Ngày', 'Số lượng đặt'])
    line_data.writerow(['Thứ hai', '15'])
    line_data.writerow(['Thứ ba', '12'])
    line_data.writerow(['Thứ tư', '10'])
    line_data.writerow(['Thứ năm', '18'])
    line_data.writerow(['Thứ sáu', '24'])
    line_data.writerow(['Thứ bảy', '26'])
    line_data.writerow(['Chủ nhật', '30'])



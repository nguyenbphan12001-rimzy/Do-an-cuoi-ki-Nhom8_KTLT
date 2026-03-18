import csv
with open('../Datasets/pie_data.csv', newline='',encoding= 'utf8') as f:
    #Nếu thiếu "newline=" thì trên windows có th bị dòng trống xen kẽ
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    for row in reader:
        print(' - '.join(row))
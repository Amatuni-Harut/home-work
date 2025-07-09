import argparse
import xlsxwriter
def read_people(fname):
    people_info = []
    try:
        with open(fname, 'r') as f:
            num_line = 1
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 4:
                    try:
                        age = int(parts[2])
                        person = {
                            'name': parts[0],
                            'surname': parts[1],
                            'age': age,
                            'profession': parts[3].replace('_', ' ')
                        }
                        people_info.append(person)
                    except ValueError:
                        print(f"[error] {num_line} -- {line.strip()}")
                else:
                    print(f"[error] {num_line} --- {line.strip()}")
                num_line += 1
    except FileNotFoundError:
        print(f"[error] file '{fname}' not found")
    return people_info
def write_to_excel(data, eczel_file, profes_filter=None):
    try:
        workbook = xlsxwriter.Workbook(eczel_file)
        worksheet = workbook.add_worksheet('People_info')
        format1 = workbook.add_format({
            'bold': True, 
            'bg_color': '#FFFF00',
            'border': 1,
            'align': 'center'
        })
        format2 = workbook.add_format({
            'bg_color': '#C6EFCE', 
            'border': 1
        })
        headers = ['Name', 'Surname', 'Age', 'Profesion']
        if profes_filter:
            headers.append(profes_filter)
        col_num = 0
        for header in headers:
            worksheet.write(0, col_num, header, format1)
            col_num += 1
        row_num = 1
        for person in data:
            if person['age'] > 25:
                row_format = format2
            else:
                row_format = None 
            worksheet.write(row_num, 0, person['name'], row_format)
            worksheet.write(row_num, 1, person['surname'], row_format)
            worksheet.write(row_num, 2, person['age'], row_format)
            worksheet.write(row_num, 3, person['profession'], row_format)
            if profes_filter:
                if person['profession'].lower() == profes_filter.lower():
                    match = 'yes'
                else:
                    match = '' 
                worksheet.write(row_num, 4, match, row_format)
            row_num += 1
        workbook.close()
        print("Excel-file is created")
    except Exception as e:
        print(f"[error] {e}")
def main():
    parser = argparse.ArgumentParser(description="Creating Excel file using data from txt file")
    parser.add_argument('-n', action='store_true', help="sorting by name")
    parser.add_argument('-p', metavar='PROFESSION', help="filtration by profession")
    parser.add_argument('-i', '--input', default='data.txt', help="enter input file name (default: data.txt)")
    parser.add_argument('-o', '--output', default='data.xlsx', help="enter output file name (default: data.xlsx)")
    args = parser.parse_args()
    data = read_people(args.input)
    if not data:
        print("error")
        return
    if args.n:
        data.sort(key=lambda x: x['name'])  
        print("information is sorted")
    write_to_excel(data, args.output, profes_filter=args.p)

if __name__ == '__main__':
    main()

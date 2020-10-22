
def process_date(date):
    folder = date.replace('/', '')
    list_folder = list(folder)
    if len(folder) == 7:
        list_folder.insert(4, '0')
        folder = ''.join(list_folder)
    elif len(folder) == 6:
        list_folder.insert(4, '0')
        list_folder.insert(6, '0')
        folder = ''.join(list_folder)
    return folder


if __name__ == '__main__':
    dd = process_date('2020/7/03')
    print(dd)

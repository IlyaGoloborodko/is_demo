import locale


def sort_companies_by_name(but, user_field):
    res = but.call_list_method('crm.company.userfield.list', {'FILTER': {'FIELD_NAME': user_field}})[0]

    field_id = res['ID']
    comp_list = res['LIST']

    locale.setlocale(locale.LC_ALL, '')

    def sort_key(item):
        return locale.strxfrm(item['VALUE'])

    sorted_companies = sorted(comp_list, key=sort_key)
    for index, company in enumerate(sorted_companies):
        company['SORT'] = index

    but.call_list_method('crm.company.userfield.update', {'ID': field_id, 'FIELDS': {'LIST': sorted_companies}})
from django import forms


class FieldSelectionForm(forms.Form):
    def find_user_fields(self, but):
        res = but.call_list_method('crm.company.userfield.list')

        clearly_list = [i['ID'] for i in res if i['USER_TYPE_ID'] == 'enumeration']
        fields_dict = {}
        for field_id in clearly_list:
            fields_dict[field_id] = but.call_list_method('crm.company.userfield.get', {'ID': field_id})

        # Создаем список
        choices = [(i['FIELD_NAME'], i['EDIT_FORM_LABEL']['ru']) for i in fields_dict.values()]

        self.fields['user_field'] = forms.ChoiceField(choices=choices)

        return res

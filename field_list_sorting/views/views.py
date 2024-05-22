import locale

from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from field_list_sorting.forms import FieldSelectionForm
from field_list_sorting.funcs.sort_companies import sort_companies_by_name


@main_auth(on_cookies=True)
def sort_companies_list(request):
    but = request.bitrix_user_token

    if request.method == "POST":
        form = FieldSelectionForm(request.POST)
        if form.is_valid():
            user_field = form.data['user_field']
            sort_companies_by_name(but, user_field)

    form = FieldSelectionForm()
    form.find_user_fields(but)

    return render(request, 'main.html', {'form': form})

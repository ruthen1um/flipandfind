from datetime import datetime


def store(request):
    current_year = datetime.now().year
    company_name = 'ООО "Матвейчик"'
    site_name = 'Flip & Find'
    context = {
        'current_year': current_year,
        'company_name': company_name,
        'site_name': site_name,
    }
    return context

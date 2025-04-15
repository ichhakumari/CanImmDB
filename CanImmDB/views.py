from django.shortcuts import render
from django.db.models import Q
from .models import ClinicalTrials
from django.http import HttpResponse




def main(request):
    trials = ClinicalTrials.objects.all()
    return render(request, 'main.html', {'trials': trials})



#--------------------------------------------------------------Basic search record--------------------------------------------------


def search_records(request):
    query = request.GET.get('q', '')
    disease_filter = request.GET.get('disease', '')
    antigen_filter = request.GET.get('antigen', '')
    year_filter = request.GET.get('year', '')
    sex_filter = request.GET.get('sex', '')

    records = ClinicalTrials.objects.all()

    if query:
        records = records.filter(
            Q(disease__icontains=query) |
            Q(disease_description__icontains=query) |
            Q(antigen__icontains=query) |
            Q(pubmed_id__icontains=query) |
            Q(clinical_trail_number__icontains=query) |
            Q(car_t_design__icontains=query)
        )

    if disease_filter:
        records = records.filter(disease=disease_filter)
    if antigen_filter:
        records = records.filter(antigen=antigen_filter)
    if year_filter:
        records = records.filter(year=year_filter)
    if sex_filter:
        records = records.filter(sex=sex_filter)

    # Distinct dropdown values
    diseases = ClinicalTrials.objects.exclude(disease__isnull=True).values_list('disease', flat=True).distinct().order_by('disease')
    antigens = ClinicalTrials.objects.exclude(antigen__isnull=True).values_list('antigen', flat=True).distinct().order_by('antigen')
    years = ClinicalTrials.objects.exclude(year__isnull=True).values_list('year', flat=True).distinct().order_by('year')
    sexes = ClinicalTrials.objects.exclude(sex__isnull=True).values_list('sex', flat=True).distinct().order_by('sex')

    return render(request, "search.html", {
        "records": records,
        "query": query,
        "diseases": diseases,
        "antigens": antigens,
        "years": years,
        "sexes": sexes,
        "selected": {
            "disease": disease_filter,
            "antigen": antigen_filter,
            "year": year_filter,
            "sex": sex_filter
        }
    })



#---------------------------------------------export----------------------------------------------------------------------
import csv
def export_records_csv(request):
    query = request.GET.get('q', '')
    disease_filter = request.GET.get('disease', '')
    antigen_filter = request.GET.get('antigen', '')
    year_filter = request.GET.get('year', '')
    sex_filter = request.GET.get('sex', '')

    records = ClinicalTrials.objects.all()

    if query:
        records = records.filter(
            Q(disease__icontains=query) |
            Q(disease_description__icontains=query) |
            Q(antigen__icontains=query) |
            Q(pubmed_id__icontains=query) |
            Q(clinical_trail_number__icontains=query) |
            Q(car_t_design__icontains=query)
        )

    if disease_filter:
        records = records.filter(disease=disease_filter)
    if antigen_filter:
        records = records.filter(antigen=antigen_filter)
    if year_filter:
        records = records.filter(year=year_filter)
    if sex_filter:
        records = records.filter(sex=sex_filter)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="CanImmDB_Search_Results.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Sequence', 'Disease', 'Disease Description', 'Patient ID',
        'Country', 'PubMed ID', 'Year', 'Title', 'Clinical Trial Number',
        'Sex', 'Age', 'Age Group', 'CAR T Design', 'Generation of CAR Receptor',
        'Vector', 'Antigen', 'Transfection Method', 'T Cell Source',
        'Inclusion Criteria', 'Exclusion Criteria', 'Best Response',
        'Partial Response', 'Stable Disease', 'Complete Response',
        'No Response', 'Progressive Disease', 'Median Survival',
        'Survival Post 6 Months', 'Previous Therapies'
    ])

    for trial in records:
        writer.writerow([
            trial.sequence,
            trial.disease,
            trial.disease_description,
            trial.patient_id,
            trial.country_name_of_clinical_trial,
            trial.pubmed_id,
            trial.year,
            trial.title_of_the_paper,
            trial.clinical_trail_number,
            trial.sex,
            trial.age,
            trial.age_group,
            trial.car_t_design,
            trial.generation_of_car_receptor,
            trial.vector,
            trial.antigen,
            trial.transfection_method,
            trial.origin_t_cell_sources,
            trial.patient_inclusion_criteria,
            trial.patient_exclusion_criteria,
            trial.best_response,
            trial.partial_response_for,
            trial.stable_disease,
            trial.complete_response_for_the_whole_group,
            trial.no_response,
            trial.progressive_disease_after_one_month,
            trial.median_overall_survival,
            trial.survival_post_6_months,
            trial.number_of_previous_therapies
        ])

    return response


#-------------------------------------------------conditional_search---------------------------------------------------------
from django.apps import apps

from .models import ClinicalTrials 


def get_clinical_trials_fields():
    """Fetch all field names of the ClinicalTrials model"""
    ClinicalTrials = apps.get_model('CanImmDB', 'ClinicalTrials')
    return [f.name for f in ClinicalTrials._meta.fields if f.name != "id"]




def conditional_search(request):
    records = None
    query_description = None

    if request.GET.getlist("filters[]") and request.GET.get("operator"):
        raw_filters = request.GET.getlist("filters[]")
        operator = request.GET.get("operator").upper()

        # Group filters as (field, value) pairs
        filter_pairs = list(zip(raw_filters[::2], raw_filters[1::2]))

        q_objects = []

        for field, value in filter_pairs:
            if field and value:
                kwargs = {f"{field}__icontains": value}
                q_objects.append(Q(**kwargs))

        if q_objects:
            if operator == "AND":
                query = q_objects[0]
                for q in q_objects[1:]:
                    query &= q
                records = ClinicalTrials.objects.filter(query)

            elif operator == "OR":
                query = q_objects[0]
                for q in q_objects[1:]:
                    query |= q
                records = ClinicalTrials.objects.filter(query)

            elif operator == "NOT":
                query = q_objects[0]
                for q in q_objects[1:]:
                    query |= q  
                records = ClinicalTrials.objects.exclude(query)

        query_description = f"{operator} search on: " + ", ".join(
            [f"{field} = {value}" for field, value in filter_pairs]
        )

    # Get all field names from model
    fields = [f.name for f in ClinicalTrials._meta.fields if f.name != "id"]

    return render(
        request,
        "conditional.html",  
        {
            "fields": fields,
            "records": records,
            "query": query_description,
        },
    )

#---------------------------------------------------BROWSE------------------------------------------------------


def browse_by_disease(request):
    disease = request.GET.get('disease')
    diseases = ClinicalTrials.objects.values_list('disease', flat=True).distinct()
    records = ClinicalTrials.objects.filter(disease__iexact=disease) if disease else None

    return render(request, 'browse_d.html', {
        'diseases': diseases,
        'records': records,
         'selected_disease': disease 
    })

#------------------------------------------------------------------------------------------------------------------------------------
def browse_by_agegrp(request):
    selected_age_group = request.GET.get('age_group')
    age_groups = ClinicalTrials.objects.values_list('age_group', flat=True).distinct()
    records = ClinicalTrials.objects.filter(age_group__iexact=selected_age_group) if selected_age_group else None

    return render(request, 'browse_agegrp.html', {
        'age_groups': age_groups,
        'selected_age_group': selected_age_group,
        'records': records
    })


#-----------------------------------------------------------------------------------------------------------------------------
def browse_by_country(request):
    country = request.GET.get('country_name_of_clinical_trial')
    countries = ClinicalTrials.objects.values_list('country_name_of_clinical_trial', flat=True).distinct()
    records = ClinicalTrials.objects.filter(country_name_of_clinical_trial__iexact=country) if country else None

    return render(request, 'browse_country.html', {
        'countries': countries,
        'records': records,
        'selected_country': country
    })



#-------------------------------------------------------------------------------------------------------------------------

def browse_by_vector(request):
    selected_vector = request.GET.get('vector')
    vectors = ClinicalTrials.objects.values_list('vector', flat=True).distinct()
    records = ClinicalTrials.objects.filter(vector__iexact=selected_vector) if selected_vector else None

    return render(request, 'browse_vector.html', {
        'vectors': vectors,
        'selected_vector': selected_vector,
        'records': records
    })
#-------------------------------------------------------------------------------------------------------------------------

def browse_by_antigen(request):
    selected_antigen = request.GET.get('antigen')
    antigens = ClinicalTrials.objects.values_list('antigen', flat=True).distinct()
    records = ClinicalTrials.objects.filter(antigen__iexact=selected_antigen) if selected_antigen else None

    return render(request, 'browse_antigen.html', {
        'antigens': antigens,
        'selected_antigen': selected_antigen,
        'records': records
    })


#--------------------------------------------------------EXPORT CSV----------------------------------------------------------

def export_disease_csv(request):
    disease = request.GET.get('disease')
    records = ClinicalTrials.objects.filter(disease__iexact=disease)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=\"disease_{disease}.csv\"'

    writer = csv.writer(response)
    writer.writerow([field.name for field in ClinicalTrials._meta.fields])
    for record in records:
        writer.writerow([getattr(record, field.name) for field in ClinicalTrials._meta.fields])

    return response


def export_agegrp_csv(request):
    age_group = request.GET.get('age_group')
    records = ClinicalTrials.objects.filter(age_group__iexact=age_group)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="agegroup_{age_group}.csv"'

    writer = csv.writer(response)
    writer.writerow([field.name for field in ClinicalTrials._meta.fields])
    for obj in records:
        writer.writerow([getattr(obj, field.name) for field in ClinicalTrials._meta.fields])

    return response

def export_country_csv(request):
    country = request.GET.get('country')
    records = ClinicalTrials.objects.filter(country__iexact=country)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="country_{country}.csv"'

    writer = csv.writer(response)
    writer.writerow([field.name for field in ClinicalTrials._meta.fields])
    for obj in records:
        writer.writerow([getattr(obj, field.name) for field in ClinicalTrials._meta.fields])

    return response

def export_vector_csv(request):
    vector = request.GET.get('vector')
    records = ClinicalTrials.objects.filter(vector__iexact=vector)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="vector_{vector}.csv"'

    writer = csv.writer(response)
    writer.writerow([field.name for field in ClinicalTrials._meta.fields])
    for obj in records:
        writer.writerow([getattr(obj, field.name) for field in ClinicalTrials._meta.fields])

    return response

def export_antigen_csv(request):
    antigen = request.GET.get('antigen')
    records = ClinicalTrials.objects.filter(antigen__iexact=antigen)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="antigen_{antigen}.csv"'

    writer = csv.writer(response)
    writer.writerow([field.name for field in ClinicalTrials._meta.fields])
    for obj in records:
        writer.writerow([getattr(obj, field.name) for field in ClinicalTrials._meta.fields])

    return response












































# from django.shortcuts import render
# from django.db.models import Q
# from .models import ClinicalTrials

# def search_records(request):
#     query = request.GET.get('q', '')
#     study_type = request.GET.get('study_type', '')
#     disease_filter = request.GET.get('disease', '')
#     antigen_filter = request.GET.get('antigen', '')
#     year_filter = request.GET.get('year', '')
#     sex_filter = request.GET.get('sex', '')

#     records = ClinicalTrials.objects.all()

#     # Apply keyword filter
#     if query:
#         records = records.filter(
#             Q(disease__icontains=query) |
#             Q(disease_description__icontains=query) |
#             Q(antigen__icontains=query) |
#             Q(pubmed_id__icontains=query) |
#             Q(clinical_trial_number__icontains=query) |
#             Q(car_t_design__icontains=query)
#         )

#     # Apply radio button filter
#     if study_type == "cell":
#         records = records.filter(t_cell_source__icontains='cell')
#     elif study_type == "animal":
#         records = records.filter(t_cell_source__icontains='animal')
#     elif study_type == "patient":
#         records = records.filter(patient_id__isnull=False)

#     # Apply dropdown filters
#     if disease_filter:
#         records = records.filter(disease=disease_filter)
#     if antigen_filter:
#         records = records.filter(antigen=antigen_filter)
#     if year_filter:
#         records = records.filter(year=year_filter)
#     if sex_filter:
#         records = records.filter(sex=sex_filter)

#     # Prepare dropdown values
#     diseases = ClinicalTrials.objects.exclude(disease__isnull=True).values_list('disease', flat=True).distinct().order_by('disease')
#     antigens = ClinicalTrials.objects.exclude(antigen__isnull=True).values_list('antigen', flat=True).distinct().order_by('antigen')
#     years = ClinicalTrials.objects.exclude(year__isnull=True).values_list('year', flat=True).distinct().order_by('year')
#     sexes = ClinicalTrials.objects.exclude(sex__isnull=True).values_list('sex', flat=True).distinct().order_by('sex')

#     return render(request, "search.html", {
#         "records": records,
#         "query": query,
#         "study_type": study_type,
#         "diseases": diseases,
#         "antigens": antigens,
#         "years": years,
#         "sexes": sexes,
#         "selected": {
#             "disease": disease_filter,
#             "antigen": antigen_filter,
#             "year": year_filter,
#             "sex": sex_filter
#         }
#     })



# import csv
# from django.http import HttpResponse

# def export_records_csv(request):
#     from .models import ClinicalTrials

#     # Apply same filters as search_records()
#     records =ClinicalTrials.objects.all()
#     query = request.GET.get('q', '')
#     study_type = request.GET.get('study_type', '')
#     disease_filter = request.GET.get('disease', '')
#     antigen_filter = request.GET.get('antigen', '')
#     year_filter = request.GET.get('year', '')
#     sex_filter = request.GET.get('sex', '')

#     if query:
#         records = records.filter(
#             Q(disease__icontains=query) |
#             Q(disease_description__icontains=query) |
#             Q(antigen__icontains=query) |
#             Q(pubmed_id__icontains=query) |
#             Q(clinical_trial_number__icontains=query) |
#             Q(car_t_design__icontains=query)
#         )

#     if study_type == "cell":
#         records = records.filter(t_cell_source__icontains='cell')
#     elif study_type == "animal":
#         records = records.filter(t_cell_source__icontains='animal')
#     elif study_type == "patient":
#         records = records.filter(patient_id__isnull=False)

#     if disease_filter:
#         records = records.filter(disease=disease_filter)
#     if antigen_filter:
#         records = records.filter(antigen=antigen_filter)
#     if year_filter:
#         records = records.filter(year=year_filter)
#     if sex_filter:
#         records = records.filter(sex=sex_filter)

#     # Create response with CSV
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="CanImmDB_filtered_records.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['ID', 'Disease', 'Patient ID', 'Antigen', 'Year', 'Trial Number'])  # Header row

#     for record in records:
#         writer.writerow([
#             record.id,
#             record.disease,
#             record.patient_id,
#             record.antigen,
#             record.year,
#             record.clinical_trial_number,
#         ])

#     return response


# # CONDITIONAL SEARCH---------------------------------------------------------------
# from django.shortcuts import render
# from django.db.models import Q
# from .models import ClinicalTrials

# def conditional_search(request):
#     query = request.GET.get('q', '')
#     filters = request.GET.getlist('filters[]')  # Get all filters from frontend
#     operator = request.GET.get('operator', 'AND')  # Default to AND operator
#     not_operator = request.GET.get('not_operator', False)  # NOT operator

#     # all records
#     records = ClinicalTrials.objects.all()

#     #  Q objects 
#     q_objects = Q()

#     for i in range(0, len(filters), 2):
#         if i + 1 < len(filters):
#             field = filters[i]
#             value = filters[i + 1]

#             if field == "animal":
#                 field = "t_cell_source"
#                 value = "animal"
#             elif field == "cell":
#                 field = "t_cell_source"
#                 value = "cell"
#             elif field == "patient":
#                 field = "patient_id"  

#             if field and value:
#                 # AND operator
#                 if operator == 'AND':
#                     q_objects &= Q(**{field: value})
#                 # OR operator
#                 elif operator == 'OR':
#                     q_objects |= Q(**{field: value})
#                 # NOT operator
#                 elif not_operator:
#                     q_objects &= ~Q(**{field: value})

#     # ilters with query
#     if query:
#         records = records.filter(q_objects & Q(disease__icontains=query))

#     records = records.filter(q_objects)  # dynamic filters

#     return render(request, 'conditional.html', {
#         'records': records,
#         'query': query,
#     })














# # from django.shortcuts import render
# # from .models import MoleculeClinicalRecord
# # from django.db.models import Q

# # def search_records(request):
# #     query = request.GET.get('q', '')
# #     study_type = request.GET.get('study_type', '')  

# #     records = MoleculeClinicalRecord.objects.all()

# #     if query:
# #         records = records.filter(
# #             Q(disease__icontains=query) |
# #             Q(disease_description__icontains=query) |
# #             Q(antigen__icontains=query) |
# #             Q(pubmed_id__icontains=query) |
# #             Q(clinical_trial_number__icontains=query) |
# #             Q(car_t_design__icontains=query)
# #         )

# #     if study_type == "cell":
# #         records = records.filter(t_cell_source__icontains='cell')
# #     elif study_type == "animal":
# #         records = records.filter(t_cell_source__icontains='animal')
# #     elif study_type == "patient":
# #         records = records.filter(patient_id__isnull=False)

# #     return render(request, "search.html", {
# #         "records": records,
# #         "query": query,
# #         "study_type": study_type
# #     })

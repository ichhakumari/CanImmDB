from django.contrib import admin
from .models import ClinicalTrials

admin.site.register(ClinicalTrials)













# from django.contrib import admin
# from .models import MoleculeClinicalRecord

# @admin.register(MoleculeClinicalRecord)
# class MoleculeClinicalRecordAdmin(admin.ModelAdmin):
#     list_display = ('id', 'disease', 'patient_id', 'year', 'antigen', 'car_t_design')
#     search_fields = ('disease', 'patient_id', 'clinical_trial_number', 'antigen', 'pubmed_id')
#     list_filter = ('disease', 'year', 'antigen', 'sex', 'country')

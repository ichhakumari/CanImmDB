from django.db import models

class ClinicalTrials(models.Model):
    sequence = models.IntegerField()
    disease = models.CharField(max_length=255)
    disease_description = models.TextField()
    paper_number_for_record = models.CharField(max_length=255)
    country_name_of_clinical_trial = models.CharField(max_length=255)
    pubmed_id = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    title_of_the_paper = models.CharField(max_length=255)
    clinical_trail_number = models.CharField(max_length=255)
    patient_id = models.CharField(max_length=255)
    sex = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    age_group = models.CharField(max_length=255)
    car_t_design = models.CharField(max_length=255)
    generation_of_car_receptor = models.CharField(max_length=255)
    vector = models.CharField(max_length=255)
    antigen = models.CharField(max_length=255)
    transfection_method = models.CharField(max_length=255)
    origin_t_cell_sources = models.CharField(max_length=255)
    patient_inclusion_criteria = models.CharField(max_length=255)
    patient_exclusion_criteria = models.CharField(max_length=255)
    best_response = models.CharField(max_length=255)
    partial_response_for = models.CharField(max_length=255)
    stable_disease = models.CharField(max_length=255)
    complete_response_for_the_whole_group = models.CharField(max_length=255)
    no_response = models.CharField(max_length=255)
    progressive_disease_after_one_month = models.CharField(max_length=255)
    median_overall_survival = models.CharField(max_length=255)
    survival_post_6_months = models.CharField(max_length=255)
    number_of_previous_therapies = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'clinical_trials'






# from django.db import models


# class MoleculeClinicalRecord(models.Model):
#     sequence = models.IntegerField()
#     disease = models.CharField(max_length=100)
#     disease_description = models.CharField(max_length=200, blank=True, null=True)
#     paper_number = models.IntegerField()
#     country = models.CharField(max_length=100, blank=True, null=True)
#     pubmed_id = models.CharField(max_length=30, blank=True, null=True)
#     year = models.IntegerField(blank=True, null=True)
#     paper_title = models.TextField(blank=True, null=True)
#     clinical_trial_number = models.CharField(max_length=100, blank=True, null=True)
#     patient_id = models.CharField(max_length=100, blank=True, null=True)
#     sex = models.CharField(max_length=10, blank=True, null=True)
#     age = models.FloatField(blank=True, null=True)
#     age_group = models.CharField(max_length=50, blank=True, null=True)
#     car_t_design = models.CharField(max_length=255, blank=True, null=True)
#     generation = models.CharField(max_length=100, blank=True, null=True)
#     vector = models.CharField(max_length=100, blank=True, null=True)
#     antigen = models.CharField(max_length=100, blank=True, null=True)
#     transfection_method = models.CharField(max_length=100, blank=True, null=True)
#     t_cell_source = models.CharField(max_length=100, blank=True, null=True)
#     inclusion_criteria = models.TextField(blank=True, null=True)
#     exclusion_criteria = models.TextField(blank=True, null=True)
#     best_response = models.CharField(max_length=100, blank=True, null=True)
#     partial_response = models.CharField(max_length=100, blank=True, null=True)
#     stable_disease = models.CharField(max_length=100, blank=True, null=True)
#     complete_response = models.CharField(max_length=100, blank=True, null=True)
#     no_response = models.CharField(max_length=100, blank=True, null=True)
#     progressive_disease = models.CharField(max_length=100, blank=True, null=True)
#     median_survival = models.CharField(max_length=100, blank=True, null=True)
#     survival_post_6_months = models.CharField(max_length=100, blank=True, null=True)
#     previous_therapies = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return f"{self.disease} | {self.patient_id or 'No ID'}"

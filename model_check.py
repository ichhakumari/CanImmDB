# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ClinicalTrials(models.Model):
    id = models.BigAutoField(primary_key=True)
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

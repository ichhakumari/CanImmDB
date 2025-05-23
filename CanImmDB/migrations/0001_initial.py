# Generated by Django 5.2 on 2025-04-09 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MoleculeClinicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.IntegerField()),
                ('disease', models.CharField(max_length=100)),
                ('disease_description', models.CharField(blank=True, max_length=200, null=True)),
                ('paper_number', models.IntegerField()),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('pubmed_id', models.CharField(blank=True, max_length=30, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('paper_title', models.TextField(blank=True, null=True)),
                ('clinical_trial_number', models.CharField(blank=True, max_length=100, null=True)),
                ('patient_id', models.CharField(blank=True, max_length=100, null=True)),
                ('sex', models.CharField(blank=True, max_length=10, null=True)),
                ('age', models.FloatField(blank=True, null=True)),
                ('age_group', models.CharField(blank=True, max_length=50, null=True)),
                ('car_t_design', models.CharField(blank=True, max_length=255, null=True)),
                ('generation', models.CharField(blank=True, max_length=100, null=True)),
                ('vector', models.CharField(blank=True, max_length=100, null=True)),
                ('antigen', models.CharField(blank=True, max_length=100, null=True)),
                ('transfection_method', models.CharField(blank=True, max_length=100, null=True)),
                ('t_cell_source', models.CharField(blank=True, max_length=100, null=True)),
                ('inclusion_criteria', models.TextField(blank=True, null=True)),
                ('exclusion_criteria', models.TextField(blank=True, null=True)),
                ('best_response', models.CharField(blank=True, max_length=100, null=True)),
                ('partial_response', models.CharField(blank=True, max_length=100, null=True)),
                ('stable_disease', models.CharField(blank=True, max_length=100, null=True)),
                ('complete_response', models.CharField(blank=True, max_length=100, null=True)),
                ('no_response', models.CharField(blank=True, max_length=100, null=True)),
                ('progressive_disease', models.CharField(blank=True, max_length=100, null=True)),
                ('median_survival', models.CharField(blank=True, max_length=100, null=True)),
                ('survival_post_6_months', models.CharField(blank=True, max_length=100, null=True)),
                ('previous_therapies', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]

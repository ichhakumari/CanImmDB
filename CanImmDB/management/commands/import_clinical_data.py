import pandas as pd
from django.core.management.base import BaseCommand
from CanImmDB.models import MoleculeClinicalRecord

class Command(BaseCommand):
    help = 'Import clinical data from Excel into MoleculeClinicalRecord model'

    def handle(self, *args, **kwargs):
        file_path = 'data/Database_ContentIupdated.xlsx_jan.xlsx'  

        df = pd.read_excel(file_path)
        df.columns = [col.strip().replace('\n', ' ').replace('  ', ' ').strip() for col in df.columns]

        count = 0

        for _, row in df.iterrows():
            try:
                MoleculeClinicalRecord.objects.create(
                    sequence=row['Sequence'],
                    disease=row['Disease'],
                    disease_description=row.get('Disease_Description'),
                    paper_number=row['Paper number for record'],
                    country=row.get('Country name of clinical trial'),
                    pubmed_id=row.get('Pubmed ID'),
                    year=row.get('Year'),
                    paper_title=row.get('Title of the paper'),
                    clinical_trial_number=row.get('Clinical trial Number'),
                    patient_id=row.get('Patient number/patient ID'),
                    sex=row.get('Sex'),
                    age=row.get('Age'),
                    age_group=row.get('Age group'),
                    car_t_design=row.get('CAR T design'),
                    generation=row.get('Generation of car receptor'),
                    vector=row.get('Vector'),
                    antigen=row.get('Antigen'),
                    transfection_method=row.get('Transfection method'),
                    t_cell_source=row.get('Original T cell Sources'),
                    inclusion_criteria=row.get('Patient inclusion criteria'),
                    exclusion_criteria=row.get('Patient exclusion criteria'),
                    best_response=row.get('best reponse'),
                    partial_response=row.get('PARTIAL RESPONSE for whole study'),
                    stable_disease=row.get('STABLE DISEASE'),
                    complete_response=row.get('complete response for the whole group'),
                    no_response=row.get('NO RESPONSE'),
                    progressive_disease=row.get('Progressive disease after one month'),
                    median_survival=row.get('median overall survival'),
                    survival_post_6_months=row.get('SURVIVAL POST 6 MONTHS for whole group'),
                    previous_therapies=row.get('number of previous therapies'),
                )
                count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Skipped row due to error: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Imported {count} records successfully!"))

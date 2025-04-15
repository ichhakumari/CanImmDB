"""
URL configuration for db_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from CanImmDB.views import search_records , export_records_csv , conditional_search, main ,browse_by_disease, browse_by_agegrp, browse_by_antigen,browse_by_country,browse_by_vector ,export_agegrp_csv
from django.shortcuts import redirect
from CanImmDB.views import export_country_csv , export_vector_csv ,export_antigen_csv, export_disease_csv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',main, name='main'),
    path('search/', search_records, name='search_records'),
    path('export/', export_records_csv, name='export_records_csv'),
    path('conditional/', conditional_search, name='conditional_search'),
    path("browse/agegrp/",browse_by_agegrp, name="browse_by_agegrp"),

    path("browse/country/", browse_by_country, name="browse_by_country"),
    path("browse/vector/", browse_by_vector, name="browse_by_vector"),
    path("browse/antigen/", browse_by_antigen, name="browse_by_antigen"),
    path("browse/disease/", browse_by_disease, name="browse_by_disease"),
 



    path("browse/disease/export/", export_disease_csv, name="export_disease_csv"),

    path("browse/agegrp/export/", export_agegrp_csv, name="export_agegrp_csv"),
    path("browse/country/export/", export_country_csv, name="export_country_csv"),
    path("browse/vector/export/", export_vector_csv, name="export_vector_csv"),
    path("browse/antigen/export/", export_antigen_csv, name="export_antigen_csv"),


]

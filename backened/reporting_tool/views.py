import mimetypes
import os, shutil
import pandas as pd
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, permissions
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from .models import ExcludedClient, Reports, RawCsvFile
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from .serializers import ExcludedClientSerializer, ReportsSerializer, RawCsvFileSerializer


class ExcludedClientViewSet(viewsets.ModelViewSet):
    """
    An endpoint to view, update and delete an excluded client.
    """

    queryset = ExcludedClient.objects.all().order_by('name')
    serializer_class = ExcludedClientSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'clientparam1',
                openapi.IN_QUERY,
                description="To view clients",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReportViewSet(viewsets.ModelViewSet):
    """
    an endpoint to view the save report files
    """
    queryset = Reports.objects.all().order_by('-date_created')
    authentication_classes = [SessionAuthentication]
    serializer_class = ReportsSerializer
    permission_classes = [permissions.IsAuthenticated]


class RawCsvFileViewSet(viewsets.ModelViewSet):
    queryset = RawCsvFile.objects.all().order_by('-date_created')
    # authentication_classes = [SessionAuthentication]
    serializer_class = RawCsvFileSerializer
    # permission_classes = [permissions.IsAuthenticated]


@api_view()
def process_csv(request):
    """
    Filters, sorts, process and downloads the file in the needed format
    """
    excluded_clients = ExcludedClient.objects.values_list('name', flat=True)
    """
    filter for the given column parameters from the uploaded file
    """
    try:
        csv_file = RawCsvFile.objects.all().last()
        specific_file_name = csv_file.file.name.split('/')[1]

        df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, str(csv_file.file)))[
            ['staff', 'client', 'sched start', 'sched end', 'clocked start']
        ]

        df.drop_duplicates(inplace=True)
 
        if not os.path.exists('csv_files'):
            os.makedirs('csv_files')

        df.to_csv(os.path.join('csv_files', specific_file_name), index=False)
        """
           sort the cvs file contents by staff name, and filter out the clients with the 
           excluded client list
        """
        final_file_name = 'filtered_' + specific_file_name
     
        filtered_df = df[~df['client'].isin(excluded_clients)]
        
        sorted_df = filtered_df.sort_values(by='staff')
        
        if not os.path.exists('processed_csv_files'):
            os.makedirs('processed_csv_files')
        sorted_df.to_csv(os.path.join('processed_csv_files', final_file_name), index=False)
        processed_file_path = os.path.join('processed_csv_files', final_file_name)
        """
        Download the the processed file 
        """
        fl = open(processed_file_path, 'r')
      
        mime_type, _ = mimetypes.guess_type(final_file_name)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % final_file_name
        
        return response
    except Exception as e:
        return Response('Error processing the file or The file doesnt exists')


@api_view()
def delete_directory(request):
    """
    Deletes the processed directory after 5 seconds the file is downloaded
    """
    dir_path = os.path.join('processed_csv_files')
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
        return Response('Directory deleted')
    return Response('Error Deleting the directory')

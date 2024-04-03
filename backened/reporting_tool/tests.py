# import os
# from django.test import TestCase
# from .models import ExcludedClient, Reports, RawCsvFile
# from .serializers import ExcludedClientSerializer, ReportsSerializer, RawCsvFileSerializer
# from .views import process_csv, delete_directory
#
#
# class ExcludedClientViewSetTests(TestCase):
#
#     def setUp(self):
#         ExcludedClient.objects.create(name="Client 1")
#         ExcludedClient.objects.create(name="Client 2")
#
#     def test_list_excluded_clients(self):
#         response = self.client.get('http://127.0.0.2:8000/reporting/excluded_clients/')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Client 1', response.content.decode())
#         self.assertIn('Client 2', response.content.decode())
#
#     def test_create_excluded_client(self):
#         data = {'name': 'Client 3'}
#         response = self.client.post('/api/excluded_clients/', data)
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(ExcludedClient.objects.count(), 3)
#
#     def test_update_excluded_client(self):
#         excluded_client = ExcludedClient.objects.first()
#         data = {'name': 'Updated Client Name'}
#         response = self.client.put('/api/excluded_clients/1/', data)
#         self.assertEqual(response.status_code, 200)
#         excluded_client.refresh_from_db()
#         self.assertEqual(excluded_client.name, 'Updated Client Name')
#
#     def test_delete_excluded_client(self):
#         excluded_client = ExcludedClient.objects.first()
#         response = self.client.delete('/api/excluded_clients/1/')
#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(ExcludedClient.objects.count(), 1)
#
#
# # class ReportViewSetTests(TestCase):
# #
# #     def setUp(self):
# #         Reports.objects.create(date_created="2023-12-03", file="report.csv")
# #
# #     def test_list_reports(self):
# #         response = self.client.get('/api/reports/')
# #         self.assertEqual(response.status_code, 200)
# #         self.assertIn('report.csv', response.content.decode())
# #
# #     def test_retrieve_report(self):
# #         response = self.client.get('/api/reports/1/')
# #         self.assertEqual(response.status_code, 200)
# #         self.assertIn('report.csv', response.content.decode())
# #
# #
# # class RawCsvFileViewSetTests(TestCase):
# #
# #     def setUp(self):
# #         RawCsvFile.objects.create(file="raw_data.csv")
# #
# #     def test_list_raw_csv_files(self):
# #         response = self.client.get('/api/raw_csv_files/')
# #         self.assertEqual(response.status_code, 200)
# #         self.assertIn('raw_data.csv', response.content.decode())
# #
# #     def test_retrieve_raw_csv_file(self):
# #         response = self.client.get('/api/raw_csv_files/1/')
# #         self.assertEqual(response.status_code, 200)
# #         self.assertIn('raw_data.csv', response.content.decode())
# #
# #
# # class ProcessCSVTests(TestCase):
# #
# #     def setUp(self):
# #         RawCsvFile.objects.create(file=open('data.csv', 'rb'))
# #
# #     def test_process_csv(self):
# #         request = self.request_factory.get('/')
# #         response = process_csv(request)
# #         self.assertEqual(response.status_code, 200)
# #
# #
# # class DeleteDirectoryTests(TestCase):
# #
# #     def setUp(self):
# #         os.makedirs('processed_csv_files')
# #
# #     def test_delete_directory(self):
# #         request = self.request_factory.get('/')
# #         response = delete_directory(request)
# #         self.assertEqual(response.status_code, 200)

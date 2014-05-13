from apiclient import KavaApi

api = KavaApi(username='', password='')

print api.add_project({
    'name': "api test",
    'company': 'Test',
})
print api.get_projects(company='42cc')
print api.get_project('api-test')

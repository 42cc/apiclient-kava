import apiclient

api = apiclient.KavaApi(username='', password='')


print api.get_projects(company='42cc')
print api.get_project('kavyarnya')

cc = api.get_company('42cc')
# print cc.add_project({'name': 'new test'})
print cc.projects()
print cc.project('kavyarnya')

import kavahq

api = kavahq.KavaApi(username='', password='', kava_url='http://127.0.0.1:8000/api/')


print api.get_projects(company='42cc')
print api.get_project('kavyarnya')

cc = api.get_company('42cc')
# print cc.add_project({'name': 'new test'})
print cc.projects()
print cc.project('kavyarnya')

=====================
KavaHQ.com API client
=====================



Usage
=====

.. code-block:: python

	import kavahq
	import keyring
	import getpass

	SERVICE = 'kavahq-api'
	username = 'imposeren'
	password = keyring.get_password(SERVICE, username)
	if password is None:
	    password = getpass.getpass()
	    keyring.set_password(SERVICE, username, password)

	api = kavahq.KavaApi(username=username, password=password)

	print api.get_projects(company='42-coffee-cups')
	>>> [{u'coordinator_id': None, u'name': u'test', u'is_active': False, u'deadline': None, u'detail_url': u'/api/project/test/', u'slug': u'test', u'budget_limit': 0.0},

	print api.get_project('kavyarnya')
	>>> {u'days_num_bugs_showing': 7, u'coordinator_id': 1, u'name': u'Kavyarnya', u'last_required_budget': u'1', u'is_active': True, u'deadline': u'1970-01-01', u'last_completion_date': u'1970-01-01', u'bugs_count': 0, u'slug': u'kavyarnya', u'budget_limit': 42}

	cc = api.get_company('42-coffee-cups')
	# print cc.add_project({'name': 'new test'})
	print cc.projects()
	print cc.project('kavyarnya')

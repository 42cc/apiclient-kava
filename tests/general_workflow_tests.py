# -*- coding: utf-8 -*-

import mock
import unittest2
import urlparse


class GeneralWorkflowTest(unittest2.TestCase):
    def setUp(self):
        super(GeneralWorkflowTest, self).setUp()

    @mock.patch('kavahq.api.requests')
    def test_projects(self, requests):
        from kavahq.api import KavaApi
        api = KavaApi(
            username='user', password='password', company_name='42 coffee cups',
        )
        project_slug = '42-jobs'
        project_api = api.projects.get(project_slug=project_slug)
        requests.get.assert_called_with(
            urlparse.urljoin(api.base_url, 'project/'),
            {'project_slug': project_slug}
        )
        project_api.estimate
        requests.get.assert_called_with(
            urlparse.urljoin(api.base_url, 'project/estimate/'),
            {'project_slug': project_slug}
        )
        project_api.properties
        requests.get.assert_called_with(
            urlparse.urljoin(api.base_url, 'project/properties/'),
            {'project_slug': project_slug}
        )
        project_api.tickets
        requests.get.assert_called_with(
            urlparse.urljoin(api.base_url, 'project/tickets/'),
            {'project_slug': project_slug}
        )

        all_projects_api = api.projects.get()
        requests.get.assert_called_with(
            urlparse.urljoin(api.base_url, 'project/'),
        )
        project_api_same = all_projects_api.get(project_slug=project_slug)
        self.assertEqual(project_api, project_api_same)

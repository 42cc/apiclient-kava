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
        company_name = '42 coffee cups'
        api = KavaApi(
            username='user', password='password', company_name=company_name,
        )
        auth = ('user', 'password')
        project_slug = '42-jobs'
        project_api = api.projects.get(project_slug)

        project_api.response
        requests.get.assert_called_with(
            urlparse.urljoin(api.base_url, 'project/%s/' % project_slug),
            params={'project_slug': project_slug},
            auth=auth,
        )

        project_api.estimate.response
        requests.get.assert_called_with(
            urlparse.urljoin(api.base_url, 'project/estimate/'),
            params={
                'project_slug': project_slug,
                'company': company_name,
            }
        )

        project_api.properties.response
        requests.post.assert_called_with(
            urlparse.urljoin(api.base_url, 'project/properties/'),
            data={
                'project_slug': project_slug,
                'company': company_name,
            },
            auth=auth,
        )

        project_api.tickets.response
        requests.post.assert_called_with(
            urlparse.urljoin(api.base_url, 'project/tickets/'),
            data={
                'project_slug': project_slug,
                'company': company_name,
            },
            auth=auth,
        )

        api.projects.response
        requests.get.assert_called_with(
            urlparse.urljoin(api.base_url, 'project/'),
            params={},
            auth=auth,
        )

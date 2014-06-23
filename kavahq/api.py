# -*- coding: utf-8 -*-
import os
import urlparse

# thirdparty:
import requests


class ApiObject(object):
    def __init__(self, path, api, data=None):
        self.internaluse_path = path
        self.internaluse_api = api
        self.internaluse_data = data or {}
        self._response = None
        return

    def __getattr__(self, name):
        if not name.endswith('/'):
            name = name + '/'
        is_project_details = (
            self.internaluse_path not in self.internaluse_api.ALLOWED_PATHS and
            self.internaluse_path.startswith('project/')
        )
        if is_project_details:
            subpath = os.path.join('project/', name)
        else:
            subpath = os.path.join(self.internaluse_path, name)
        return ApiObject(subpath, self.internaluse_api, self.internaluse_data)

    def __getitem__(self, key):
        return self.response[key]

    def __unicode__(self):
        return u"<ApiObject '{self.internaluse_path}'?{self.internaluse_data} >".format(self=self)

    def __repr__(self):
        return str(self.__unicode__())

    def __eq__(self, other):
        return (
            self.internaluse_path == other.internaluse_path and
            self.internaluse_data == other.internaluse_data
        )

    def __iter__(self):
        # allows to run dict(api_object_instance)
        for key in self.response.iterkeys():
            yield self.response[key]

    def __hash__(self):
        # this will allow to use ApiObject instances as dict keys
        return (self.internaluse_path, self._method, self.internaluse_data_hash).__hash__()

    def get(self, subpath=None, **kwargs):
        new_data = dict(self.internaluse_data)
        new_data.update(kwargs)

        # special handling for projects
        if subpath and self.internaluse_path == 'project/':
            new_data['project_slug'] = subpath

        path = self.internaluse_path
        if subpath:
            if not subpath.endswith('/'):
                subpath = subpath + '/'
            path = os.path.join(path, subpath)

        return ApiObject(path, self.internaluse_api, new_data)

    @property
    def response(self):
        if self._response is None:
            self._response = self.internaluse_api._make_request(self.internaluse_path, self.internaluse_data)
        return self._response

    def _data_hash(self):
        keys = tuple(sorted(self.internaluse_data.keys()))
        values = tuple([self.internaluse_data[key] for key in keys])
        return tuple(keys, values).__hash__()


class KavaApi(object):

    ALLOWED_PATHS = {
        'project/add/': {
            'method': 'post',
            'accepts_company': True,
            'auth': 'basic',
            },
        'project/add/': {
            'method': 'post',
            'accepts_company': True,
            'auth': 'basic',
            },
        'project/edit/': {
            'method': 'post',
            'accepts_company': True,
            'auth': 'basic',
            },
        'project/tickets/': {
            'method': 'post',  # orly? maybe should change api to GET?
            'accepts_company': True,
            'auth': 'basic',
            },
        'project/tickets/count/': {
            'method': 'get',
            'accepts_company': True,
            'auth': 'api_key',
            },
        'project/estimate/': {
            'method': 'get',
            'accepts_company': True,
            'auth': 'api_key',
            },
        'project/properties/': {
            'method': 'post',  # orly? maybe should change api to GET?
            'accepts_company': True,
            'auth': 'basic',
            },

    }

    def __init__(
            self,
            username,
            password,
            api_key=None,
            base_url='https://kavahq.com/api/',
            company_name=None):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.internaluse_api_key = api_key
        self.company_name = company_name
        self.__root_api = ApiObject('', self)

    def __getattr__(self, name):
        if name == 'projects':  # just to be more meaningful
            name = 'project'
        return getattr(self.__root_api, name)

    def get_api_key(self):
        pass

    def _make_request(self, resource_uri, data=None):
        url = urlparse.urljoin(self.base_url, resource_uri)
        data = data or {}
        data = dict(data)
        method = self.ALLOWED_PATHS.get(resource_uri, {}).get('method', 'get')

        if method == 'get':
            data_key = 'params'
        elif method == 'post':
            data_key = 'data'
        requests_method = getattr(requests, method)

        accepts_company = self.ALLOWED_PATHS.get(resource_uri, {}).get('accepts_company')

        if accepts_company and not 'company' in data:
            data['company'] = self.company_name

        requires_api_key = self.ALLOWED_PATHS.get(resource_uri, {}).get('auth') == 'api_key'

        requests_method_kwargs = {data_key: data}

        if requires_api_key and not self.internaluse_api_key:
            self.get_api_key()
        else:
            requests_method_kwargs['auth'] = (self.username, self.password)

        return requests_method(url, **requests_method_kwargs).json()

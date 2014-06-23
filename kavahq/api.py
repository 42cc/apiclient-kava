# -*- coding: utf-8 -*-
import requests
import urlparse


class ApiObject(object):
    def __init__(self, path, api, post_or_filters=None):
        self._path = path
        self._api = api
        self._filters = {}
        self._data = None
        self._method = api.ALLOWED_PATHS[path]['method']
        self._post_or_filters = post_or_filters or {}

        if self._method == 'post':
            self.data
        return

    def __getattr__(self, name):
        subpath = os.path.join(self._path, name)
        if subpath in self._api.ALLOWED_PATHS:
            return ApiObject(subpath, self._api)
        else:
            raise AttributeError

    @property
    def data(self):
        if self._data is None:
            if self._method == 'get':
                self._data = self.api.get()
            elif self._method == 'post':
                self._data = self.api.post()
        return self._data

    def post(self, **post_data):
        full_post_data = dict(self._post_or_filters)
        full_post_data.update(post_data)
        self.api._make_request(self._path, full_post_data)

    def get(self, **filters):
        full_filters = dict(self._post_or_filters)
        full_filters.update(filters)
        return self.api._make_request(self._path, full_filters, force_get=True)

    def __unicode__(self):
        return u"<ApiObject '{self.path}': {self.data} >".format(self=self)

    def _data_hash(self):
        keys = tuple(sorted(self._data.keys()))
        values = tuple([self._data[key] for key in keys])
        return tuple(keys, values).__hash__()

    def __eq__(self, other):
        return (
            self._path == other._path and
            self._data == other._data and
            self._method == other._method
        )

    def __hash__(self):
        # this will allow to use ApiObject instances as dict keys
        return (self._path, self._method, self._data_hash).__hash__()


class KavaApi(object):

    ALLOWED_PATHS = {
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
        self.api_key = api_key
        self.company_name = company_name

    def _make_request(self, resource_uri, data=None, method='get'):
        url = urlparse.urljoin(self.base_url, resource_uri)
        data = data or {}
        data = dict(data)
        requests_method = getattr(requests, method)

        accepts_company = self.ALLOWED_PATHS.get(resource_uri, {}).get('accepts_company')

        if accepts_company and not 'company' in data:
            data['company'] = self.company_name

        requires_api_key = self.ALLOWED_PATHS.get(resource_uri, {}).get('auth') == 'api_key'

        if requires_api_key and not self._api_key:
            self.get_api_key()

        requests_method(url, data)

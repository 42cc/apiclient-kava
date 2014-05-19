import urllib
import urllib2
import base64
import json


API_SETTINGS = {
    'kava_url': 'http://127.0.0.1:8000/api/',
    'username': '',
    'password': '',
}


class KavaApi(object):

    class ApiError(Exception):
        pass

    class UnauthorizedError(ApiError):
        pass

    def __init__(self, *args, **kwargs):
        self.settings = dict(API_SETTINGS)
        self.settings.update(kwargs)

    def get_projects(self, **kwargs):
        filters = kwargs
        return self._make_request('project/', filters, force_get=True)['projects']

    def get_project(self, project_slug):
        return self._make_request('project/%s' % project_slug)

    def add_project(self, data):
        return self._make_request('project/add/', data)

    def _make_request(self, resource_uri, post_data=None, force_get=False):
        """
        This method is used to make GET and POST requests to API
        with BaseAuth and handling api errors.

        Params:
        post_data - dict to send in POST or GET
        force_get - if True, than post_data will be sended in query-string

        Returns:
        If request was success - returns data under 'message' key in response.
        """

        post_data_str = None
        if post_data:
            post_data_str = urllib.urlencode(post_data)

        request_url = '%s%s' % (
            self.settings['kava_url'], resource_uri)

        if post_data_str and force_get:
            request = urllib2.Request(request_url + '?%s' % post_data_str)
        else:
            request = urllib2.Request(request_url, data=post_data_str)

        user_pass_string = '%s:%s' % (self.settings['username'],
                                      self.settings['password'])

        base64string = base64.standard_b64encode(user_pass_string)
        request.add_header("Authorization", "Basic %s" % base64string)

        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            if e.code == 401:
                raise self.UnauthorizedError(e.read())
            elif e.code == 400:
                content = e.read()
                error_msg = content
                try:
                    resp_message = json.loads(content)['message']
                except:
                    pass
                else:
                    if 'errors' in resp_message:
                        error_msg = resp_message['errors']

                raise self.ApiError(error_msg)
            else:
                raise

        resp_data = response.read()
        response.close()

        api_resp = json.loads(resp_data)
        result_data = api_resp['message']
        result_code = api_resp['code']

        # Return data
        return result_data

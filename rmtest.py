import requests
import requests_mock


def get_session():
    adapter = requests_mock.Adapter()
    session = requests.Session()
    session.mount('mock', adapter)
    return [adapter, session]


class APIClient(object):
    def __init__(self, url, session=None):
        self.url = url

        if session is None:
            session = requests.Session()

        self.session = session

    def get(self, resource, identifier=None, **kwargs):
        url = "%s/%s" % (self.url, resource)

        if identifier:
            url = "%s/%s/%s" % (self.url, resource, identifier)

        r = self.session.get(url, params=kwargs)
        return r.json()


class TestAPIClient(object):
    def test_qs(self):
        adapter, session = get_session()
        adapter.register_uri('GET', 'mock://test.api.com/things', text='{"foo": "bar"}')

        api = APIClient('mock://test.api.com', session=session)
        response = api.get('things', foo='bar', bar='baz')

        assert response == {'foo': 'bar'}
        assert len(adapter.request_history) == 1
        assert adapter.request_history[0].url == 'mock://test.api.com/things'
        assert adapter.request_history[0].qs == {
            'foo': 'bar',
            'bar': 'baz'
        }

    def test_qs_in_url(self):
        adapter, session = get_session()
        adapter.register_uri('GET', 'mock://test.api.com/things?foo=bar&bar=baz', text='{"foo": "bar"}')

        api = APIClient('mock://test.api.com', session=session)
        response = api.get('things', foo='bar', bar='baz')

        assert response == {'foo': 'bar'}
        assert len(adapter.request_history) == 1
        assert adapter.request_history[0].url == 'mock://test.api.com/things'
        assert adapter.request_history[0].qs == {
            'foo': 'bar',
            'bar': 'baz'
        }

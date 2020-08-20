import json
import logging
import os
import requests
from time import sleep

from sss_beneficiarios_hospitales.parser import SSSParser

logger = logging.getLogger(__name__)


class DataBeneficiariosSSSHospital:
    """ Consultas al Padrón de Beneficiarios de los Agentes 
        Nacionales del Seguro de Salud. Requiere credenciales 
        de Hospital habilitado. """
    
    def __init__(self, user, password, headers=None):
        self.user = user
        self.password = password
        self.session = requests.session()
        self.verify_ssl = False
        self.login_url = 'https://seguro.sssalud.gob.ar/login.php?b_publica=Acceso+Restringido+para+Hospitales&opc=bus650&user=HPGD'
        self.logged_in = False
        self.query_url = 'https://seguro.sssalud.gob.ar/indexss.php?opc=bus650&user=HPGD&cat=consultas'
        logger.debug('DBH started')
        self.pause_before_requests = 2
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
            }
        if headers is not None:
            default_headers.update(headers)
        
        self.session.headers.update(default_headers)
        self.debug = False
        self.fake_env = user == 'FAKE' and password == 'FAKE'

    def login(self):

        if self.fake_env:
            self.logged_in = True
            return True

        params = {
            '_user_name_': self.user,
            '_pass_word_': self.password,
            'submitbtn': 'Ingresar'
        }
        
        sleep(self.pause_before_requests)

        ret = self._request(self.login_url, params=params)
        if ret['ok']:
            self.login_response = ret['response']
        else:
            raise Exception('Unable to login to SSS page. {}'.format(ret['error']))

        self._save_response('login', self.login_response)
        self.logged_in = self._validate_logged_in()
        if not self.logged_in:
            logger.error('Failed to log in {}'.format(self.login_response.status_code))
        else:
            logger.info('Logged in')
        
        return self.logged_in

    def query(self, dni):
        logger.info('DBH query')
        if not self.logged_in:
            self.login()
        if not self.logged_in:
            return {'ok': False, 'error': 'Unable to login'}
        
        params = {
            'pagina_consulta': '',
            'cuil_b': '',
            'nro_doc': dni,
            'B1': 'Consultar'
        }
        sleep(self.pause_before_requests)

        ret = self._request(self.query_url, params=params)
        if ret['ok']:
            self.query_response = ret['response']
        else:
            raise Exception('Unable to Query from SSS page. {}'.format(ret['error']))

        logger.info('Query {}'.format(self.query_response.status_code))

        self._save_response('query', self.query_response)
        if self.fake_env:
            # DNI should be a file in html-samples folder e.g. "full-afiliado"
            html = get_html_sample(dni)
            # dejar un valor predeterminado
            if not os.path.isfile(html):
                html = get_html_sample('full-afiliado')
        else:
            html = self.query_response.text
        self.parser = SSSParser(html)
        self.parser.debug = self.debug
        data = self.parser.get_all_data()
        
        return {'ok': True, 'resultados': data}

    def _save_response(self, filename, resp):
        if self.fake_env:
            return

        f = open(f'{filename}.html', 'w')
        f.write(resp.text)
        f.close()

        data = {
            'headers': dict(resp.headers),
            'cookies': resp.cookies.get_dict(),
            'encoding': resp.encoding,
            'status_code': resp.status_code
            }

        str_data = json.dumps(data, indent=4)

        f = open(f'{filename}.json', 'w')
        f.write(str_data)
        f.close()

    def _validate_logged_in(self):
        """ validate login worked fine """
        ok1 = 'usuario_logueado' in self.login_response.text
        ok2 = 'nro_doc' in self.login_response.text
        return ok1 and ok2
    
    def _request(self, url, method='POST', params={}):

        ret = {'ok': True}
        if self.fake_env:
            class FakeResponse:
                status_code = 0
            ret['response'] = FakeResponse()
            return ret

        if method == 'GET':
            try:
                res = self.session.get(url, verify=self.verify_ssl)
            except Exception as e:
                ret['ok'] = False
                error = f'Error requesting {method} {url}: {e}'

        elif method == 'POST':
            try:
                res = self.session.post(url, data=params, verify=self.verify_ssl)
            except Exception as e:
                ret['ok'] = False
                error = f'Error requesting {method} {url}: {e}'

        else:
            error = f'Invalid method {method}'
            ret['ok'] = False
        
        if ret['ok']:
            ret['response'] = res
        else:
            logger.error(error)
            ret['error'] = error
        
        return ret


def get_html_sample(sample_name):
    samples_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html-samples')
    path = os.path.join(samples_folder, '{}.html'.format(sample_name))
    return path
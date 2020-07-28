import logging
import requests


logger = logging.getLogger(__name__)


class DataBeneficiariosSSSHospital:
    """ Consultas al Padrón de Beneficiarios de los Agentes 
        Nacionales del Seguro de Salud. Requiere credenciales 
        de Hospital habilitado. """
    
    def __init__(self, user, password, headers=None):
        self.user = user
        self.password = password
        self.session = requests.Session()
        self.login_url = 'https://seguro.sssalud.gob.ar/login.php?b_publica=Acceso+Restringido+para+Hospitales&opc=bus650&user=HPGD'
        # self.login_url = 'https://seguro.sssalud.gob.ar/login.php?b_publica=Acceso+Restringido+para+Hospitales&amp;opc=bus650&amp;user=HPGD'
        self.logged_in = False
        self.query_url = 'https://seguro.sssalud.gob.ar/indexss.php?opc=bus650&user=HPGD&cat=consultas'
        logger.debug('DBH started')

        default_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
            }
        if headers is not None:
            default_headers.update(headers)
        
        self.session.headers.update(default_headers)

    def login(self):
        params = {
            '_user_name_': self.user,
            '_pass_word_': self.password,
        }
        
        self.login_response = self.session.post(self.login_url, data=params, verify=False)

        f = open('login.html', 'w')
        f.write(self.login_response.text)
        f.close()

        self.logged_in = self._validate_logged_in()
        if not self.logged_in:
            logger.error('Failed to log in {}'.format(self.login_response.status_code))
        else:
            logger.info('Logged in')
        
        return self.logged_in
        
    def _validate_logged_in(self):
        """ validate login worked fine """
        txt = '<input type="text" class="form-control" name="nro_doc" maxlength="13">'
        return txt in self.login_response.text

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
        self.query_response = self.session.post(self.query_url, data=params, verify=False)
        logger.info('Query {}'.format(self.query_response.status_code))

        f = open('query.html', 'w')
        f.write(self.query_response.text)
        f.close()

        return {'ok': False, 'error': 'Error parsing HTML'}
        

        

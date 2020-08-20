import logging
import os
import re
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class SSSParser:
    def __init__(self, html):
        """ html is text or a file path """
        logger.info('Start parser for {}'.format(html[:80]))
        self.path = None
        if os.path.isfile(html):
            self.path = html
            html = self._open_file(html)
        self.raw_html = html
        self.soup = BeautifulSoup(html, 'html5lib')

        self.keys = {
            'hay_afiliacion_vigente': 'DATOS DE AFILIACION VIGENTE',
            'no_hay_afiliacion_vigente': 'No se reportan datos para el NUMERO DE DOCUMENTO',
        }
        self.debug = False

    def get_all_data(self):
        s_tables = self.soup.find_all('table')
        
        hay_afiliacion = self.keys['hay_afiliacion_vigente'] in self.raw_html
        no_hay_afiliacion = self.keys['no_hay_afiliacion_vigente'] in self.raw_html
        
        if hay_afiliacion:
            afiliado = True
        elif no_hay_afiliacion:
            afiliado = False
        else:
            afiliado = None

        data = {
            'title': self.soup.title.text,
            'afiliado': afiliado,
            'tablas': [],
        }

        # get tables
        tables = []
        for table in s_tables:
            dict_table = self._get_table(table)
            tables.append(dict_table)
            use, dat = self._parse_table(dict_table)
            if use or self.debug:
                data['tablas'].append(dat)
        if self.debug:
            data['unparsed_tables'] = tables
        
        return data
    
    def _parse_table(self, dict_table):
        """ identificar la tabla y transformarla en datos valiosos """

        summary = dict_table['summary']
        logger.info(f'Parsing table {summary}')

        if summary == "Esta tabla muestra los datos de Afiliaci\u00f3n Vigente":
            # tabla general que incluye tablas dentro
            return False, 'No interesa'
        elif summary == "Esta tabla muestra los datos personales":
            return True, self._parse_datos_personales_afiliado(dict_table['rows'])
        elif summary == "Esta tabla muestra los datos de afiliaci\u00f3n":
            return True, self._parse_datos_de_afiliacion(dict_table['rows'])
        elif summary == "Esta tabla muestra los datos de la persona":
            return True, self._parse_datos_personales_no_afiliado(dict_table['rows'])
        elif summary == "Esta tabla muestra los datos de bajas":
            # TODO return True, self._parse_bajas(dict_table['rows'])
            return False, 'TODO'
        elif summary == "Esta tabla muestra los datos declarados por el empleador":
            return True, self._parse_datos_del_empleador(dict_table['rows'])
        else:
            return False, f'Summary no reconocido {summary}'

    def _clean_row(self, row):
        """ revisar antes de tomar como valido los datos de una fila en particular """
        if type(row) != list:
            row = ['INVALIDA DATA TYPE', str(row)]
        
        if len(row) == 0:
            return None
        elif len(row) == 1:
            row.append('')
        
        return row[0], row[1]

    def _parse_datos_personales_afiliado(self, rows):
        """ sample 
            ["Parentesco","TITULAR"],
            ["CUIL", "27-1XXXXXX3-6"],
            ["Tipo de documento","DOCUMENTO UNICO"],
            ["N\u00famero de documento", "1XXXXX3"],
            ["Apellido y nombre","PEREZ JUAN"],
            ["Provincia","CORDOBA"],
            ["Fecha de nacimiento", "09-01-1980"],
            ["Sexo", "Femenino"]
        """
        data = {'name': 'AFILIACION', 'data': {}}
        for row in rows:
            k, v = self._clean_row(row)
            data['data'][k] = v
        return data

    def _parse_datos_de_afiliacion(self, rows):
        """ sample 
            ["CUIL titular", "27-1XXXXXXX3-6"],
            ["CUIT de empleador", "33-63761744-9"],
            ["Tipo de beneficiario", "JUBILADOS Y PENSIONADOS DE PAMI"],
            ["C\u00f3digo de Obra Social", "5-0080-7"],
            ["Denominaci\u00f3n Obra Social", "INSTITUTO NACIONAL DE SERVICIOS SOCIALES PARA JUBILADOS Y PENSIONADOS"],
            ["Fecha Alta Obra Social", "01-08-2012"]
        """
        data = {'name': 'AFILIADO', 'data': {}}
        for row in rows:
            k, v = self._clean_row(row)
            data['data'][k] = v
        return data

    
    def _parse_datos_personales_no_afiliado(self, rows):
        """ sample 
            ["Apellido y Nombre","Tipo Documento","Nro Documento","CUIL"], ["PEREZ JUAN","DU","2XXXXXX1","202XXXXX14"]
        
        """
        try:
            data = dict(zip(rows[0], rows[1]))
        except Exception as e:
            data = {'error': f'Error Zipping: {e}', 'rows': rows}

        data = {'name': 'NO_AFILIADO', 'data': data}
        return data

    def _parse_datos_del_empleador(self, rows):
        """ sample
            ["Tipo Beneficiario Declarado", "RELACION DE DEPENDENCIA (DDJJ SIJP)"],
            ["Ultimo Per\u00edodo Declarado","04-2020"]
        """
        data = {'name': 'DECLARADO_POR_EMPLEADOR', 'data': {}}
        for row in rows:
            k, v = self._clean_row(row)
            data['data'][k] = v
        return data

    """ TODO 
    def _parse_bajas(self, rows):
        return
    """ 
    def _get_table(self, soup_table):
        res = {
            'summary': soup_table.get('summary', ''),
            'rows': []
        }
        
        # print('************************************************************')
        # print(f'TABLE {soup_table}')
        # print('************************************************************')

        all_trs = soup_table.findAll('tr')
        res['total_rows'] = len(all_trs)
        
        for row in all_trs:
            cols = row.findAll(['td', 'th'])
            # print(f'\tCOLS {cols}')
            elems = [ele.text.strip() for ele in cols]
            # print(f'\t\tELEMS {elems}')
            res['rows'].append(elems)
        
        return res
    
    def _open_file(self, path):
        f = open(path)
        res = f.read()
        f.close()

        return res
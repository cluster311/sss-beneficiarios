[![Travis (.org)](https://img.shields.io/travis/cluster311/sss-beneficiarios?style=for-the-badge)](https://travis-ci.org/github/cluster311/sss-beneficiarios)
[![GitHub All Releases](https://img.shields.io/github/downloads/cluster311/sss-beneficiarios/total?style=for-the-badge)](https://github.com/cluster311/sss-beneficiarios/releases)
[![GitHub Issues](https://img.shields.io/github/issues/cluster311/sss-beneficiarios?style=for-the-badge)](https://github.com/cluster311/sss-beneficiarios/issues)
[![GitHub PR](https://img.shields.io/github/issues-pr/cluster311/sss-beneficiarios?style=for-the-badge)](https://github.com/cluster311/sss-beneficiarios/pulls)
[![Licence](https://img.shields.io/github/license/cluster311/sss-beneficiarios?style=for-the-badge)](https://github.com/cluster311/sss-beneficiarios/blob/master/LICENSE)
[![Twitter URL](https://img.shields.io/twitter/url?style=for-the-badge&url=https%3A%2F%2Ftwitter.com%2Fcluster311)](https://twitter.com/cluster311)
[![Pypi py version](https://img.shields.io/pypi/pyversions/sss-beneficiarios-hospitales?style=for-the-badge)](https://pypi.org/project/sss-beneficiarios-hospitales/)
[![Last Commit](https://img.shields.io/github/last-commit/cluster311/sss-beneficiarios?style=for-the-badge)](https://github.com/cluster311/sss-beneficiarios/commits/master)
# Registro privado de beneficiarios de Obras Sociales de Argentina

Consultas al Padrón de Beneficiarios de los Agentes Nacionales del Seguro de Salud. Requiere credenciales de Hospital habilitado.

## Uso

Requiere tener usuario válido para el servicio de información sobre beneficiarios de 
la Superintendencia de Servicios de Salud

``` python
usuario = 'FAKE'  # usuario de prueba
clave = 'FAKE'   # clave de pruebas

from sss_beneficiarios_hospitales.data import DataBeneficiariosSSSHospital
dbh = DataBeneficiariosSSSHospital(user=usuario, password=clave)

res = dbh.query(dni='99999999')
print(res)
```

Resultados para no afiliados

``` python
{
    'ok': True, 
    'resultados': {
        'title': 'Superintendencia de Servicios de Salud',
        'afiliado': False,
        'tablas': [
            {
                "name": "NO_AFILIADO",
                "data": {
                    "Apellido y Nombre": "PEREZ JUAN",
                    "Tipo Documento": "DU",
                    "Nro Documento": "2XXXXXX3",
                    "CUIL": "202XXXXXX31"
                }
            }
        ]
        }
}
```

Resultados para afiliados (la seccion `DECLARADO_POR_EMPLEADOR` podría no estar disponible)

``` python
{
    'ok': True, 
    'resultados': {
        'title': 'Superintendencia de Servicios de Salud', 
        'afiliado': True, 
        'tablas': [
            {
                'name': 'AFILIACION', 
                'data': {
                    'Parentesco': 'TITULAR', 
                    'CUIL': '20-1XXXXXX8-8', 
                    'Tipo de documento': 'DOCUMENTO UNICO', 
                    'Número de documento': '1XXXXX8', 
                    'Apellido y nombre': 'GOMEZ GONZALO', 
                    'Provincia': 'CORDOBA', 
                    'Fecha de nacimiento': '27-12-1951', 
                    'Sexo': 'Masculino'
                    }
            }, 
            {
                'name': 'AFILIADO', 
                'data': {
                    'CUIL titular': '20-1XXXXXX8-8', 
                    'CUIT de empleador': '30-XXX07484-3', 
                    'Tipo de beneficiario': 'RELACION DE DEPENDENCIA', 
                    'Código de Obra Social': '1-1320-5', 
                    'Denominación Obra Social': 'OBRA SOCIAL DE JEFES Y OFICIALES NAVALES DE RADIOCOMUNICACIONES', 
                    'Fecha Alta Obra Social': '01-01-2011'
                    }
            }, 
            {
                'name': 'DECLARADO_POR_EMPLEADOR', 
                'data': {
                    'Tipo Beneficiario Declarado': 'RELACION DE DEPENDENCIA (DDJJ SIJP)', 
                    'Ultimo Período Declarado': '12-2019'
                    }
            }
            ]}
}
```


## Install

Instalar desde [Pypi](https://pypi.org/project/sss-beneficiarios-hospitales/)

```
pip install sss_beneficiarios_hospitales
```

## Test

```
pip install -r dev-requirements.txt
python -m pytest
```
[![Build Status](https://travis-ci.org/cluster311/sss-beneficiarios.svg?branch=master)](https://travis-ci.org/cluster311/sss-beneficiarios)
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
        'hay_afiliacion': False,
        'no_hay_afiliacion': True,
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
        'hay_afiliacion': True, 
        'no_hay_afiliacion': False, 
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
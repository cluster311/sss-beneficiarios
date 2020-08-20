from sss_beneficiarios_hospitales.data import DataBeneficiariosSSSHospital


def test_query_afiliado():
    dbh = DataBeneficiariosSSSHospital(user='FAKE', password='FAKE')
    res = dbh.query(dni='full-afiliado')
    assert res['ok']
    data = res['resultados']
    assert data['title'] == "Superintendencia de Servicios de Salud"
    assert data["afiliado"]
    
    assert len(data['tablas']) == 2
    for d in data['tablas']:
        assert "name" in d
        is_afiliacion = "AFILIACION" in [v for k, v in d.items() if k == 'name']
        is_persona = "AFILIADO" in [v for k, v in d.items() if k == 'name']
        assert is_afiliacion or is_persona

        if is_afiliacion:
            assert d['data']["Parentesco"] == "TITULAR"
            assert d['data']["CUIL"] == "27-1XXXXX3-6"
            assert d['data']["Tipo de documento"] == "DOCUMENTO UNICO"
            assert d['data']["N\u00famero de documento"] == "1XXXXX3"
            assert d['data']["Apellido y nombre"] == "FXXXL  MARIA"
            assert d['data']["Provincia"] == "CORDOBA"
            assert d['data']["Fecha de nacimiento"] == "09-09-1961"
            assert d['data']["Sexo"] == "Femenino"

        if is_persona:
            assert d['data']["CUIL titular"] == "27-1XXXXX3-6"
            assert d['data']["CUIT de empleador"] == "33-63761744-9"
            assert d['data']["CUIL titular"] == "27-1XXXXX3-6"
            assert d['data']["Tipo de beneficiario"] == "JUBILADOS Y PENSIONADOS DE PAMI"
            assert d['data']["C\u00f3digo de Obra Social"] == "5-0080-7"
            assert d['data']["Denominaci\u00f3n Obra Social"] == "INSTITUTO NACIONAL DE SERVICIOS SOCIALES PARA JUBILADOS Y PENSIONADOS"
            assert d['data']["Fecha Alta Obra Social"] == "01-08-2012"


def test_query_afiliado_con_empleador():
    dbh = DataBeneficiariosSSSHospital(user='FAKE', password='FAKE')
    res = dbh.query(dni='full-afiliado-con-empleador')
    assert res['ok']
    data = res['resultados']
    assert data['title'] == "Superintendencia de Servicios de Salud"
    assert data["afiliado"]
    
    for d in data['tablas']:
        assert "name" in d
        is_afiliacion = "AFILIACION" in [v for k, v in d.items() if k == 'name']
        is_persona = "AFILIADO" in [v for k, v in d.items() if k == 'name']
        is_declarado = "DECLARADO_POR_EMPLEADOR" in [v for k, v in d.items() if k == 'name']
        assert is_afiliacion or is_persona or is_declarado

        if is_afiliacion:
            assert d['data']["Parentesco"] == "TITULAR"
            assert d['data']["CUIL"] == "27-1XXXXX3-6"
            assert d['data']["Tipo de documento"] == "DOCUMENTO UNICO"
            assert d['data']["N\u00famero de documento"] == "1XXXXX3"
            assert d['data']["Apellido y nombre"] == "GOMEZ EDUARDO"
            assert d['data']["Provincia"] == "CAPITAL FEDERAL"
            assert d['data']["Fecha de nacimiento"] == "25-05-1977"
            assert d['data']["Sexo"] == "Masculino"

        if is_persona:
            assert d['data']["CUIL titular"] == "27-1XXXXX3-6"
            assert d['data']["CUIT de empleador"] == "30-70818659-3"
            assert d['data']["CUIL titular"] == "27-1XXXXX3-6"
            assert d['data']["Tipo de beneficiario"] == "RELACION DE DEPENDENCIA"
            assert d['data']["C\u00f3digo de Obra Social"] == "4-0080-0"
            assert d['data']["Denominaci\u00f3n Obra Social"] == "OBRA SOCIAL DE EJECUTIVOS Y DEL PERSONAL DE DIRECCION DE EMPRESAS"
            assert d['data']["Fecha Alta Obra Social"] == "01-06-1931"
        
        if is_declarado:
            assert d['data']["Tipo Beneficiario Declarado"] == "RELACION DE DEPENDENCIA (DDJJ SIJP)"
            assert d['data']["Ultimo Per\u00edodo Declarado"] == "02-2020"


def test_query_no_afiliado():
    dbh = DataBeneficiariosSSSHospital(user='FAKE', password='FAKE')
    res = dbh.query(dni='full-sin-datos')
    assert res['ok']
    data = res['resultados']
    assert data['title'] == "Superintendencia de Servicios de Salud"
    assert data["afiliado"] == False
    
    for d in data['tablas']:
        assert "name" in d
        is_persona = "NO_AFILIADO" in [v for k, v in d.items() if k == 'name']
        assert is_persona

        assert d['data']["Apellido y Nombre"] == "BXXXXXXXXS FXXXL JUAN CARLOS"
        assert d['data']["Tipo Documento"] == "DU"
        assert d['data']["Nro Documento"] == "2XXXXX1"
        assert d['data']["CUIL"] == "202XXXXX18"


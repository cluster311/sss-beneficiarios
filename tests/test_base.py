from tests import settings
from sss_beneficiarios_hospitales.data import DataBeneficiariosSSSHospital

print(settings.USER)
print(settings.PASSWORD)
print(settings.DNI)

dbh = DataBeneficiariosSSSHospital(user=settings.USER, password=settings.PASSWORD)
assert dbh.login()
dbh.query(dni=settings.DNI)



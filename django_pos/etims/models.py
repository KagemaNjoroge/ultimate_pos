from django.db import models

# Create your views here.
class Country(models.Model):
    countryId = models.AutoField(primary_key=True)
    countryCode = models.CharField(max_length=10, unique=True)
    countryName = models.CharField(max_length=100, unique=True)
    currencyCode = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = "Country"
        verbose_name_plural = "Countries"
        verbose_name = "Country"

    def __str__(self) -> str:
        return self.countryName

    def to_json(self) -> dict:
        return {
            "id": self.countryId,
            "name": self.countryName,
            "currency_code": self.currencyCode,
            "country_code": self.countryCode,
        }


class EtimsNotice(models.Model):
    """
    {'noticeNo': 28, 'title': 'First Craft', 'cont': 'First Craft',
    'dtlUrl': 'http://HOST_IP:PORT/common/link/ebm/receipt/indexEbmNotice?noticeNo=28',
    'regrNm': 'Admin', 'regDt': '20240524120831'},
    """

    noticeNumber = models.CharField(primary_key=True, max_length=100)
    title = models.CharField(max_length=100)
    content = models.TextField()
    noticeUrl = models.URLField()
    registrationDate = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    registrarName = models.CharField(max_length=100)

    class Meta:
        db_table = "Notice"
        verbose_name_plural = "Notices"
        verbose_name = "Notice"

    def __str__(self) -> str:
        return self.title

    def to_json(self) -> dict:
        return {
            "noticeNumber": self.noticeNumber,
            "title": self.title,
            "content": self.content,
            "noticeURL": self.noticeURL,
            "registrationDate": self.registrationDate,
            "registrarName": self.registrarName,
            "read": self.read,
        }


class TaxType(models.Model):

    taxTypeCode = models.CharField(max_length=1, primary_key=True)
    taxTypeName = models.CharField(
        max_length=20,
    )
    taxTypeDescription = models.CharField(
        max_length=100,
    )

    class Meta:
        db_table = "TaxType"
        verbose_name_plural = "TaxTypes"
        verbose_name = "TaxType"

    def to_json(self) -> dict:
        return {
            "tax_type_code": self.taxTypeCode,
            "tax_type_name": self.taxTypeName,
            "tax_type_description": self.taxTypeDescription,
        }


class PackagingUnits(models.Model):
    packagingUnitId = models.AutoField(primary_key=True)
    packagingUnitName = models.CharField(max_length=100)
    packagingUnitDescription = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=5, default="BZ")

    class Meta:
        db_table = "PackagingUnits"
        verbose_name_plural = "Packaging Units"
        verbose_name = "Packaging Unit"

    def __str__(self) -> str:
        return self.packagingUnitName

    def to_json(self) -> dict:
        return {
            "packagingUnitId": self.packagingUnitId,
            "packagingUnitName": self.packagingUnitName,
            "packagingUnitDescription": self.packagingUnitDescription,
            "code": self.code,
        }


class UnitOfQuantity(models.Model):
    unitOfQuantityId = models.AutoField(primary_key=True)
    unitOfQuantityName = models.CharField(max_length=100)
    unitOfQuantityDescription = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=5, default="NO")

    class Meta:
        db_table = "UnitsOfQuantity"
        verbose_name_plural = "Units Of Quantity"
        verbose_name = "Unit Of Quantity"

    def __str__(self) -> str:
        return self.unitOfQuantityName

    def to_json(self) -> dict:
        return {
            "unitOfQuantityId": self.unitOfQuantityId,
            "unitOfQuantityName": self.unitOfQuantityName,
            "unitOfQuantityDescription": self.unitOfQuantityDescription,
            "code": self.code,
        }


class ItemClassCodes(models.Model):
    """ "
        {
        "itemClsCd": "99011005",
        "itemClsNm": "Groundnuts not roasted or otherwise cooked In shell of tariff number 12024100",
        "itemClsLvl": 4,
        "taxTyCd": null,
        "mjrTgYn": null,
        "useYn": "Y"
    },
    """

    itemClassCode = models.CharField(max_length=1000)
    itemClassLevel = models.IntegerField()
    itemClassCodeName = models.CharField(max_length=1000)
    taxTypeCode = models.CharField(max_length=100, blank=True, null=True)
    majorTargetYN = models.BooleanField(default=False)
    useYN = models.BooleanField(default=True)

    class Meta:
        db_table = "ItemClassCodes"
        verbose_name_plural = "Item Class Codes"
        verbose_name = "Item Class Code"

    def __str__(self) -> str:
        return self.itemClassCodeName

    def to_json(self) -> dict:
        return {
            "itemClassLevel": self.itemClassLevel,
            "itemClassCodeName": self.itemClassCodeName,
            "taxTypeCode": self.taxTypeCode,
            "useYN": self.useYN,
            "majorTargetYN": self.majorTargetYN,
        }


class EtimsBranch(models.Model):
    """
    {'tin': 'P051238105V', 'bhfId': '00', 'bhfNm': 'Headquarter', 'bhfSttsCd': '01',
    'prvncNm': 'Nairobi', 'dstrtNm': 'Westlands District', 'sctrNm': 'Lavington',
    'locDesc': None, 'mgrNm': 'DEJAVU TECHNOLOGIES LIMITED', 'mgrTelNo': '0734717119',
    'mgrEmail': 'ACCOUNTS1@DEJAVUTECHKENYA.COM', 'hqYn': 'Y'}
    """

    branch_tin = models.CharField(max_length=11)
    branch_id = models.CharField(max_length=10, primary_key=True)
    branch_name = models.CharField(max_length=100)
    branch_status_code = models.CharField(max_length=10)
    province_name = models.CharField(max_length=100, blank=True, null=True)
    district_name = models.CharField(max_length=100, blank=True, null=True)
    sctr_name = models.CharField(max_length=100, blank=True, null=True)
    location_description = models.TextField(blank=True, null=True)
    manager_name = models.CharField(max_length=100, blank=True, null=True)
    manager_telephone = models.CharField(max_length=15, blank=True, null=True)
    manager_email = models.EmailField(blank=True, null=True)

    def __str__(self) -> str:
        return self.branch_name

    def to_json(self) -> dict:
        return {
            "branch_tin": self.branch_tin,
            "branch_id": self.branch_id,
            "branch_name": self.branch_name,
            "branch_status_code": self.branch_status_code,
            "province_name": self.province_name,
            "district_name": self.district_name,
            "sctr_name": self.sctr_name,
            "location_description": self.location_description,
            "manager_name": self.manager_name,
            "manager_telephone": self.manager_telephone,
            "manager_email": self.manager_email,
        }

    class Meta:
        db_table = "EtimsBranch"
        verbose_name_plural = "Etims Branches"
        verbose_name = "Etims Branch"


class EtimsProduct(models.Model):
    """
    {"tin": "P051238105V", "itemCd": "00000000000001", "itemClsCd": "99000000",
    "itemTyCd": "1", "itemNm": "A", "itemStdNm": null, "orgnNatCd": "AG",
    "pkgUnitCd": "BC", "qtyUnitCd": "4B", "taxTyCd": "A", "btchNo": "1",
    "regBhfId": "00", "bcd": "00000000000001", "dftPrc": 1, "grpPrcL1": 0,
    "grpPrcL2": 0, "grpPrcL3": 0, "grpPrcL4": 0, "grpPrcL5": 0, "addInfo": "1",
    "sftyQty": 0, "isrcAplcbYn": "N", "rraModYn": "N", "useYn": "Y"
    }
    """

    pass

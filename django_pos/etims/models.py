from django.db import models


# Create your views here.
class Country(models.Model):
    countryId = models.AutoField(primary_key=True)
    countryCode = models.CharField(max_length=10, unique=True)
    countryName = models.CharField(max_length=100, unique=True)
    currencyCode = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = 'Country'
        verbose_name_plural = 'Countries'
        verbose_name = 'Country'

    def __str__(self) -> str:
        return self.countryName


class Notice(models.Model):
    noticeNumber = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    noticeURL = models.URLField()
    registrationDate = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        db_table = 'Notice'
        verbose_name_plural = 'Notices'
        verbose_name = 'Notice'

    def __str__(self) -> str:
        return self.title

    def to_json(self):
        return {
            'noticeNumber': self.noticeNumber,
            'title': self.title,
            'content': self.content,
            'noticeURL': self.noticeURL,
            'registrationDate': self.registrationDate,
            'read': self.read
        }


class TaxType(models.Model):
    taxTypeId = models.AutoField(primary_key=True)
    taxTypeName = models.CharField(max_length=100)
    taxTypeRate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    taxTypeIdentifier = models.CharField(max_length=1, unique=True)  # A - 16%, B - 8%, C - 0% etc

    class Meta:
        db_table = 'TaxType'
        verbose_name_plural = 'TaxTypes'
        verbose_name = 'TaxType'

    def __str__(self) -> str:
        return self.taxTypeName

    def to_json(self):
        return {
            'taxTypeId': self.taxTypeId,
            'taxTypeName': self.taxTypeName,
            'taxTypeRate': self.taxTypeRate,
            'taxTypeIdentifier': self.taxTypeIdentifier
        }


class PackagingUnits(models.Model):
    packagingUnitId = models.AutoField(primary_key=True)
    packagingUnitName = models.CharField(max_length=100)
    packagingUnitDescription = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'PackagingUnits'
        verbose_name_plural = 'Packaging Units'
        verbose_name = 'Packaging Unit'

    def __str__(self) -> str:
        return self.packagingUnitName

    def to_json(self):
        return {
            'packagingUnitId': self.packagingUnitId,
            'packagingUnitName': self.packagingUnitName,
            'packagingUnitDescription': self.packagingUnitDescription
        }


class UnitOfQuantity(models.Model):
    unitOfQuantityId = models.AutoField(primary_key=True)
    unitOfQuantityName = models.CharField(max_length=100)
    unitOfQuantityDescription = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'UnitsOfQuantity'
        verbose_name_plural = 'Unit Of Quantity'
        verbose_name = 'Unit Of Quantity'

    def __str__(self) -> str:
        return self.unitOfQuantityName

    def to_json(self):
        return {
            'unitOfQuantityId': self.unitOfQuantityId,
            'unitOfQuantityName': self.unitOfQuantityName,
            'unitOfQuantityDescription': self.unitOfQuantityDescription,
        }


class ItemClassCodes(models.Model):
    itemClassLevel = models.IntegerField()
    itemClassCodeName = models.CharField(max_length=100, unique=True)
    taxType = models.ForeignKey(TaxType, models.PROTECT, db_column='taxType')
    useYN = models.BooleanField(default=True)

    class Meta:
        db_table = 'ItemClassCodes'
        verbose_name_plural = 'Item Class Codes'
        verbose_name = 'Item Class Code'

    def __str__(self) -> str:
        return self.itemClassCodeName

    def to_json(self):
        return {
            'itemClassLevel': self.itemClassLevel,
            'itemClassCodeName': self.itemClassCodeName,
            'taxType': self.taxType.to_json(),
            'useYN': self.useYN
        }

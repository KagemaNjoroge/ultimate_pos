from django.db import models


# Create your views here.
"""
CREATE TABLE "Country" 
(
	"countryId"	INTEGER,
	"countryCode"	TEXT NOT NULL UNIQUE,
	"countryName"	TEXT NOT NULL,
	"currencyCode"	TEXT NOT NULL,
	PRIMARY KEY("countryId" AUTOINCREMENT)
);


CREATE TABLE "Notice"
(
	"noticeNumber"	INTEGER,
	"title"	TEXT NOT NULL,
	"content"	TEXT NOT NULL,
	"noticeURL"	TEXT NOT NULL,
	"registrationDate"	DATETIME,
	"read"	INTEGER DEFAULT 0,
	PRIMARY KEY("noticeNumber" AUTOINCREMENT)
);

  CREATE TABLE "TaxType"
(
	"taxTypeId"	INTEGER,
	"taxTypeName"	TEXT NOT NULL,
	"taxTypeRate"	NUMERIC NOT NULL DEFAULT 0,
	PRIMARY KEY("taxTypeId" AUTOINCREMENT)
);
"""


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
            'taxTypeRate': self.taxTypeRate
        }

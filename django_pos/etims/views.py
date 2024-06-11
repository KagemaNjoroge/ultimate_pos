from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
from dotenv import load_dotenv
from etims_vscu_wrapper.clients.http_client import HttpClient
from etims_vscu_wrapper.core.VSCUProtocol.code_data import CodeData
from pydantic import Json

from etims.utils.server_status import ping
from .models import EtimsBranch, EtimsNotice, ItemClassCodes
import datetime
from etims_vscu_wrapper.core.VSCUProtocol.item_information import ItemInformation

load_dotenv()

etims_url = os.getenv("ETIMS_ENDPOINT")
device_serial = os.getenv("DEVICE_SERIAL_NUMBER")
bhf_id = os.getenv("BHF_ID")
kra_pin = os.getenv("KRA_PIN")


http_client = HttpClient(etims_url)


@login_required(login_url="/users/login/")
def get_etims_server_status(request: HttpRequest) -> HttpResponse:
    status = ping(etims_url)
    if status:
        return JsonResponse({"status": "success"}, safe=False)
    return JsonResponse({"status": "error"}, safe=False)


@login_required(login_url="/users/login/")
def etims(request: HttpRequest) -> HttpResponse:
    return render(request, "etims/etims.html", {"active_icon": "etims"})


def get_etims_branches_list(request: HttpRequest) -> HttpResponse:

    code_data = CodeData(http_client, kra_pin, bhf_id)
    code_list = code_data.get_branch_list().json()
    branches = code_list["data"]["bhfList"]
    """
    
    [{'tin': 'P051238105V', 'bhfId': '00', 'bhfNm': 'Headquarter', 'bhfSttsCd': '01', 'prvncNm': 'Nairobi', 'dstrtNm': 'Westlands District', 'sctrNm': 'Lavington', 'locDesc': None, 'mgrNm': 'DEJAVU TECHNOLOGIES LIMITED', 'mgrTelNo': '0734717119', 'mgrEmail': 'ACCOUNTS1@DEJAVUTECHKENYA.COM', 'hqYn': 'Y'}
    """
    # save branches in the database
    for branch in branches:
        EtimsBranch.objects.update_or_create(
            branch_tin=branch["tin"],
            branch_id=branch["bhfId"],
            branch_name=branch["bhfNm"],
            branch_status_code=branch["bhfSttsCd"],
            province_name=branch["prvncNm"],
            district_name=branch["dstrtNm"],
            sctr_name=branch["sctrNm"],
            location_description=branch["locDesc"],
            manager_name=branch["mgrNm"],
            manager_telephone=branch["mgrTelNo"],
            manager_email=branch["mgrEmail"],
        )

    return JsonResponse(branches, safe=False)


def parse_bool(value: str) -> bool:
    if value == "Y" or value == "y" or value == "1":
        return True
    return False


def get_etims_notices(request: HttpRequest) -> HttpResponse:

    code_data = CodeData(http_client, kra_pin, bhf_id)
    code_list = code_data.get_notice_list().json()
    notices = code_list["data"]["noticeList"]
    """
    {'noticeNo': 28, 'title': 'First Craft', 'cont': 'First Craft', 
    'dtlUrl': 'http://HOST_IP:PORT/common/link/ebm/receipt/indexEbmNotice?noticeNo=28', 
    'regrNm': 'Admin', 'regDt': '20240524120831'}
    """
    for notice in notices:
        EtimsNotice.objects.update_or_create(
            notice_no=notice["noticeNo"],
            title=notice["title"],
            content=notice["cont"],
            detail_url=notice["dtlUrl"],
            registrant_name=notice["regrNm"],
            registration_date=datetime.datetime.strptime(
                notice["regDt"], "%Y%m%d%H%M%S"
            ),
        )

    return JsonResponse(notices, safe=False)


def get_etims_items_class_codes(request: HttpRequest) -> HttpResponse:
    code_data = CodeData(http_client, kra_pin, bhf_id)
    code_list = code_data.get_item_classification_list().json()
    try:
        item_class_codes = code_list["data"]["itemClsList"]
        """
            {
            "itemClsCd": "99011005",
            "itemClsNm": "Groundnuts not roasted or otherwise cooked In shell of tariff number 12024100",
            "itemClsLvl": 4,
            "taxTyCd": null,
            "mjrTgYn": null,
            "useYn": "Y"
        },
        """
        for item_class_code_info in item_class_codes:

            ItemClassCodes.objects.update_or_create(
                itemClassCode=item_class_code_info["itemClsCd"],
                itemClassCodeName=item_class_code_info["itemClsNm"],
                itemClassLevel=item_class_code_info["itemClsLvl"],
                taxTypeCode=item_class_code_info["taxTyCd"],
                majorTargetYN=parse_bool(item_class_code_info["mjrTgYn"]),
                useYN=parse_bool(item_class_code_info["useYn"]),
            )
        return JsonResponse(item_class_codes, safe=False)
    except KeyError:
        return JsonResponse({"error": "No data found"}, safe=False)


def get_etims_items_list(request: HttpRequest) -> HttpResponse:
    client = ItemInformation(http_client=http_client, tin=kra_pin, bhf_id=bhf_id)
    try:
        items = client.get_item_list().json()
        if items["resultCd"] == "000":
            items = items["data"]["itemList"]
            return JsonResponse(items, safe=False)
        else:
            return JsonResponse({"error": items["resultMsg"]}, safe=False)
    except KeyError:
        return JsonResponse({"error": "No data found"}, safe=False)

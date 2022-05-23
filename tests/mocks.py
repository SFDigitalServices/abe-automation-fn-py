"""Mock objects for testing"""
# pylint: disable-all

NOCO_WEBHOOK = {
    "modified_by": "ds-admin@test.test",
    "ida_submission_id": "1",
    "status_id": "1"
}

SUBMISSION = {
    "ID": 24,
    "CONTACT_NAME": "contact name",
    "CONTACT_EMAIL": "test@test.com",
    "CONTACT_PHONE": "(415) 111-1111",
    "FORMIO_SUBMISSION_ID": "123abc",
    "PROCESS": "categoryChecklist",
    "UPLOAD": "http://www.test.com/test.pdf",
    "APPLICATION_NUMBER": None,
    "SUBMISSION_DATE": "2022-03-12",
    "AUDIT_BY": None,
    "AUDIT_DATE": None,
    "AUDIT_NOTE": None,
    "UNVERIFIED_ADDRESS": "1 Main Street",
    "UNVERIFIED_BLOCK": "1",
    "UNVERIFIED_LOT": "1",
    "UNVERIFIED_ZIP": "11111",
    "TECHNICAL_INFEASABILITY": "N",
    "UNREASONABLE_HARDSHIP": "N",
    "IDA_CATEGORY_ID_LOOKUP_id": 2,
    "IDADATA_id": 1007,
    "IDA_SUBMISSION_STATUS_id": 6,
    "IDA_STATUS_REASON_id": None,
    "AGENT_AUTHORIZATION_FORM": None,
    "IDACategoryIdLookupRead": {
        "IDA_CATEGORY_ID": 2,
        "DESCRIPTION": "Non-compliant Elements, 0 step"
    },
    "IDADATARead": {
        "ID": 1007,
        "BLOCK": "6532",
        "LOT": "021"
    },
    "IDA_SUBMISSION_STATUSRead": {
        "ID": 6,
        "DESCRIPTION": "Recorded"
    }
}

IDADATA = {
    "ID": 1007,
    "BLOCK": "6532",
    "LOT": "021",
    "CLASSCode": None,
    "SUPERVISORDistrict": "8",
    "SUPERVISORName": "supervisor",
    "PROPERTYStreetNumber": 1,
    "PROPERTYStreetNumberSfx": None,
    "PROPERTYStreetName": "MAIN",
    "PROPERTYStreetSfx": "ST",
    "PROPERTYUnit": None,
    "PROPERTYUnitSfx": None,
    "OWNERNAME": "owner",
    "ADDRESS1": "",
    "ADDRESS2": "1 GEARY BLVD STE 1",
    "ADDRESS3": None,
    "ADDRESS4": None,
    "OWNERZIP": None,
    "DELETEDate": None,
    "ZONINGDescription": "Residential",
    "ZONE": "RM-1",
    "NEIGHBORHOOD": "Mission",
    "TENANTName": "John Doe",
    "TENANTAddress1": "1827 Main Ave",
    "TENANTAddress2": "SF, CA",
    "TENANTAddress3": None,
    "TENANTAddress4": None,
    "TENANTZip": "11111",
    "IDAAppNum": None,
    "USERId": "user_id",
    "LASTModifiedBy": "automation",
    "LASTModifiedDate": "2022-03-24",
    "APPLICATIONNumber": None,
    "COMPLAINTNumber": None,
    "RESPONDED": None,
    "BATCH": None,
    "NOTES": "1/7/19: Extension to submit forms\r\nExemption 4.1",
    "TRANSACTIONNumber": None,
    "TECHNICAL_INFEASABILITY": "N",
    "UNREASONABLE_HARDSHIP": "N",
    "ALTERNATE_METHODS": "N",
    "OTHERS": "N",
    "FRMRcvdDt": "2019-03-28",
    "PYMTRcvdDt": None,
    "CAT_CHKLST_COMPL_FORM": "N",
    "PRE_SCREENING_FORM": "Y",
    "OWNERPhone": "415-111-1111",
    "OWNEREmail": "user@user.com",
    "TENANTPhone": "415-111-1111",
    "TENANTEmail": "user@user.com",
    "PRESCREENFORM_RETURN": None,
    "CATCHECKFORM_RETURN": None,
    "WAIVER_FORM": "N",
    "EXT_TIME_SUBM_REQ_FORMS": "N",
    "EXT_TIME_FILE_PERM_APPL": "N",
    "RESIDENCE_TYPE": None,
    "IDA_CATEGORY_ID": None,
    "combined_address": "1 MAIN  ST",
    "IDAProfessionalList": [],
    "IDA_SUBMISSIONList": [
        {
            "ID": 105,
            "CONTACT_NAME": "user",
            "IDADATA_id": 1007
        }
    ],
    "IDACategoryIdLookupRead": {
        "IDA_CATEGORY_ID": 2,
        "DESCRIPTION": "Non-compliant Elements, 0 step"
    }
}

ADDRESS_POST = {
    "idadata_id": "1",
    "PROPERTYStreetNumber": "1600",
    "PROPERTYStreetNumberSfx": None,
    "PROPERTYStreetName": "Pennsylvania",
    "PROPERTYStreetSfx": "Ave",
    "PROPERTYUnit": "",
    "PROPERTYUnitSfx": None,
    "FULL_ADDRESS": ""
}

BLOCKLOT_POST = {
    "idadata_id": "1",
    "BLOCK": "001",
    "LOT": "111",
    "BLOCKLOT": ""
}

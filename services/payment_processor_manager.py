from django.utils.translation import gettext_lazy as _
from services.payment_processor_config import (
    PAYMENT_PROCESSOR_SYNDCT_ID,
    PAYMENT_PROCESSOR_BILL_FETCH_MODE,
    PAYMENT_PROCESSOR_URL,
    PAYMENT_PROCESSOR_ND_ID,
    GET_TOKEN_ACCESS_URI,
    FETCH_MDM_V2_ACCESS_URI,
    FETCH_BILL_ACCESS_URI,
    PAY_BILL_ACCESS_URI,
    CHECK_BILL_STATUS_ACCESS_URI,
    PAYMENT_PROCESSOR_BILLERS_INFORMATION_SYNC_FREQUENCY
)
from services.constants import RequestTypes
from django.core.cache import cache
from django.conf import settings
from services.decorators import (
    check_and_set_payment_processor_token
)
from services.helper_functions import (
    generate_unique_transaction_id,
    get_current_time,
    generate_unique_reference_id
)
from services.helper_functions import RequestMixin
from services.encryption_decryption_request_manager import (
    EncryptionDecryptionBodyMixin
)
from services.constants import CacheKey
from billing.models import (
    FetchBillRequest,
    FetchBillResponse
)


class PaymentProcessorGetToken(RequestMixin):
    @staticmethod
    def convert_duration_to_seconds(duration_str):
        suffix_multiplier = {'s': 1, 'm': 60, 'h': 3600}
        suffix = duration_str[-1]
        multiplier = suffix_multiplier.get(suffix)
        if multiplier is not None:
            return int(duration_str.rstrip(suffix)) * multiplier
        else:
            raise ValueError(f"Unsupported duration format: {duration_str}")

    @staticmethod
    def get_payment_processor_token(*args, **kwargs):
        url = PAYMENT_PROCESSOR_URL+GET_TOKEN_ACCESS_URI
        payload = {
            'user_id': kwargs.get('user_id', settings.PAYMENT_PROCESSOR_USER_ID),
            'pass_key': kwargs.get('pass_key', settings.PAYMENT_PROCESSOR_PASS_KEY)
        }
        req_context = {
            'req_type': RequestTypes.POST,
            'url': url,
            'payload': payload
        }
        res = RequestMixin.make_request(**req_context)
        res = res.json()
        if res.get('token_exp_time') and res.get('token_exp_time') is not None:
            cache.set(
                key=CacheKey.PAYMENT_PROCESSOR_TOKEN.value,
                value=res.get('security_token'),
                timeout=PaymentProcessorGetToken.convert_duration_to_seconds(
                    res.get('token_exp_time')
                )
            )
        return res


class PaymentProcessorFetchMdmBillersInformation(EncryptionDecryptionBodyMixin):
    @staticmethod
    @check_and_set_payment_processor_token
    def fetch_mdm_billers_information(*args, **kwargs):
        headers = {
            'Content-Type': 'text/plain',
            'Authorization': 'Bearer '+cache.get('payment_processor_token')
        }
        url = PAYMENT_PROCESSOR_URL+FETCH_MDM_V2_ACCESS_URI
        payload = {
            "hdrs": {
                "nm": "FETCH_MDM_DATA_REQ",
                "ver": "v1.3.0",
                "tms": get_current_time(),
                "nd_id": PAYMENT_PROCESSOR_ND_ID
            },
            "trx": {
                "trx_id": generate_unique_transaction_id(),
                "trx_tms": get_current_time()
            }
        }
        encrypted_payload = EncryptionDecryptionBodyMixin.encrypt_payload(
            payload=payload
        )
        req_context = {
            'req_type': RequestTypes.POST,
            'url': url,
            'payload': encrypted_payload.decode('utf-8'),
            'headers': headers,
            'payload_type': 'data'
        }
        res = RequestMixin.make_request(**req_context)
        decrypted_payload = EncryptionDecryptionBodyMixin.decrypt_payload(
            payload=res.content.decode('utf-8')
        )

        cache.set(
            key=CacheKey.BILLERS_INFO.value,
            value=decrypted_payload,
            timeout=int(PAYMENT_PROCESSOR_BILLERS_INFORMATION_SYNC_FREQUENCY)
        )
        return decrypted_payload

    @staticmethod
    def fetch_mdm_billers_information_from_cache(*args, **kwargs):
        billers_info = cache.get(CacheKey.BILLERS_INFO.value)
        if not billers_info:
            billers_info = PaymentProcessorFetchMdmBillersInformation.fetch_mdm_billers_information(
                *args, **kwargs)
            return billers_info
        return billers_info


class PaymentProcessorFetchCustomerBillInformation(EncryptionDecryptionBodyMixin):
    @staticmethod
    @check_and_set_payment_processor_token
    def fetch_customer_bill_information(*args, **kwargs):
        headers = {
            'Content-Type': 'text/plain',
            'Authorization': 'Bearer '+cache.get('payment_processor_token')
        }
        url = PAYMENT_PROCESSOR_URL+FETCH_BILL_ACCESS_URI
        payload = {
            "hdrs": {
                "nm": "FETCH_BLL_REQ",
                "ver": "v1.3.0",
                "tms": get_current_time(),
                "ref_id": generate_unique_reference_id(),
                "nd_id": PAYMENT_PROCESSOR_ND_ID
            },
            "trx": {
                "trx_id": generate_unique_transaction_id(),
                "trx_tms": get_current_time()
            },
            "bll_inf": {
                "mode": PAYMENT_PROCESSOR_BILL_FETCH_MODE
            },
            "usr_inf": {
                "syndct_id": PAYMENT_PROCESSOR_SYNDCT_ID
            }
        }
        payload['bll_inf'].update(kwargs)
        req = FetchBillRequest.objects.create(
            payload=payload,
            ref_id=payload.get('hdrs').get('ref_id', ""),
            bllr_id=payload.get('bll_inf').get('bllr_id')
        )
        encrypted_payload = EncryptionDecryptionBodyMixin.encrypt_payload(
            payload=payload
        )
        req_context = {
            'req_type': RequestTypes.POST,
            'url': url,
            'payload': encrypted_payload.decode('utf-8'),
            'headers': headers,
            'payload_type': 'data'
        }
        res = RequestMixin.make_request(**req_context)
        decrypted_payload = EncryptionDecryptionBodyMixin.decrypt_payload(
            payload=res.content.decode('utf-8')
        )
        FetchBillResponse.objects.create(
            fetch_bill_request=req,
            response=decrypted_payload,
            ref_id=decrypted_payload.get('hdrs').get('ref_id', ""),
            trx_id=decrypted_payload.get('trx').get('trx_id'),
            bllr_inf=decrypted_payload.get('bllr_inf'),
            refno_ack=decrypted_payload.get('resp_status').get('refno_ack'),
        )
        if decrypted_payload.get('bllr_inf').get('is_bll_pd') == 'Y':
            return _("bill is already paid")
        return decrypted_payload


class PaymentProcessorPayBill(EncryptionDecryptionBodyMixin):
    @staticmethod
    @check_and_set_payment_processor_token
    def pay_bill(*args, **kwargs):
        headers = {
            'Content-Type': 'text/plain',
            'Authorization': 'Bearer '+cache.get('payment_processor_token')
        }
        url = PAYMENT_PROCESSOR_URL+PAY_BILL_ACCESS_URI
        payload = {
            "hdrs": {
                "nm": "UPDT_BLL_PYMNT_REQ",
                "ver": "v1.3.0",
                "tms": get_current_time(),
                "nd_id": PAYMENT_PROCESSOR_ND_ID,
                "ref_id": kwargs.get('ref_id')
            },
            "trx": {
                "trx_id": generate_unique_transaction_id(),
                "trx_tms": get_current_time(),
                "refno_ack": kwargs.get('refno_ack')
            },
            "pyd_inf": {
                "pyd_trxn_refid": kwargs.get('pyd_trxn_refid'),
                "pyd_tms": get_current_time(),
                "pyd_amnt": kwargs.get('pyd_amnt')
            },
            "bllr_inf": kwargs.get('bllr_inf'),
            "usr_inf": {
                "syndct_id": PAYMENT_PROCESSOR_SYNDCT_ID
            }
        }
        payload['bllr_inf'].update({"mode": "SAPI"})
        encrypted_payload = EncryptionDecryptionBodyMixin.encrypt_payload(
            payload=payload
        )
        req_context = {
            'req_type': RequestTypes.POST,
            'url': url,
            'payload': encrypted_payload.decode('utf-8'),
            'headers': headers,
            'payload_type': 'data'
        }
        res = RequestMixin.make_request(**req_context)
        decrypted_payload = EncryptionDecryptionBodyMixin.decrypt_payload(
            payload=res.content.decode('utf-8')
        )
        return decrypted_payload


class PaymentProcessorCheckBillStatus(EncryptionDecryptionBodyMixin):
    @staticmethod
    @check_and_set_payment_processor_token
    def check_bill_status(*args, **kwargs):
        headers = {
            'Content-Type': 'text/plain',
            'Authorization': 'Bearer '+cache.get('payment_processor_token')
        }
        url = PAYMENT_PROCESSOR_URL+CHECK_BILL_STATUS_ACCESS_URI
        payload = {
            "hdrs": {
                "nm": "CHCK_BLL_STTS_REQ",
                "ver": "v1.3.0",
                "tms": "2023-11-29T16:38:00+06:00",
                "nd_id": "NS5981",
                "ref_id": "DRAAKF0RPYFWXZXXUET4CY"
            },
            "trx": {
                "trx_id": "2VAFKAXEQJIIYHJVHZZIBI",
                "trx_tms": "2023-11-29T16:38:00+06:00"
            },
            "bll_inf": {
                "mode": "SAPI",
                "bllr_id": "b025"
            },
            "usr_inf": {
                "syndct_id": "s572"
            }
        }

        encrypted_payload = EncryptionDecryptionBodyMixin.encrypt_payload(
            payload=payload
        )
        req_context = {
            'req_type': RequestTypes.POST,
            'url': url,
            'payload': encrypted_payload.decode('utf-8'),
            'headers': headers,
            'payload_type': 'data'
        }
        res = RequestMixin.make_request(**req_context)
        decrypted_payload = EncryptionDecryptionBodyMixin.decrypt_payload(
            payload=res.content.decode('utf-8')
        )
        return decrypted_payload

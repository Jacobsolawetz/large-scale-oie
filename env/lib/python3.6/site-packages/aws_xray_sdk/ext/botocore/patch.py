import wrapt
import botocore.client

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.boto_utils import inject_header, aws_meta_processor


def patch():
    """
    Patch botocore client so it generates subsegments
    when calling AWS services.
    """
    if hasattr(botocore.client, '_xray_enabled'):
        return
    setattr(botocore.client, '_xray_enabled', True)

    wrapt.wrap_function_wrapper(
        'botocore.client',
        'BaseClient._make_api_call',
        _xray_traced_botocore,
    )

    wrapt.wrap_function_wrapper(
        'botocore.endpoint',
        'Endpoint._encode_headers',
        inject_header,
    )


def _xray_traced_botocore(wrapped, instance, args, kwargs):

    service = instance._service_model.metadata["endpointPrefix"]
    return xray_recorder.record_subsegment(
        wrapped, instance, args, kwargs,
        name=service,
        namespace='aws',
        meta_processor=aws_meta_processor,
    )

import argparse
from ast import arg
import sys

from awsume.awsumepy import hookimpl, safe_print
from awsume.awsumepy.lib.logger import logger
from awsume.awsumepy.lib.cache import read_aws_cache, valid_cache_session
from ykman.device import connect_to_device, list_all_devices
from yubikit.core.smartcard import SmartCardConnection
from yubikit.oath import OathSession
from ykman.cli.util import prompt_timeout


@hookimpl
def add_arguments(parser: argparse.ArgumentParser):
    try:
        parser.add_argument('-y', '--yubi',
                            action='store_true',
                            default=False,
                            dest='yubi',
                            help='Provide MFA code with Yubikey',
                            )
    except argparse.ArgumentError:
        pass


def _string_id(credential):
    return credential.id.decode("utf-8")


def _search(creds, query):
    hits = []
    for c in creds:
        cred_id = _string_id(c)
        if cred_id == query:
            return [c]
        if query.lower() in cred_id.lower():
            hits.append(c)
    return hits


@hookimpl
def pre_get_credentials(config: dict, arguments: argparse.Namespace, profiles: dict):
    if not arguments.yubi:
        return
    profile = profiles.get(arguments.target_profile_name)
    if not profile:
        return
    source_profile = profiles.get(profile.get("source_profile"))
    if not source_profile:
        return
    mfa_serial = profile.get("mfa_serial")
    if not mfa_serial:
        return

    cache_file_name = 'aws-credentials-' + \
        source_profile.get("aws_access_key_id")
    cache_session = read_aws_cache(cache_file_name)

    if valid_cache_session(cache_session):
        return

    for _, info in list_all_devices():
        if not info.version >= (5, 0, 0):
            continue

        connection, _, _ = connect_to_device(
            serial=info.serial, connection_types=[SmartCardConnection])
        with connection:
            session = OathSession(connection)

            entries = session.calculate_all()
            creds = _search(entries.keys(), mfa_serial)
            cred = creds[0]
            with prompt_timeout():
                # HOTP might require touch, we don't know.
                # Assume yes after 500ms.
                code = session.calculate_code(cred)
                arguments.mfa_token = code.value

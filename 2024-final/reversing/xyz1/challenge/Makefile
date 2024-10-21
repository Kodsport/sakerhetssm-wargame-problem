
default: do-test-sshd

libkrb5support.so.0: /lib/x86_64-linux-gnu/libkrb5support.so.0
	cp $< $@

libcrypto.so.3: /lib/x86_64-linux-gnu/libcrypto.so.3
	cp $< $@

libkrb5support-injected.so.0: libkrb5support.so.0 sshd-hook add-init.py
	python3 add-init.py $@ libkrb5support.so.0 sshd-hook

test-sshd: test-sshd.c libkrb5support-injected.so.0 libcrypto.so.3
	gcc -Wall -Wpedantic -o $@ $^

test-krb5: test-krb5.c libkrb5support-injected.so.0
	gcc -Wall -Wpedantic -o $@ $^

sshd-hook: sshd-init-hook.c
	gcc -O2 -fcf-protection=none -fno-plt -nostdlib -nodefaultlibs -fPIC -fvisibility=hidden --shared -o $@ $<

flag.h flag.c: generate-flag1.py
	python3 $< "SSM{part1_placeholder_flag}"

sshd-backdoor.so: sshd-crypto-hook.c flag.h flag.c
	gcc -O2 -fPIC --shared -fvisibility=hidden -o $@ -Iplthook plthook/plthook_elf.c $^

do-test-krb5: test-krb5
	./$^

do-test-sshd: test-sshd sshd-backdoor.so
	./$^

docker-build-run: Dockerfile
	docker build --build-arg FLAG1="SSM{based_0n_4_Tru3_St0ry}" --build-arg FLAG2="SSM{m4yb3_0ne_0f_MaNy}" -f $^ -t ssm_xyz .

docker-build-dist: Dockerfile
	docker build --build-arg FLAG1="SSM{based_0n_4_Tru3_St0ry}" -f $^ -t ssm_xyz_dist .

docker-run: docker-build-run
	docker run --rm -it --cap-add=SYS_PTRACE -p3000:22 ssm_xyz:latest

ssm_xyz.tar.gz: docker-build-dist
	docker run -d --rm --name ssm_xyz_export ssm_xyz_dist:latest
	docker export ssm_xyz_export | gzip > ssm_xyz.tar.gz
	docker stop ssm_xyz_export

clean:
	rm -f libcrypto.so.3 libkrb5support-injected.so.0 libkrb5support.so.0 sshd-backdoor.so sshd-hook test-krb5 test-sshd ssm_xyz.tar.gz flag.c flag.h

.PHONY: docker-build docker-run default test clean do-test-krb5 do-test-sshd


all: enc_flag md10.py

enc_flag: md10.tpl.py
	sed 's/FLAG_PLACEHOLDER/SSM{d0nt_3v3n_try_t0_@z%2?@5_gu3ss_y0u_l1ttl3...}/' md10.tpl.py > md10-secret.py
	python3 md10-secret.py
	rm md10-secret.py

md10.py: md10.tpl.py
	sed 's/FLAG_PLACEHOLDER/SSM{d0nt_3v3n_try_t0_xxxxxx_gu3ss_y0u_l1ttl3...}/' md10.tpl.py > md10.py

.PHONY: all

#include <linux/bpf.h>
#include <linux/ip.h>
#include <linux/ipv6.h>
#include <linux/in.h>
#include <linux/tcp.h>
#include <linux/udp.h>

#include <bpf/bpf_helpers.h>


SEC("prog")
int filter_flag(struct __sk_buff *skb) {
	char buf[64];

	bpf_copy_from_user(buf, 64, (void *)0x402004);
	//bpf_probe_write_user((void *)0x402004, buf, 64);
	
	bpf_printk("Flag: %s\n", buf);
	//bpf_printk("Ptr: %p\n", skb);

	if(buf[0] == 'n') // set to buf[0] == 'S' and see the difference in output
		bpf_sys_close(1); // test for each char-by-char brute

	return -1;
}

char _license[] SEC("license") = "GPL";

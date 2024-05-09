FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

# Update
RUN apt-get update --fix-missing && apt-get -y upgrade

# Dependencies
RUN apt-get install -y xinetd

# CTF user account
RUN groupadd -r ctf && useradd -r -g ctf ctf

# Add Resources
ADD ctf.xinetd /etc/xinetd.d/ctf
ADD redir.sh /home/ctf/redir.sh
ADD chall /home/ctf/chall

# Permissions
RUN chown -R root:ctf /home/ctf
RUN chmod 750 /home/ctf/redir.sh
RUN chmod 750 /home/ctf/chall

RUN service xinetd restart
CMD ["/usr/sbin/xinetd", "-dontfork"]

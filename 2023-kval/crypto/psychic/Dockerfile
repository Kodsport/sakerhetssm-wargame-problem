# Based on https://github.com/oracle/docker-images/blob/main/OracleJava/17/Dockerfile
FROM oraclelinux:8 as builder

LABEL maintainer="SÄK-SM by Sentor"

RUN set -eux; \
	dnf install -y tar; 

ENV LANG=en_US.UTF-8 \
    JAVA_URL=https://download.oracle.com/java/17/archive \
    JAVA_VERSION=17.0.2 \
	JAVA_HOME=/usr/java/jdk-17 \
    JAVA_SHA256=342e76bb9ded80aa1edd566efbae42f8f1c2366e19b9189e5941b45893b9861f \
	PATH=$JAVA_HOME/bin:$PATH \
    TOMCAT_VERSION=11.0.0-M3 \
    TOMCAT_HOME=/opt/tomcat \
    TOMCAT_SHA512=3ef407fccdb077268c62c55aea466c402db3050ab84711d8bf3cd45245c19ecfeba2ab8b768d4dabe1d11e0005dc94b469b5a30d2ae766b3aff4bb6220451a0c

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN set -eux; \
	ARCH="$(uname -m)" && \
    if [ "$ARCH" = "x86_64" ]; \
        then ARCH="x64"; \
    fi && \
    JAVA_PKG="$JAVA_URL"/jdk-"${JAVA_VERSION}"_linux-"${ARCH}"_bin.tar.gz ; \
	curl --output /tmp/jdk.tgz "$JAVA_PKG" && \
	echo "$JAVA_SHA256" */tmp/jdk.tgz | sha256sum -c; \
	mkdir -p "$JAVA_HOME"; \
	tar --extract --file /tmp/jdk.tgz --directory "$JAVA_HOME" --strip-components 1

RUN curl --output /tmp/tomcat.tgz https://dlcdn.apache.org/tomcat/tomcat-11/v"$TOMCAT_VERSION"/bin/apache-tomcat-"$TOMCAT_VERSION".tar.gz && \
	echo "$TOMCAT_SHA512" */tmp/tomcat.tgz | sha512sum -c; \
	mkdir -p "$TOMCAT_HOME"; \
	tar --extract --file /tmp/tomcat.tgz --directory "$TOMCAT_HOME" --strip-components 1; \
	sed -i 's/redirectPort="8443"/redirectPort="8443" server="Tomcat '"$TOMCAT_VERSION"'; Java '"$JAVA_VERSION"'"/' "$TOMCAT_HOME"/conf/server.xml

COPY src /tmp/src
RUN cd /tmp/src/main; \
    "$JAVA_HOME"/bin/javac -classpath "$TOMCAT_HOME"/lib/servlet-api.jar -d webapp/WEB-INF/classes java/Psychic.java; \
	cd webapp; \
	"$JAVA_HOME"/bin/jar -cvf psychic.war *

FROM oraclelinux:8

ENV LANG=en_US.UTF-8 \
    JAVA_HOME=/usr/java/jdk-17 \
    TOMCAT_HOME=/opt/tomcat \
    PATH=$JAVA_HOME/bin:$PATH

# Change for the SÄK-SM competition!
ENV FLAG=SSM{sentor_diggar_dr_who} \
    PUBLIC_KEY="MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEKY/2QKid9XCTRWCusDHUddgjWUTskYpY2wjWcgZ6vVfBlYRL0UhyLGbgBpucjGGjRAYoWRvn83f+GhAfiqmydw==" \
    PRIVATE_KEY="MEECAQAwEwYHKoZIzj0CAQYIKoZIzj0DAQcEJzAlAgEBBCBfWNacqAsGHMnGbWiZXR81mRvB4w/Icva0jGFPduwBxQ=="

COPY --from=builder $JAVA_HOME $JAVA_HOME
RUN set -eux; \
	dnf -y update; \
	dnf install -y freetype fontconfig; \
	rm -rf /var/cache/dnf; \
	ln -sfT "$JAVA_HOME" /usr/java/default; \
	ln -sfT "$JAVA_HOME" /usr/java/latest; \
	for bin in "$JAVA_HOME/bin/"*; do \
		base="$(basename "$bin")"; \
		[ ! -e "/usr/bin/$base" ]; \
		alternatives --install "/usr/bin/$base" "$base" "$bin" 20000; \
	done;

COPY --from=builder $TOMCAT_HOME $TOMCAT_HOME
RUN rm -rf $TOMCAT_HOME/webapps/*    
COPY --from=builder /tmp/src/main/webapp/psychic.war "$TOMCAT_HOME"/webapps/ROOT.war

EXPOSE 8080
CMD ["/opt/tomcat/bin/catalina.sh", "run"]

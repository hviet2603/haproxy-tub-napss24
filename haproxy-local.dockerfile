FROM alpine:3.20

WORKDIR /

# Runtime dependencies
RUN apk add --no-cache \
# @system-ca: https://github.com/docker-library/haproxy/pull/216
		ca-certificates \
	;

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    make \
    libc-dev \
    linux-headers \
    pcre-dev \
    pcre2-dev \
    openssl \
    openssl-dev \
    zlib-dev \
    lua5.4-dev \
    readline-dev

RUN set -eux; \
	addgroup --gid 99 --system haproxy; \
	adduser \
		--disabled-password \
		--home /var/lib/haproxy \
		--ingroup haproxy \
		--no-create-home \
		--system \
		--uid 99 \
		haproxy \
	; \
	mkdir /var/lib/haproxy; \
	chown haproxy:haproxy /var/lib/haproxy

COPY haproxy /haproxy

RUN cd /haproxy; \
    makeOpts=' \
        TARGET=linux-musl \
        USE_GETADDRINFO=1 \
        USE_LUA=1 LUA_INC=/usr/include/lua5.4 LUA_LIB=/usr/lib/lua5.4 \
        USE_OPENSSL=1 \
        USE_PCRE2=1 USE_PCRE2_JIT=1 \
        USE_PROMEX=1  \
    '; \
    make -j8 all $makeOpts \
    && make install install-bin $makeOpts 

#RUN runDeps="$( \
#        scanelf --needed --nobanner --format '%n#p' --recursive /usr/local \
#            | tr ',' '\n' \
#            | sort -u \
#            | awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
#    )"; \
#    apk add --no-network --virtual .haproxy-rundeps $runDeps; \
#    apk del --no-network .build-deps; 

#RUN rm -rf /haproxy

RUN mkdir -p /usr/local/etc/haproxy

EXPOSE 80 443

CMD ["haproxy", "-f", "/usr/local/etc/haproxy/haproxy.cfg"]
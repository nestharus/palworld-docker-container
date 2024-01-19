FROM nginx

ARG PALWORLD_ROUTE
ENV PALWORLD_ROUTE ${PALWORLD_ROUTE}

COPY ./config/default.conf /etc/nginx/conf.d/default.conf.template

RUN /bin/bash -c "envsubst '\$PALWORLD_ROUTE' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf"
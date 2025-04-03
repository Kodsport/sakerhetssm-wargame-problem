FROM node:21

COPY ./container /app

WORKDIR /app
RUN yarn

ENV STRIPE_KEY=sk_test_51OwkQtGQEtULAKKdGtMGfqhmvDPC4OHu9fE3TjLu1UJm8wpFVD8aSowCw4WQ1L9sIRiCieAfm0MDGqw658x4caNS00qFfVu2xh
ENV FLAG=SSM{spoopy_signatures}

ENTRYPOINT node index.js
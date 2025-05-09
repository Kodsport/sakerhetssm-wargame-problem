rm ./gogoworm-container.zip
zip -r gogoworm-container.zip ./container/ -x ./container/Dockerfile
printf "@ container/Dockerfile.handout\n@=container/Dockerfile\n" | zipnote -w gogoworm-container.zip
#!/bin/sh

echo "#!/bin/sh -ex

systemctl restart redis
redis-benchmark \$@ | tee \$LOG_FILE
systemctl stop redis

sed \"s/\\\"/ /g\" -i \$LOG_FILE" > redis
chmod +x redis

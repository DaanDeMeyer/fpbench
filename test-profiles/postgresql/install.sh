#!/bin/sh -ex

# Check if /var/lib/pgsql/data is empty.
if [ -z "$(ls -A /var/lib/pgsql/data)" ]; then
	postgresql-setup --initdb
fi

echo "#!/bin/sh -ex
systemctl restart postgresql
su postgres -c 'createdb pgbench'

su postgres -c 'pgbench -i \$1 \$2 -n pgbench'
su postgres -c 'pgbench -j \$NUM_CPU_CORES \$@ -n -T 120 -r pgbench' 2>&1 | tee \$LOG_FILE

su postgres -c 'dropdb pgbench'
systemctl stop postgresql" > postgresql
chmod +x postgresql

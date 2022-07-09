#!/bin/sh

echo "#!/bin/sh -ex
sysbench --threads=\$NUM_CPU_CORES --time=90 \$@ 2>&1 | tee \$LOG_FILE
echo \$? > ~/test-exit-status" > sysbench
chmod +x sysbench

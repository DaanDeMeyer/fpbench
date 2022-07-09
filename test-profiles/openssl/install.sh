#!/bin/sh

echo "#!/bin/sh -ex
openssl speed -multi \$NUM_CPU_CORES -seconds 30 \$@ 2>&1 | tee \$LOG_FILE 
echo \$? > ~/test-exit-status" > openssl
chmod +x openssl



#!/bin/sh

tar -zxvf pybench-2018-02-16.tar.gz

echo "#!/bin/sh -ex
cd pybench-2018-02-16/
python3 pybench.py \$@ 2>&1 | tee \$LOG_FILE
echo \$? > ~/test-exit-status" > pybench
chmod +x pybench

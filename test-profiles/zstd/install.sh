#!/bin/sh

cat > zstd <<EOT
#!/bin/sh -ex
unzip silesia.zip -d silesia
zstd -T\$NUM_CPU_CORES \$@ silesia/* 2>&1 | tee \$LOG_FILE
sed -i -e "s/\r/\n/g" \$LOG_FILE
rm -r silesia
EOT
chmod +x zstd

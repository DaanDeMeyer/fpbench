# How to run the benchmarks

- Clone the repository
- Install (mkosi)[https://github.com/systemd/mkosi]
- Install python3-pandas, python3-numpy and python3-click
- Clone mkosi repository at `../mkosi` relative to the fpbench repository root
- build systemd-nspawn from source and make the executable at `../systemd/build/systemd-nspawn` relative to the fpbench repository root

```
# Run benchmarks in Fedora 37 with frame pointers container
sudo ../mkosi/bin/mkosi --default no-omit-fp/mkosi.conf boot systemd.unit=bench.service
# Run benchmarks in Fedora 37 without frame pointers container
sudo ../mkosi/bin/mkosi --default omit-fp/mkosi.conf boot systemd.unit=bench.service
# Analyze and display the results
./analyze.py bench.json
```

Results:

```
    Benchmark                        Result       Mean (omit / no-omit) Mean Difference Std Dev (omit / no-omit) Num Tests (omit / no-omit)
      blender                  Duration (s)              392.75 / 400.2            1.9%        0.2111% / 0.4299%                      4 / 5
        botan           AES-256 (MB/second)        5721.316 / 5694.8384            0.5%         0.486% / 0.6865%                     8 / 10
        botan AES-256 [openssl] (MB/second)       5598.8459 / 5566.2604            0.6%        1.1385% / 1.2932%                     8 / 10
        botan          Blowfish (MB/second)         231.6743 / 231.6037            0.0%        1.2896% / 1.2925%                     8 / 10
        botan          CAST-256 (MB/second)             90.6434 / 90.63            0.0%        0.1703% / 0.1823%                     8 / 10
        botan  ChaCha20Poly1305 (MB/second)         642.0556 / 641.6031            0.1%        0.5257% / 0.8547%                     8 / 10
        botan            KASUMI (MB/second)           78.1414 / 78.0889            0.1%          1.586% / 1.508%                     8 / 10
        botan           Twofish (MB/second)         176.0366 / 177.4218            0.8%        2.3791% / 0.5486%                     8 / 10
          gcc                  Duration (s)         246.9607 / 252.9407            2.4%        0.0859% / 0.0395%                      4 / 4
      openssl       aes-128-cbc (MB/second)       1688.5987 / 1688.0522            0.0%         0.0229% / 0.035%                      4 / 5
      openssl       aes-192-cbc (MB/second)       1429.2144 / 1429.2428            0.0%        0.0433% / 0.0139%                      4 / 5
      openssl       aes-256-cbc (MB/second)       1238.3488 / 1238.5301            0.0%          0.02% / 0.0204%                      4 / 5
      openssl  camellia-128-cbc (MB/second)         204.8652 / 204.8495            0.0%        0.0537% / 0.0136%                      4 / 5
      openssl  camellia-192-cbc (MB/second)          152.7494 / 152.742            0.0%        0.0177% / 0.0231%                      4 / 5
      openssl  camellia-256-cbc (MB/second)         152.7787 / 152.8181            0.0%        0.0293% / 0.0424%                      4 / 5
      openssl          des-ede3 (MB/second)            28.481 / 28.4732            0.0%        0.5417% / 0.3393%                      4 / 5
      openssl             ghash (MB/second)        14061.5 / 14057.4878            0.0%        0.1272% / 0.0857%                      4 / 5
      openssl         hmac(md5) (MB/second)         720.2127 / 720.1047            0.0%        0.0311% / 0.0631%                      4 / 5
      openssl               md5 (MB/second)          724.5759 / 724.535            0.0%        0.0195% / 0.0279%                      4 / 5
      openssl              rand (MB/second)       5909.9436 / 5928.8331            0.3%        0.0609% / 0.2412%                      4 / 5
      openssl              sha1 (MB/second)       1665.9534 / 1666.3307            0.0%        0.0279% / 0.0259%                      4 / 5
      openssl            sha256 (MB/second)       1317.9472 / 1317.9478            0.0%         0.0374% / 0.022%                      4 / 5
      openssl            sha512 (MB/second)         644.6275 / 644.3334            0.0%         0.042% / 0.0419%                      4 / 5
      pgbench       Average Latency (in ms)             2.7258 / 2.7633            1.4%        4.6027% / 4.5057%                    12 / 15
      pgbench       Transactions per second        7356.0942 / 7252.962            1.4%        4.4527% / 4.4865%                    12 / 15
pyperformance                          2to3             0.2823 / 0.2886            2.2%        0.4236% / 0.2374%                      4 / 5
pyperformance                     chameleon             0.0075 / 0.0077            2.9%        0.3635% / 0.8713%                      4 / 5
pyperformance                         chaos             0.0757 / 0.0769            1.5%        0.3042% / 0.1542%                      4 / 5
pyperformance                  crypto_pyaes             0.0808 / 0.0836            3.5%        0.3391% / 0.3949%                      4 / 5
pyperformance                     deltablue             0.0041 / 0.0043            5.9%        0.0402% / 0.5238%                      4 / 5
pyperformance               django_template              0.0365 / 0.039            6.6%        0.4204% / 0.1759%                      4 / 5
pyperformance                   dulwich_log              0.065 / 0.0673            3.5%        0.2735% / 0.5403%                      4 / 5
pyperformance                      fannkuch             0.4175 / 0.4276            2.4%        0.1763% / 0.9582%                      4 / 5
pyperformance                         float             0.0829 / 0.0862            3.9%        0.4386% / 0.8319%                      4 / 5
pyperformance                   genshi_text              0.027 / 0.0269            0.6%        0.3068% / 0.5333%                      4 / 5
pyperformance                    genshi_xml              0.0614 / 0.063            2.6%        0.2192% / 0.2014%                      4 / 5
pyperformance                            go             0.1519 / 0.1552            2.2%        0.2472% / 1.1143%                      4 / 5
pyperformance                        hexiom              0.007 / 0.0073            4.2%         0.214% / 0.2223%                      4 / 5
pyperformance                      html5lib             0.0674 / 0.0698            3.5%        0.1654% / 0.2173%                      4 / 5
pyperformance                    json_dumps              0.012 / 0.0126            5.2%        0.5807% / 0.7049%                      4 / 5
pyperformance                    json_loads                   0.0 / 0.0            5.6%        0.1126% / 0.4373%                      4 / 5
pyperformance                logging_format                   0.0 / 0.0            4.1%        0.3382% / 0.1203%                      4 / 5
pyperformance                logging_silent                   0.0 / 0.0            3.6%         0.321% / 0.3155%                      4 / 5
pyperformance                logging_simple                   0.0 / 0.0            4.7%        0.3069% / 0.1819%                      4 / 5
pyperformance                          mako              0.0106 / 0.011            3.7%        1.0228% / 0.3132%                      4 / 5
pyperformance                meteor_contest              0.1107 / 0.115            3.8%        0.1211% / 0.1522%                      4 / 5
pyperformance                         nbody             0.0974 / 0.1066            8.6%        0.5261% / 1.6923%                      4 / 5
pyperformance                       nqueens             0.0989 / 0.1007            1.8%         0.1031% / 0.318%                      4 / 5
pyperformance                       pathlib             0.0174 / 0.0182            4.5%        0.8631% / 0.6443%                      4 / 5
pyperformance                        pickle                   0.0 / 0.0            7.1%        0.5275% / 0.4534%                      4 / 5
pyperformance                   pickle_dict                   0.0 / 0.0            3.8%        0.2149% / 0.3785%                      4 / 5
pyperformance                   pickle_list                   0.0 / 0.0            0.4%        0.6997% / 0.3421%                      4 / 5
pyperformance            pickle_pure_python             0.0003 / 0.0003            4.3%        0.1638% / 0.6242%                      4 / 5
pyperformance                      pidigits             0.1953 / 0.1964            0.6%         0.0255% / 0.039%                      4 / 5
pyperformance                       pyflate             0.4697 / 0.4817            2.5%         1.202% / 0.6028%                      4 / 5
pyperformance                python_startup              0.009 / 0.0091            1.4%        1.3195% / 0.8585%                      4 / 5
pyperformance        python_startup_no_site             0.0063 / 0.0064            0.8%        0.5466% / 0.9968%                      4 / 5
pyperformance                      raytrace             0.3316 / 0.3454            4.0%        0.2206% / 0.1397%                      4 / 5
pyperformance                 regex_compile             0.1515 / 0.1568            3.4%         0.095% / 0.2667%                      4 / 5
pyperformance                     regex_dna             0.1636 / 0.1712            4.4%        0.1309% / 0.1551%                      4 / 5
pyperformance                  regex_effbot             0.0025 / 0.0027            6.0%         0.072% / 0.2793%                      4 / 5
pyperformance                      regex_v8             0.0185 / 0.0195            5.1%        0.0692% / 0.3962%                      4 / 5
pyperformance                      richards              0.0478 / 0.051            6.3%        0.1424% / 0.3229%                      4 / 5
pyperformance                   scimark_fft             0.3213 / 0.3517            8.6%        0.3755% / 0.3829%                      4 / 5
pyperformance                    scimark_lu             0.1288 / 0.1366            5.7%        0.3641% / 0.8092%                      4 / 5
pyperformance           scimark_monte_carlo             0.0728 / 0.0781            6.8%        0.2093% / 0.8044%                      4 / 5
pyperformance                   scimark_sor             0.1277 / 0.1337            4.5%        0.3221% / 0.2813%                      4 / 5
pyperformance       scimark_sparse_mat_mult             0.0047 / 0.0052            9.5%        0.3764% / 0.5924%                      4 / 5
pyperformance                 spectral_norm              0.109 / 0.1182            7.7%        0.2437% / 1.1068%                      4 / 5
pyperformance        sqlalchemy_declarative             0.1323 / 0.1358            2.6%        0.1379% / 0.3609%                      4 / 5
pyperformance         sqlalchemy_imperative             0.0176 / 0.0183            3.4%        0.4265% / 0.2622%                      4 / 5
pyperformance                  sqlite_synth                   0.0 / 0.0            7.6%        0.4354% / 1.4469%                      4 / 5
pyperformance                  sympy_expand             0.5166 / 0.5408            4.5%        0.0961% / 0.2924%                      4 / 5
pyperformance               sympy_integrate             0.0219 / 0.0227            3.4%        0.1906% / 0.4094%                      4 / 5
pyperformance                     sympy_str              0.309 / 0.3218            4.0%        0.1631% / 0.1377%                      4 / 5
pyperformance                     sympy_sum             0.1654 / 0.1717            3.7%        0.1806% / 0.2936%                      4 / 5
pyperformance                         telco             0.0075 / 0.0079            5.1%         0.7319% / 0.536%                      4 / 5
pyperformance                  tornado_http             0.1148 / 0.1165            1.5%         0.299% / 0.5194%                      4 / 5
pyperformance               unpack_sequence                   0.0 / 0.0            1.2%        0.2169% / 1.0563%                      4 / 5
pyperformance                      unpickle                   0.0 / 0.0            4.4%          0.48% / 0.3702%                      4 / 5
pyperformance                 unpickle_list                   0.0 / 0.0            3.8%        0.0715% / 0.8382%                      4 / 5
pyperformance          unpickle_pure_python             0.0003 / 0.0003            3.2%        0.0958% / 0.1659%                      4 / 5
pyperformance            xml_etree_generate             0.0845 / 0.0902            6.3%        0.0764% / 0.5246%                      4 / 5
pyperformance           xml_etree_iterparse             0.1093 / 0.1131            3.3%         0.4933% / 0.648%                      4 / 5
pyperformance               xml_etree_parse              0.1671 / 0.173            3.4%         0.2738% / 0.797%                      4 / 5
pyperformance             xml_etree_process             0.0617 / 0.0658            6.2%         0.3025% / 1.196%                      4 / 5
        redis     GET (requests per second) 2236723.2778 / 2214881.0667            1.0%        0.3753% / 0.5794%                     9 / 15
        redis    LPOP (requests per second)  1604092.6667 / 1596965.076            0.4%        0.5202% / 0.4415%                     9 / 15
        redis   LPUSH (requests per second) 1699474.6533 / 1698218.7593            0.1%        2.1367% / 0.4933%                     9 / 15
        redis    SADD (requests per second) 2041983.3333 / 2063767.1413            1.1%        0.5224% / 0.4361%                     9 / 15
        redis     SET (requests per second)   1843387.11 / 1835161.7687            0.4%        0.8817% / 0.6366%                     9 / 15
         zstd      Compression Speed (MB/s)           259.7067 / 256.09            1.4%        1.6995% / 1.6875%                    30 / 50
         zstd    Decompression Speed (MB/s)           1820.99 / 1829.85            0.5%        0.2523% / 0.4443%                    30 / 50
```

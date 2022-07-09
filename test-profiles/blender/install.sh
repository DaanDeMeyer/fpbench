#!/bin/sh

set -x

unzip -o cycles_benchmark_20160228.zip

mv benchmark/bmw27/*.blend  ~
mv benchmark/classroom/*.blend ~
mv benchmark/fishy_cat/*.blend ~
mv benchmark/pabellon_barcelona/*.blend ~
rm -rf benchmark

echo "#!/bin/bash -ex
BLEND_ARGS=\$@

COMPUTE_TYPE=\"NONE\"
BLEND_ARGS=\${BLEND_ARGS/_gpu/_cpu}

echo \"import bpy
bpy.context.preferences.addons['cycles'].preferences.get_devices()
bpy.context.preferences.addons['cycles'].preferences.compute_device_type = '\$COMPUTE_TYPE'
bpy.context.preferences.addons['cycles'].preferences.devices[0].use = True

bpy.ops.wm.save_userpref()\" > setgpu.py

blender -b --python setgpu.py 

blender \$BLEND_ARGS | tee \$LOG_FILE
rm -f output.test" > blender
chmod +x blender

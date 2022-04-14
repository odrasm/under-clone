/usr/local/src/underground/tools/underground init aio
/usr/local/src/underground/tools/underground bootstrap victoria -m baremetal -n ens3 -e "@/usr/local/share/underground/examples/underground_baremetal_vars.yml"
/usr/local/src/underground/tools/underground build -t dib -e underground_baremetal_image="ipa"
/usr/local/src/underground/tools/underground configure
/usr/local/src/underground/tools/underground deploy
/usr/local/src/underground/tools/underground post-deploy
/usr/local/src/underground/tools/underground build -t dib -e underground_baremetal_image="underground" -e baremetal_image_upload="true"

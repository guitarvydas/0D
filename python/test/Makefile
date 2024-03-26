das2jsondir=../../das2json/
0Dsrc = ../
STD = ../std

0D = ${0Dsrc}/gensym.py \
    ${0Dsrc}/datum.py \
    ${0Dsrc}/message.py \
    ${0Dsrc}/container.py \
    ${0Dsrc}/registry.py \
    ${0Dsrc}/process.py \
    ${0Dsrc}/0d.py \
    ${STD}/std.py \
    ${STD}/lib.py \
    ${STD}/fakepipe.py \
    ${STD}/transpiler.py \
    ${STD}/stock.py \
    ${STD}/run.py

all :
	clear
	make dev0d4

main: jsons
	# *** building _.py
	@cat ${0D} ./main.py > _.py
	python3 _.py "0D was here" main helloworld0d.drawio.json transpile.drawio.json

jsons: simple0d.drawio simple0d2.drawio simple0d3.drawio simple0d4.drawio helloworld0d.drawio transpile.drawio vsh0d.drawio arith0d.drawio
	# *** building jsons
	@${das2jsondir}/das2json simple0d.drawio
	@${das2jsondir}/das2json simple0d2.drawio
	@${das2jsondir}/das2json simple0d3.drawio
	@${das2jsondir}/das2json simple0d4.drawio
	@${das2jsondir}/das2json helloworld0d.drawio
	@${das2jsondir}/das2json transpile.drawio
	@${das2jsondir}/das2json vsh0d.drawio
	@${das2jsondir}/das2json arith0d.drawio
	@${das2jsondir}/das2json ../std/transpile.drawio

install:
	./makedas2json.bash ${das2jsondir}



# dev helpers

dev4: jsons
	# *** building _.py
	@cat ${0D} ./main.py > _.py
	python3 _.py ex1.math main arith0d.drawio.json transpile.drawio.json

dev3: jsons
	# *** building _.py
	@cat ${0D} ./main.py > _.py
	python3 _.py "pt was here" main vsh0d.drawio.json transpile.drawio.json

dev2: jsons
	# *** building _.py
	@cat ${0D} ./main.py > _.py
	python3 _.py "pt was here" main helloworld0d.drawio.json transpile.drawio.json

dev1a: jsons
	# *** building _.py
	@cat ${0D} ./main.py > _.py
	python3 _.py "pt was here" main simple0d3.drawio.json

dev1: jsons
	# *** building _.py
	@cat ${0D} ./main.py > _.py
	python3 _.py "pt was here" main simple0d2.drawio.json

dev0: jsons
	# *** building _.py
	@cat ${0D} ./main.py > _.py
	python3 _.py "@" main simple0d.drawio.json

dev0d4: jsons
	# *** building _.py
	@cat ${0D} ./main.py > _.py
	python3 _.py "@" main simple0d4.drawio.json


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
    ${STD}/run.py \

dev: jsons
	cat ${0D} ./main.py > _.py
	python3 _.py "pt was here" main simple0d2.drawio.json

dev0: jsons
	cat ${0D} ./main.py > _.py
	python3 _.py "pt was here" main helloworld0d.drawio.json transpile.drawio.json

all:
	cat ${0D} ./main.py > _.py
	python3 _.py "Hello World from 0D" main simple0d.drawio.json

jsons: simple0d.drawio simple0d2.drawio helloworld0d.drawio transpile.drawio
	./makedas2json.bash ${das2jsondir}
	${das2jsondir}/das2json simple0d.drawio
	${das2jsondir}/das2json simple0d2.drawio
	${das2jsondir}/das2json helloworld0d.drawio
	${das2jsondir}/das2json transpile.drawio

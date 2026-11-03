# Лаборатори 5 · Python орчин ба Mini-GIS

- python -m minigis — Lab 4-ийн жишээ давхаргуудыг нээнэ. File цэсээр .shp файл эсвэл хавтас нэмнэ. View цэсээр томруулах, жижигрүүлэх, нийт хүрээнд харах, сонгосон давхарга хаах үйлдэл хийнэ. Газрын зургийг хулганаар чирнэ.
- python -m minigis --no-gui — Давхаргын объектын тоо ба шугам/цагирагийн нийт уртыг хэвлэнэ.
- python debug_demo.py — SyntaxError, ZeroDivisionError, FileNotFoundError, finally, модулийн хайлтын зам болон ZIP файлыг туршина.
- python -m idlelib — IDLE Shell нээнэ. File → Open цэсээр debug_demo.py нээгээд F5 дарна. Options → Configure IDLE цэсээр өнгө, фонт, доголыг туршина.

## Багцын бүтэц

Dataset (.shp, .shx, .dbf) → Layer → Feature. Feature-ээс Point ба Polyline, Polyline-аас Polygon удамшина. Polygon нь vis()-ийг өөрчилж, уртын тооцоог удамшуулна. read_shapefile.py геометр уншина, app.py цонх ба үйлдлүүдийг удирдана, __main__.py багцыг эхлүүлнэ.

Номын Mini-GIS болон Fairfax өгөгдлийн оронд Python 3 Mini-GIS-lite, Lab 4-ийн зохиомол давхаргуудыг ашигласан. Номын хоёр давхаргын огтлолцлын хэрэгсэл энэ хувилбарт байхгүй.

# limiarizacao

### Requisitos
Para executar o projeto será necessário instalar:
- [Python 3](https://www.python.org/download/releases/3.0/)
- [OpenCV](https://opencv.org/releases/)
- [Numpy](https://numpy.org/install/)

### Build
Para executar o projeto, utilize o comando:
```shell
python3 main.py -i imagem_entrada -t algoritmo -b politica
```
**imagem_entrada** é a imagem de entrada no formato png

**algoritmo** é o algoritmo de limiarização [rc, otsu]

**politica** é a política de limiarização [bin, trunc, zero]
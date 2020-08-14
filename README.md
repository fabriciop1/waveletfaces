# Uma análise extensa de funções wavelet para a tarefa de reconhecimento facial

Esse projeto foi parte do trabalho de conclusão de curso na Universidade Federal Rural de Pernambuco

Neste projeto de aprendizagem de máquina, são combinados métodos de extração de características como o PCA e o LDA em conjunto com a Transformada Wavelet Discreta para a tarefa de reconhecimento facial. Uma análise estatística de diferentes funções de decomposição wavelet é realizada em 7 diferentes bases de dados com diversas características.
Um total de 4 classificadores foram utilizados para medir a capacidade do método de extração.

## Tecnologias Utilizadas

* Linguagem Python v. 2.7;
* Numpy e OpenCV;
* Sklearn para construção dos modelos;
* Biblioteca PYWT para análise das funções.

## Métodos de Extração de Características Utilizados

* Principal Component Analysis (PCA);
* Linear Discriminant Analysis (LDA);
* Discrete Wavelet Transform (DWT).

Visualização dos 5 primeiros eigenvectors após o PCA (meio) e a dispersão entre classes após LDA (baixo)
com 5 classes diferentes da base de dados Georgia Tech (topo).

![eigenfisher](pics/eigenfisher.jpg)<br/>  

```python
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.decomposition import PCA
pca_m = PCA(n_components=50)
pca_m.fit(training_imgs)
lda = LinearDiscriminantAnalysis(n_components=100)
lda.fit(training_imgs, classes_treino)
```

Imagem original (esquerda) e decomposição em um nível pela DWT (direita) com as funções de haar (topo-esquerda), bior3.7 (baixo-esquerda), db5 (topo-direita) e sym16 (baixo-direita).

![waveletfaces](pics/dwt_decomp.png)<br/>

```python
import pywt
import cv2
img = cv2.imread(file)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
coeffs = pywt.wavedec2(img, wavelet, level=1)
```

## Combinações de Métodos Utilizados

* Apenas DWT;
* DWT + PCA;
* DWT + LDA;
* DWT + PCA + LDA, nessa ordem.

## Classificadores Utilizados

* Nearest Neighbor Classfier (1-NN): Classificador de distância;
* Gaussian Naive Bayes (GNB): Classificador probabilístico; 
* Support Vector Machines (SVM): Classificador com máquina de vetores suporte;
* Random Forest Classifier (RFC): Classificador com árvores de decisão.

## Bases de Dados Consideradas

* [ORL](http://cam-orl.co.uk/facedatabase.html);
* [AR Face Database](http://www2.ece.ohio-state.edu/~aleix/ARdatabase.html);
* [Essex Faces95](https://cswww.essex.ac.uk/mv/allfaces/faces95.html);
* [Yale B Face Dataset](http://vision.ucsd.edu/~leekc/ExtYaleDatabase/ExtYaleB.html);
* [Georgia Tech Face Dataset](http://www.anefian.com/research/face_reco.htm);
* [LFW - Labeled Faces in The Wild](http://vis-www.cs.umass.edu/lfw/);
* [CASIA-WebFace](https://drive.google.com/open?id=1Of_EVz-yHV7QVWQGihYfvtny9Ne8qXVz);
* [Youtube_Faces](https://www.cs.tau.ac.il/~wolf/ytfaces/).

As funções wavelets que maximizam a acurácia para a tarefa de reconhecimento são então avaliadas com um intervalo de confiança de 95%.
Foram consideradas mais de 4.000.000 de taxas de acurácia média para avaliação e os experimentos mostraram que algumas dessas funções não são adequadas para a tarefa.
No entanto, outras funções são significativamente diferentes para os testes específicos considerados na pesquisa.
A função wavelet rbio3.1 da família Reverse Biorthogonal foi a que mais apresentou resultados de acurácia mais altos se comparada com as outras funções.

## Execução

### Requisitos

  * Python 2.7;
  * Bases de dados com imagens alinhadas e cortadas com detecção da face.
  
Primeiro, tenha certeza que as bibliotecas sklearn, pywt, cv2, csv, numpy e math estão instaladas corretamente.
Caso não esteja, instale-as utilizando o pip pela linha de comando, onde `<library>` é qualquer uma das bibliotecas descritas:

```bash
pip install <library>
```
No arquivo `training_test_divider.py` modifique o número de classes da base de dados avaliada e quantos holdouts separar para treino e teste para o algoritmo.
Modifique também o caminho da base de dados no sistema. Por padrão, 33% das imagens de cada classe são consideradas para treino e o restante para testes.
Porém, caso deseje mais ou menos, basta alterar a linha 52.

Execute tal arquivo:
```bash
python training_test_divider.py
```

No arquivo `__main__.py` altere a linha 181 para o nome do arquivo .txt gerado pela execução do arquivo anterior e quais níveis utilizar na linha 190.

Execute tal arquivo, pela linha de comando, enquanto dentro da pasta principal do projeto:

```bash
python __main__.py
```

Por padrão, os níveis 1-6 e todas as combinações de métodos serão executadas para os arquivos .txt já existentes, com apenas 1 holdout. 
Arquivos .csv serão gerados com os resultados para todos os wavelets da biblioteca pywt.



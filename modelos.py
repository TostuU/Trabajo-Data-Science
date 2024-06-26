# -*- coding: utf-8 -*-
"""Tarea Preprocesamiento de datos.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dzA7tfUYBc_AYimWaBSN06ekWhqJKk62

# ***NAIVE BAYES***
"""

# Importando las bibliotecas necesarias para los 3 metodos
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve,auc
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
import graphviz
from sklearn import tree
from sklearn.tree import plot_tree
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
import ipywidgets as widgets
import matplotlib.pyplot as plt

# Cargando el conjunto de datos desde una URL
url = 'https://raw.githubusercontent.com/adiacla/bigdata/master/DatosEmpresaChurn.csv'
df = pd.read_csv(url)

# Imprimiendo las primeras filas del conjunto de datos
print(df.head())

# Commented out IPython magic to ensure Python compatibility.
#GRAFICAS
# %matplotlib inline
df.plot()

# Imputando los valores NaN con la media de la columna
df = df.replace(',', '.', regex=True)
df = df.astype(float)
imputer = SimpleImputer(strategy='mean')
df = pd.DataFrame(imputer.fit_transform(df), columns = df.columns)

# Codificando las columnas categóricas
le = LabelEncoder()
for column in df.columns:
    if df[column].dtype == type(object):
        df[column] = le.fit_transform(df[column])

# Normalizando el conjunto de datos
scaler = StandardScaler()
df = pd.DataFrame(scaler.fit_transform(df), columns = df.columns)

# Imprimiendo las primeras filas del conjunto de datos normalizado
print(df.head())

# Creando un gráfico de pares para visualizar las relaciones entre las características
sns.pairplot(df)
plt.show()

# Imprimiendo las columnas del conjunto de datos
print(df.columns)

# Dividiendo el conjunto de datos en conjuntos de entrenamiento y prueba
X = df.drop('TARGET CLASS', axis=1)
y = df['TARGET CLASS']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Convirtiendo y_train a enteros
y_train = y_train.astype(int)
# Creando y entrenando el modelo de Naive Bayes Gaussiano
modeloNB = GaussianNB()
modeloNB.fit(X_train, y_train)

# Haciendo predicciones con el modelo
y_pred = modeloNB.predict(X_test)

# Convirtiendo y_test a enteros
y_test = y_test.astype(int)

# Creando una matriz de confusión para evaluar las predicciones
cm = confusion_matrix(y_test, y_pred)

# Visualizando la matriz de confusión
sns.heatmap(cm, annot=True)
plt.show()

# Calculando la precisión del modelo
accuracy = accuracy_score(y_test, y_pred)

# Imprimiendo la precisión del modelo
print(f'La precisión del modelo es: {accuracy}')

# Haciendo predicciones con el modelo
y_pred_proba_NB = modeloNB.predict_proba(X_test)[::,1]

# Calculando y dibujando la curva ROC
fpr, tpr, _ = roc_curve(y_test, y_pred_proba_NB)
auc_score = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f"Naive Bayes, AUC={auc_score:.3f}")
plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
plt.xlabel('Tasa de falsos positivos')
plt.ylabel('Tasa de verdaderos positivos')
plt.title('Característica Operativa del Receptor')
plt.legend(loc=4)
plt.show()

#Guardamos el modelo entrenado en un archivo
pickle.dump(modeloNB,open('modeloNB','wb'))

"""# ***ARBOLES DE DECISION***"""

# Creando y entrenando el modelo de árbol de decisión
modeloArbol = DecisionTreeClassifier(random_state=0)
modeloArbol.fit(X_train, y_train)

# Haciendo predicciones con el modelo
y_pred = modeloArbol.predict(X_test)

modeloArbol.score(X_test,y_test)

# Creando una matriz de confusión para evaluar las predicciones
cm = confusion_matrix(y_test, y_pred)

# Visualizando la matriz de confusión
sns.heatmap(cm, annot=True)
plt.show()

# Calculando la precisión del modelo
accuracy = accuracy_score(y_test, y_pred)

# Imprimiendo la precisión del modelo
print(f'La precisión del modelo es: {accuracy}')

# Haciendo predicciones con el modelo
y_pred_proba_arb = modeloArbol.predict_proba(X_test)[::,1]

# Calculando y dibujando la curva ROC
fpr, tpr, _ = roc_curve(y_test, y_pred_proba_arb)
auc_score = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f"Arbol de decisiones, AUC={auc_score:.3f}")
plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
plt.xlabel('Tasa de falsos positivos')
plt.ylabel('Tasa de verdaderos positivos')
plt.title('Característica Operativa del Receptor')
plt.legend(loc=4)
plt.show()

"""# ***BOSQUES ALEATORIOS***"""

# Creando y entrenando el modelo de Random Forest
modeloBosque = RandomForestClassifier(n_estimators=10,
                               criterion="gini",
                               bootstrap=True,
                               max_features="sqrt",
                               max_samples=0.8,
                               oob_score=True,
                               random_state=0)
modeloBosque.fit(X_train, y_train)

# Haciendo predicciones con el modelo
y_pred = modeloBosque.predict(X_test)

# Creando una matriz de confusión para evaluar las predicciones
cm = confusion_matrix(y_test, y_pred)

# Visualizando la matriz de confusión
sns.heatmap(cm, annot=True)
plt.show()

# Calculando la precisión del modelo
accuracy = accuracy_score(y_test, y_pred)

# Imprimiendo la precisión del modelo
print(f'La precisión del modelo es: {accuracy}')

modeloBosque.fit(X_train, y_train)

#Graficando algunos (NO TODOS) arboles del bosque aleatorio
for i in modeloBosque.estimators_:
    tree.plot_tree(i)
    plt.show()

# Haciendo predicciones con el modelo
y_pred_proba_bos = modeloBosque.predict_proba(X_test)[::,1]

# Calculando y dibujando la curva ROC
fpr, tpr, _ = roc_curve(y_test, y_pred_proba_bos)
auc_score = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f"Bosque Aleatorio, AUC={auc_score:.3f}")
plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
plt.xlabel('Tasa de falsos positivos')
plt.ylabel('Tasa de verdaderos positivos')
plt.title('Caracteristica operativa del receptor')
plt.legend(loc=4)
plt.show()
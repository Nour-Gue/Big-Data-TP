FROM python:3.8.20
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir pandas numpy matplotlib seaborn scikit-learn jupyter notebook
CMD ["jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", "tp3.ipynb"]

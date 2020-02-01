# Requirements for plots :

- For 3d plots in `plots/*` :
    ```bash
    pip3 install plotly
    ```
    Plot with :
    ```bash
    python3 file.py
    ```

- For interactive 3d plots in `plots/jupyter/*` :

    ```bash
    pip3 install notebook
    pip3 install ipywidgets
    ```
    in root of the project :
    ```bash
    jupyter nbextension enable --py widgetsnbextension --sys-prefix
    jupyter nbextension enable --py plotlywidget --sys-prefix
    ```
    Plot with :
    ```bash
    jupyter notebook
    ```
    Then open .ipynb file, and `ctrl+enter` in a chunk of code to run 

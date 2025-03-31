import pandas as pd
import streamlit as st
from datetime import datetime
from io import BytesIO, StringIO
import OTMrunReport as rr
import requests
st.set_page_config(layout="wide")
logo_base64 = """
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"""
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo de la Empresa" width="300">
    </div>
    """,
    unsafe_allow_html=True,
)
# Acceder a las credenciales desde los secretos
usernames = st.secrets["credentials"]["usernames"]
passwords = st.secrets["credentials"]["passwords"]

# Función para verificar las credenciales
def authenticate(username, password):
    if username in usernames:
        index = usernames.index(username)
        if passwords[index] == password:
            return True
    return False

# Inicializar el estado de sesión si no existe
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Si el usuario no está autenticado, mostrar el formulario de inicio de sesión
if not st.session_state.authenticated:
    st.title("Iniciar sesión")
    username_input = st.text_input("Usuario")
    password_input = st.text_input("Contraseña", type="password")
    if st.button("Iniciar sesión"):
        if authenticate(username_input, password_input):
            st.session_state.authenticated = True
            st.success(f"Bienvenid@, {username_input}!")
            st.rerun()  # Recarga la página para reflejar el cambio
        else:
            st.error("Usuario o contraseña incorrectos")
else:
    # Contenido de la aplicación para usuarios autenticados
    provisiones = st.secrets["google_drive"]["provisiones"]
    mapeo = st.secrets["google_drive"]["mapeo"]
    base = st.secrets["google_drive"]["base"]

    @st.cache_data
    def cargar_datos_pro(url, sheet_name=None):
        response = requests.get(url)
        response.raise_for_status()  # Verifica si hubo algún error en la descarga
        archivo_excel = BytesIO(response.content)
        return pd.read_excel(archivo_excel, sheet_name=sheet_name, engine="openpyxl")

    @st.cache_data
    def cargar_datos(url):
            response = requests.get(url)
            response.raise_for_status()  # Verifica si hubo algún error en la descarga
            archivo_excel = BytesIO(response.content)
            return pd.read_excel(archivo_excel, engine="openpyxl")

    # Especifica la hoja que deseas cargar
    hoja_deseada = "Base provisiones"

    df_provisiones = cargar_datos_pro(provisiones, sheet_name=hoja_deseada)
    df_mapeo = cargar_datos(mapeo)
    df_base = cargar_datos(base)
    @st.cache_data
    def get_xtr_as_dataframe():
        # 1. Obtener el reporte (contenido del archivo XTR)
        headers = rr.headers(st.secrets["RR"]["usuario_otm"], st.secrets["RR"]["contrasena_otm"])
        algo = rr.runReport(st.secrets["RR"]["path"], 'ekck.fa.us6', headers)

        # 2. Verificar el tipo de "algo"
        if isinstance(algo, bytes):
            algo = algo.decode('utf-8')  # Convertir bytes a string

        # 3. Convertir el contenido XTR a DataFrame
        try:
            xtr_io = StringIO(algo)  # Crear un buffer en memoria
            df = pd.read_csv(xtr_io, sep=",", low_memory=False)  # Ajusta el delimitador aquí
        except Exception as e:
            st.error(f"Error al procesar el archivo XTR: {e}")
            return None

        return df, algo

    df, algo = get_xtr_as_dataframe()
    df_original = df.copy()

        # Selección y renombrado de columnas
    columnas_d = ['DEFAULT_EFFECTIVE_DATE', 'DEFAULT_EFFECTIVE_DATE', 'SEGMENT1', 'SEGMENT2', 'SEGMENT3', 'SEGMENT5', 'CREDIT', 'DEBIT']
    nuevo_nombre = ['Año_A','Mes_A', 'Empresa_A', 'CeCo_A', 'Proyecto_A', 'Cuenta_A', 'Credit_A', 'Debit_A']
        # Validar que las columnas existen en el DataFrame
    columnas_disponibles = [col for col in columnas_d if col in df.columns]
        # Seleccionar y renombrar las columnas
    df = df[columnas_disponibles]
    df.columns = nuevo_nombre[:len(columnas_disponibles)]
    df['Cuenta_A'] = pd.to_numeric(df['Cuenta_A'], errors='coerce')
    df['Debit_A'] = pd.to_numeric(df['Debit_A'], errors='coerce')
    df['Credit_A'] = pd.to_numeric(df['Credit_A'], errors='coerce')

        # Rellenar valores NaN con 0 (opcional, dependiendo de tus datos)
    df[['Debit_A', 'Credit_A']] = df[['Debit_A', 'Credit_A']].fillna(0)
        # Calcular la columna Neto_A
    df['Neto_A'] = df.apply(
            lambda row: row['Debit_A'] - row['Credit_A'] ,
            axis=1
        )
    df['Año_A'] = pd.to_datetime(df['Año_A'], errors='coerce')
    df['Año_A'] = df['Año_A'].dt.year

        # Convertir la columna 'Mes_A' al tipo datetime
    df['Mes_A'] = pd.to_datetime(df['Mes_A'], errors='coerce')
    df = df.merge(df_mapeo, on='Cuenta_A', how='left')
        # Crear una nueva columna con el mes (en formato numérico o nombre, según prefieras)
    df['Mes_A'] = df['Mes_A'].dt.month 
    df = df.groupby(['Año_A', 'Mes_A', 'Proyecto_A', 'CeCo_A', 'Empresa_A', 'Cuenta_A'])['Debit_A','Credit_A','Neto_A'].sum().reset_index()
    df = df.merge(df_mapeo, on='Cuenta_A', how='left')

    meses = df['Mes_A'].unique().tolist()
    años = df['Año_A'].unique().tolist()
    empresas = df['Empresa_A'].unique().tolist()
    st.write('')
    @st.cache_data
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")
        return output.getvalue()

    # Botón de descarga
    excel_data = to_excel(df)
    col1, col2 = st.columns(2)
    col1.download_button(
        label="Descargar Movimientos de sistema",
        data=excel_data,
        file_name="datos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    def limpiar_cache():
        st.cache_data.clear()  # Limpia el caché de los datos
        
    if col2.button("Volver a recargar datos del sistema"):
        limpiar_cache()
        st.warning("recargar la pagina")
    col1, col2 = st.columns(2)
    año = col1.selectbox('SELECCIONAR AÑO', años)
    mes = col2.selectbox('SELECCIONAR MES', meses)

    df = df[(df['Año_A'] == año) & (df['Mes_A'] == mes)]
    col1, col2 = st.columns(2)
    ingreso_50 = df[(df['CeCo_A'] == 50) & (df['Cuenta_A'] >399999999) & (df['Cuenta_A'] <500000000)]['Neto_A'].sum()
    egreso_50 = df[(df['CeCo_A'] == 50) & (df['Cuenta_A'] >500000000)]['Neto_A'].sum()
    col1.write(f'INGRESO INTEREMPRESAS: {ingreso_50:,.2f}')
    col2.write(f'EGRESO INTEREMPRESAS: {egreso_50:,.2f}')
    dfsb = df[~(df['CeCo_A'] == 50) & (df['Cuenta_A']>399999999)]
    orden_meses = {
        1: 'ene.', 2: 'feb.', 3: 'mar.', 4: 'abr.',
        5: 'may.', 6: 'jun.', 7: 'jul.', 8: 'ago.',
        9: 'sep.', 10: 'oct.', 11: 'nov.', 12: 'dic.'
    }
    mes_a_numero = {v: k for k, v in orden_meses.items()}

    # Cambiar la columna 'mes' de abreviaturas a números usando map
    df_base['Mes_A'] = df_base['Mes_A'].map(mes_a_numero)

    proyectos = dfsb['Proyecto_A'].unique().tolist()
    historicos = ['CASETAS', 'RENTA', 'SOFTWARE', 'NOMINA ADMINISTRATIVOS','NOMINA OPERADORES']
    def df_cuentas (df, y, cat, col, mes, df_base):
        df_list = []
        for x in proyectos:
            df_pro = df[df['Proyecto_A'] == x]
            df_cat = df_pro[df_pro[y] == cat]['Neto_A'].sum(skipna=True)
            if cat in historicos:
                df_base = df_base[df_base['Mes_A'] == (mes -1)]
                df_pro_provisiones = df_base[df_base['Proyecto_A'] == x]
                df_cat_provisiones = df_pro_provisiones[df_pro_provisiones[y] == cat]['Neto_A'].sum(skipna=True)
            else:
                df_pro_provisiones = df_provisiones[df_provisiones['Proyecto_A'] == x]
                df_cat_provisiones = df_pro_provisiones[df_pro_provisiones[y] == cat]['Neto_A'].sum(skipna=True)
            data = {
                'PROYECTO' : [x],
                f'{cat} SISTEMA' : [df_cat],
                f'{cat} PROVISION' : [df_cat_provisiones] 
            }
            x = pd.DataFrame(data)
            df_list.append(x)

        df_final = pd.concat(df_list, ignore_index=True)
        nueva_fila = {
        df_final.columns[0] : 'ESGARI',
        df_final.columns[1] : df_final[df_final.columns[1]].sum(skipna=True),
        df_final.columns[2] : df_final[df_final.columns[2]].sum(skipna=True)
            }
        nueva_fila = pd.DataFrame([nueva_fila])
        df_final = pd.concat([df_final, nueva_fila], ignore_index=True)
        df_final = df_final.set_index('PROYECTO')
        col.subheader(f'COMPARACIÓN {cat}')
        col.write(df_final)

    categorias = ['INGRESO','NOMINA OPERADORES', 'NOMINA ADMINISTRATIVOS', 'FLETES', 'RENTA DE REMOLQUES', 'COMBUSTIBLE', 'CASETAS', 'RENTA', 'SOFTWARE']
    i = 0
    col1, col2, col3 = st.columns(3)

    # Alternar entre tres columnas
    i = 0
    for x in categorias:
        if i % 3 == 0:
            # Columna 1
            current_col = col1
        elif i % 3 == 1:
            # Columna 2
            current_col = col2
        else:
            # Columna 3
            current_col = col3
        df_cuentas(dfsb, 'Categoria_A', x, current_col, mes, df_base)
        i = i+1

    cuentas = ['DAÑOS', 'DIF DE KILOMETRAJE', 'MANTENIMIENTO EQ TRANSPORTE', 'SEGUROS Y FIANZAS']
    i = 0
    col1, col2, col3 = st.columns(3)

    # Alternar entre tres columnas
    i = 0
    for x in cuentas:
        if i % 3 == 0:
            # Columna 1
            current_col = col1
        elif i % 3 == 1:
            # Columna 2
            current_col = col2
        else:
            # Columna 3
            current_col = col3
        df_cuentas(dfsb, 'Cuenta_Nombre_A', x, current_col, mes, df_base)
        i = i+1
    if st.button("Cerrar sesión"):
        st.session_state.authenticated = False
        st.rerun()

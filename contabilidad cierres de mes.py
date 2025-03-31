import pandas as pd
import streamlit as st
from datetime import datetime
from io import BytesIO, StringIO
import OTMrunReport as rr
import requests
st.set_page_config(layout="wide")
logo_base64 = """
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
"""
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo de la Empresa" width="300">
    </div>
    """,
    unsafe_allow_html=True,
)
# Acceder a los secretos
usernames = st.secrets["credentials"]["usernames"]
passwords = st.secrets["credentials"]["passwords"]

# Lógica de autenticación
def authenticate(username, password):
    if username in usernames:
        index = usernames.index(username)
        if passwords[index] == password:
            return True
    return False

# Interfaz de usuario
username_input = st.text_input("Usuario")
password_input = st.text_input("Contraseña", type="password")

if st.button("Iniciar sesión"):
    if authenticate(username_input, password_input):
        st.success("Bienvenid@!")
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

    else:
        st.error("Usuario o contraseña incorrectos")

import pymysql

def obtener_conexion():
    """
    Establece una conexión con la base de datos MySQL.

    Retorna:
        Una conexión activa a la base de datos.
    """
    try:
        conexion = pymysql.connect(
            host="localhost",          # Cambia esto a la IP de tu servidor si no es local
            user="root",               # Usuario de tu base de datos
            password="curso",          # Contraseña del usuario
            database="encuestas",      # Nombre de la base de datos
            port=3306                  # Puerto de MySQL, generalmente 3306
        )
        print("Conexión a la base de datos establecida correctamente.")
        return conexion
    except pymysql.MySQLError as e:
        print("Error al conectar a la base de datos:", e)
        return None

def listar_registros():
    """
    Obtiene todos los registros de la tabla ENCUESTA.

    Retorna:
        Una lista de tuplas con los registros de la tabla.
    """
    conexion = obtener_conexion()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return []

    try:
        with conexion.cursor() as cursor:
            consulta = """
            SELECT idEncuesta, edad, Sexo, BebidasSemana, CervezasSemana,
                   BebidasFinSemana, BebidasDestiladasSemana, VinosSemana,
                   PerdidasControl, DiversionDependenciaAlcohol,
                   ProblemasDigestivos, TensionAlta, DolorCabeza
            FROM ENCUESTA;
            """
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            return resultados
    except pymysql.MySQLError as e:
        print("Error al listar registros:", e)
        return []
    finally:
        conexion.close()

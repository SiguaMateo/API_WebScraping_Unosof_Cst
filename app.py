try:
    from fastapi import FastAPI
    import uvicorn
    from task import start_scheduler, get_data_task

except Exception as e:
    print(f"Error al importar las librerías en main.py, {e}")

app = FastAPI(
    title="API WebScraping DAE Unosof",
    description="API para la extracción de datos de la página de Unosof",
    version="1.0.0"
)

@app.get("/", description="Endpoint raíz")
def default_endpoint():
    return {"message": "Inicio la API WebScraping DAE Unosof"}

@app.get("/get-data-unosof", description="Endpoint para extraer la data de la página Unosof")
def trigger_get_data():
    """
    Endpoint para ejecutar manualmente la tarea de extracción.
    """
    get_data_task()
    return {"message": "Tarea de extracción ejecutada manualmente"}

if __name__ == "__main__":
    start_scheduler()  # Iniciar el programador al arrancar la API
    uvicorn.run("app:app", host="0.0.0.0", port=9995, reload=True)

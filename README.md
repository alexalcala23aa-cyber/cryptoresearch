
Requiere Python 3.11 o posterior.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Para ejecutar las pruebas:
```bash
python -m unittest discover -s tests -v
```

## Instalar en el repositorio GitHub existente
1. Descarga y descomprime este ZIP.
2. Abre tu repositorio `CryptoResearch-AI`.
3. Sube el contenido de esta carpeta a la raíz del repositorio con **Add file → Upload files**.
4. Acepta la actualización de los archivos existentes y confirma los cambios.
5. Abre **Actions** y comprueba el workflow `CryptoResearch AI - análisis 4h`.
6. Para probarlo, selecciona el workflow y pulsa **Run workflow**.

El workflow necesita permiso para guardar los informes. El archivo YAML ya solicita `contents: write`; si la organización lo bloquea, un administrador deberá permitirlo en los ajustes de Actions.

## Frecuencia y límites
GitHub Actions puede retrasar ejecuciones programadas y no garantiza puntualidad exacta. La API pública puede limitar peticiones o estar temporalmente indisponible. Si un activo falla, el programa lo anota y continúa con los demás. El informe indicará claramente cuándo faltan datos.

## Seguridad y alcance
- No añadas claves, contraseñas ni tokens de exchanges.
- No conectes cuentas ni actives operaciones reales.
- Todo el historial es observacional; no simula fills ni rentabilidad.
- Los umbrales son parámetros experimentales y deben validarse antes de sacar conclusiones.


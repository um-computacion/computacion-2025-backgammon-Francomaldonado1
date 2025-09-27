import os

def read_full_file(filepath):
    """Lee y devuelve todo el contenido de un archivo."""
    if not os.path.exists(filepath):
        return f"Error: Report file not found at {filepath}"
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def extract_pylint_score(filepath):
    """Busca en el reporte de Pylint y extrae solo la línea final de la puntuación."""
    if not os.path.exists(filepath):
        return f"Error: Pylint report file not found at {filepath}"
    
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("Your code has been rated at"):
                return line.strip()
                
    return "Pylint score line not found in the report."

# --- Lógica Principal ---

coverage_report = read_full_file("coverage_report.txt")
pylint_summary = extract_pylint_score("pylint_report.txt")

# --- Construcción del reporte por partes (MÉTODO MÁS SEGURO) ---
# En lugar de un solo f-string, creamos el contenido paso a paso.
# Esto evita que caracteres en los reportes rompan la cadena principal.

reports_content_parts = [
    "# Automated Reports\n",
    "## Coverage Report",
    coverage_report,
    "---",
    "## Pylint Score",
    "------------------------------------------------------------------",
    pylint_summary,
]

# Unimos todas las partes con saltos de línea
reports_content = "\n".join(reports_content_parts)


with open("REPORTS.md", "w", encoding="utf-8") as f:
    f.write(reports_content)

print("REPORTS.md generated successfully!")
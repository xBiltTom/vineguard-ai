"""
Módulo de estadísticas avanzadas para VineGuard AI.
Contiene las funciones de cálculo de MCC, McNemar y validación con múltiples imágenes.
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import matthews_corrcoef, confusion_matrix
import streamlit as st
from PIL import Image

from src.utils.config import DISEASE_CLASSES


def calculate_matthews_coefficient(y_true, y_pred, num_classes):
    """
    Calcula el Coeficiente de Matthews para clasificación multiclase
    """
    try:
        mcc = matthews_corrcoef(y_true, y_pred)
        return mcc
    except:
        # Cálculo manual si hay problemas
        cm = confusion_matrix(y_true, y_pred, labels=range(num_classes))

        # Para multiclase, usamos la fórmula generalizada
        # MCC = (∑c*s - ∑pk*tk) / sqrt((∑s^2 - ∑pk^2)(∑s^2 - ∑tk^2))

        n = cm.sum()
        sum_diag = np.trace(cm)

        sum_pk = np.sum(cm.sum(axis=0) ** 2)
        sum_tk = np.sum(cm.sum(axis=1) ** 2)
        sum_squares = np.sum(cm.sum(axis=0) * cm.sum(axis=1))

        numerator = n * sum_diag - sum_squares
        denominator = np.sqrt((n**2 - sum_pk) * (n**2 - sum_tk))

        if denominator == 0:
            return 0.0

        mcc = numerator / denominator
        return mcc


def mcnemar_test_multiclass(y_true, y_pred1, y_pred2):
    """
    Prueba de McNemar para clasificación multiclase
    Compara si dos modelos difieren significativamente en sus predicciones
    """
    # Crear tabla de contingencia 2x2
    # (correcto_modelo1, incorrecto_modelo1) vs (correcto_modelo2, incorrecto_modelo2)

    correct_1 = (y_true == y_pred1)
    correct_2 = (y_true == y_pred2)

    # Casos donde los modelos difieren
    model1_correct_model2_wrong = np.sum(correct_1 & ~correct_2)  # b
    model1_wrong_model2_correct = np.sum(~correct_1 & correct_2)  # c

    # Tabla de McNemar
    # |  Modelo2  |           |
    # |  C    W   | Modelo1   |
    # |  a    b   | Correcto  |
    # |  c    d   | Incorrecto|

    b = model1_correct_model2_wrong
    c = model1_wrong_model2_correct

    # Si no hay diferencias, no se puede hacer la prueba
    if b + c == 0:
        return {
            'statistic': 0.0,
            'p_value': 1.0,
            'b': b,
            'c': c,
            'interpretation': 'No hay diferencias entre modelos'
        }

    # Aplicar corrección de continuidad de Yates
    if b + c > 25:
        # Para muestras grandes, usar corrección de continuidad
        statistic = (abs(b - c) - 0.5) ** 2 / (b + c)
    else:
        # Para muestras pequeñas, usar prueba exacta
        statistic = (b - c) ** 2 / (b + c)

    # Calcular p-valor usando distribución chi-cuadrado con 1 grado de libertad
    p_value = 1 - stats.chi2.cdf(statistic, df=1)

    # Interpretación
    if p_value < 0.001:
        interpretation = "Diferencia altamente significativa (p < 0.001)"
    elif p_value < 0.01:
        interpretation = "Diferencia muy significativa (p < 0.01)"
    elif p_value < 0.05:
        interpretation = "Diferencia significativa (p < 0.05)"
    elif p_value < 0.1:
        interpretation = "Diferencia marginalmente significativa (p < 0.1)"
    else:
        interpretation = "No hay diferencia significativa (p ≥ 0.1)"

    return {
        'statistic': statistic,
        'p_value': p_value,
        'b': b,
        'c': c,
        'interpretation': interpretation
    }


def interpret_mcc(mcc):
    """Interpreta el valor del Coeficiente de Matthews"""
    if mcc >= 0.9:
        return "Excelente (≥ 0.9)"
    elif mcc >= 0.8:
        return "Muy bueno (0.8-0.89)"
    elif mcc >= 0.6:
        return "Bueno (0.6-0.79)"
    elif mcc >= 0.4:
        return "Moderado (0.4-0.59)"
    elif mcc >= 0.2:
        return "Débil (0.2-0.39)"
    elif mcc > 0:
        return "Muy débil (0-0.19)"
    elif mcc == 0:
        return "Sin correlación (0)"
    else:
        return "Correlación negativa (< 0)"


def process_multiple_images_by_folders(disease_files, models):
    """
    Procesa múltiples imágenes organizadas por carpetas de enfermedades
    """
    from src.core.inference import predict_disease
    from src.ui.tabs.tab_mcnemar import get_disease_folders_dynamic

    all_predictions = {model_name: [] for model_name in models.keys()}
    y_true = []
    total_images = 0

    # Contar total de imágenes
    for disease_name, files in disease_files.items():
        total_images += len(files)

    if total_images == 0:
        return None, "No se cargaron imágenes"

    try:
        progress_bar = st.progress(0)
        processed = 0

        DISEASE_FOLDERS = get_disease_folders_dynamic()

        for disease_name, files in disease_files.items():
            if len(files) > 0:
                # Obtener la clave en inglés de la enfermedad
                disease_key = DISEASE_FOLDERS[disease_name]["key"]
                disease_idx = DISEASE_CLASSES.index(disease_key)

                for uploaded_file in files:
                    # Cargar imagen
                    image = Image.open(uploaded_file).convert('RGB')

                    # Añadir etiqueta verdadera
                    y_true.append(disease_idx)

                    # Obtener predicciones de todos los modelos
                    for model_name, model in models.items():
                        result = predict_disease(image, model, model_name)
                        predicted_idx = result['predicted_class_idx']
                        all_predictions[model_name].append(predicted_idx)

                    processed += 1
                    progress_bar.progress(processed / total_images)

        progress_bar.empty()

        # Convertir a arrays numpy
        model_predictions = [np.array(all_predictions[model_name]) for model_name in models.keys()]
        y_true = np.array(y_true)

        return {
            'y_true': y_true,
            'predictions': model_predictions,
            'model_names': list(models.keys())
        }, None

    except Exception as e:
        return None, f"Error procesando imágenes: {str(e)}"


def create_validation_results_display(validation_data, mcnemar_analysis):
    """
    Crea visualización de resultados de validación
    """
    y_true = validation_data['y_true']
    model_predictions = validation_data['predictions']
    model_names = validation_data['model_names']

    # Calcular métricas por modelo
    results_summary = []
    for i, (model_name, predictions) in enumerate(zip(model_names, model_predictions)):
        accuracy = np.mean(y_true == predictions)
        results_summary.append({
            'Modelo': model_name,
            'Precisión': f"{accuracy:.1%}",
            'Muestras Correctas': f"{np.sum(y_true == predictions)}/{len(y_true)}"
        })

    return pd.DataFrame(results_summary)


def perform_mcnemar_analysis(validation_data):
    """
    Realiza análisis McNemar con datos reales de validación
    MODIFICADO: Solo compara el mejor modelo (según MCC) con los demás
    """
    if validation_data is None:
        return None

    y_true_real = validation_data['y_true']
    model_predictions = validation_data['predictions']
    model_names = validation_data['model_names']

    # Calcular MCC real para cada modelo
    matthews_coefficients = []
    for i, (model_name, predictions) in enumerate(zip(model_names, model_predictions)):
        mcc = calculate_matthews_coefficient(y_true_real, predictions, len(DISEASE_CLASSES))
        matthews_coefficients.append({
            'model': model_name,
            'mcc': mcc,
            'interpretation': interpret_mcc(mcc),
            'index': i  # Añadir índice para referencia
        })

    # MODIFICACIÓN: Encontrar el mejor modelo según MCC
    best_model_info = max(matthews_coefficients, key=lambda x: x['mcc'])
    best_model_idx = best_model_info['index']
    best_model_name = best_model_info['model']

    # MODIFICACIÓN: Realizar pruebas de McNemar solo entre el mejor modelo y los demás
    mcnemar_results = []
    for i in range(len(model_names)):
        if i != best_model_idx:  # No comparar el mejor modelo consigo mismo
            mcnemar_result = mcnemar_test_multiclass(
                y_true_real,
                model_predictions[best_model_idx],
                model_predictions[i]
            )
            mcnemar_result['model1'] = best_model_name
            mcnemar_result['model2'] = model_names[i]
            mcnemar_results.append(mcnemar_result)

    return {
        'matthews_coefficients': matthews_coefficients,
        'mcnemar_results': mcnemar_results,
        'sample_size': len(y_true_real),
        'real_data': True,
        'best_model': best_model_name  # Añadir información del mejor modelo
    }


def generate_interpretation_for_professor(mcnemar_analysis, validation_data):
    """
    Genera interpretación concisa para el profesor
    MODIFICADO: Actualizar texto para reflejar que solo se compara el mejor modelo
    """
    if not mcnemar_analysis:
        return "No hay datos para interpretar."

    # Análisis básico
    sample_size = mcnemar_analysis['sample_size']
    matthews_coefficients = mcnemar_analysis['matthews_coefficients']
    mcnemar_results = mcnemar_analysis['mcnemar_results']
    best_model = mcnemar_analysis.get('best_model', 'N/A')

    # Encontrar mejor modelo por MCC
    best_mcc_model = max(matthews_coefficients, key=lambda x: x['mcc'])

    # Encontrar mejor modelo por precisión
    y_true = validation_data['y_true']
    model_predictions = validation_data['predictions']
    model_names = validation_data['model_names']

    accuracies = []
    for i, (model_name, predictions) in enumerate(zip(model_names, model_predictions)):
        accuracy = np.mean(y_true == predictions)
        accuracies.append({'model': model_name, 'accuracy': accuracy})

    best_accuracy_model = max(accuracies, key=lambda x: x['accuracy'])

    # Contar diferencias significativas
    significant_differences = len([r for r in mcnemar_results if r['p_value'] < 0.05])

    # Generar interpretación
    interpretation = f"""
**INTERPRETACIÓN PARA PRESENTACIÓN ACADÉMICA**

**Dataset de Validación:** {sample_size} imágenes reales de hojas de vid

**Modelo Recomendado:** {best_accuracy_model['model']} (Precisión: {best_accuracy_model['accuracy']:.1%})

**Análisis Estadístico:**
• **Coeficiente de Matthews (MCC):** {best_mcc_model['mcc']:.3f} - {best_mcc_model['interpretation']}
• **Pruebas de McNemar:** {best_model} (mejor modelo) vs otros 3 modelos: {significant_differences} de {len(mcnemar_results)} comparaciones muestran diferencias significativas (p < 0.05)

**Conclusión Científica:**
"""

    if significant_differences > 0:
        interpretation += f"El modelo {best_model} muestra diferencias estadísticamente significativas respecto a {significant_differences} de los otros modelos, validando su superioridad técnica. Recomendación: implementar {best_accuracy_model['model']} para uso clínico."
    else:
        interpretation += f"El modelo {best_model} no muestra diferencias estadísticamente significativas respecto a los otros modelos (p ≥ 0.05), indicando rendimiento equivalente. Criterios adicionales (velocidad, recursos) pueden guiar la selección final."

    if best_mcc_model['mcc'] == 0:
        interpretation += f"\n\n**Nota Metodológica:** MCC = 0 indica dataset homogéneo (una clase predominante), típico en validaciones clínicas enfocadas."

    return interpretation


def create_beautiful_validation_charts(validation_data, mcnemar_analysis):
    """
    Crea gráficos bonitos y elegantes para la validación.
    Esta función se mantiene aquí (en statistics_core) para evitar
    importaciones circulares entre pdf_generator y tab_mcnemar.
    """
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Configurar estilo de matplotlib
    plt.style.use('default')
    sns.set_palette("husl")

    # Crear figura con múltiples subplots
    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor('white')

    # Datos básicos
    y_true = validation_data['y_true']
    model_predictions = validation_data['predictions']
    model_names = validation_data['model_names']
    matthews_coefficients = mcnemar_analysis['matthews_coefficients']
    mcnemar_results = mcnemar_analysis['mcnemar_results']

    # Colores elegantes
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3']

    # ===== GRÁFICO 1: MCC por modelo (arriba izquierda) =====
    ax1 = plt.subplot(2, 3, 1)
    models = [m['model'] for m in matthews_coefficients]
    mccs = [m['mcc'] for m in matthews_coefficients]

    bars = ax1.bar(models, mccs, color=colors[:len(models)], alpha=0.8, edgecolor='white', linewidth=2)
    ax1.set_title('📈 Coeficiente de Matthews (MCC)', fontsize=14, fontweight='bold', pad=20)
    ax1.set_ylabel('MCC', fontweight='bold')
    ax1.set_ylim(-1, 1)
    ax1.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    ax1.grid(True, alpha=0.3)

    for bar, mcc in zip(bars, mccs):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                 f'{mcc:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

    plt.xticks(rotation=45)

    # ===== GRÁFICO 2: Precisión por modelo (arriba centro) =====
    ax2 = plt.subplot(2, 3, 2)
    accuracies = []
    for i, (model_name, predictions) in enumerate(zip(model_names, model_predictions)):
        accuracy = np.mean(y_true == predictions)
        accuracies.append(accuracy)

    bars2 = ax2.bar(model_names, accuracies, color=colors[:len(model_names)], alpha=0.8, edgecolor='white', linewidth=2)
    ax2.set_title('🎯 Precisión por Modelo', fontsize=14, fontweight='bold', pad=20)
    ax2.set_ylabel('Precisión', fontweight='bold')
    ax2.set_ylim(0, 1)
    ax2.grid(True, alpha=0.3)

    for bar, acc in zip(bars2, accuracies):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                 f'{acc:.1%}', ha='center', va='bottom', fontweight='bold', fontsize=10)

    plt.xticks(rotation=45)

    # ===== GRÁFICO 3: McNemar p-valores (arriba derecha) =====
    ax3 = plt.subplot(2, 3, 3)
    comparisons = [f"{r['model1']} vs {r['model2']}" for r in mcnemar_results]
    p_values = [r['p_value'] for r in mcnemar_results]

    bar_colors = ['#FF6B6B' if p < 0.05 else '#4ECDC4' for p in p_values]

    bars3 = ax3.bar(range(len(comparisons)), p_values, color=bar_colors, alpha=0.8, edgecolor='white', linewidth=2)
    ax3.set_title('🔬 Prueba de McNemar (p-valores)', fontsize=14, fontweight='bold', pad=20)
    ax3.set_ylabel('p-valor', fontweight='bold')
    ax3.set_xticks(range(len(comparisons)))
    ax3.set_xticklabels([comp.replace(' vs ', '\nvs\n') for comp in comparisons], fontsize=8)
    ax3.axhline(y=0.05, color='red', linestyle='--', alpha=0.7, label='α = 0.05')
    ax3.grid(True, alpha=0.3)
    ax3.legend()

    for bar, p in zip(bars3, p_values):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                 f'{p:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=8)

    # ===== GRÁFICO 4: Distribución del dataset (abajo izquierda) =====
    ax4 = plt.subplot(2, 3, 4)
    unique, counts = np.unique(y_true, return_counts=True)
    disease_names_chart = [DISEASE_CLASSES[i] for i in unique]

    wedges, texts, autotexts = ax4.pie(counts, labels=disease_names_chart, autopct='%1.1f%%',
                                       colors=colors[:len(unique)], startangle=90,
                                       textprops={'fontsize': 10, 'fontweight': 'bold'})
    ax4.set_title('📊 Distribución del Dataset', fontsize=14, fontweight='bold', pad=20)

    # ===== GRÁFICO 5: Matriz de confusión del mejor modelo (abajo centro) =====
    ax5 = plt.subplot(2, 3, 5)
    best_model_info = max(matthews_coefficients, key=lambda x: x['mcc'])
    best_model_idx = best_model_info['index']
    best_predictions = model_predictions[best_model_idx]

    # Asegurar que la matriz siempre sea de tamaño num_classes x num_classes
    cm = confusion_matrix(y_true, best_predictions, labels=range(len(DISEASE_CLASSES)))
    im = ax5.imshow(cm, interpolation='nearest', cmap='Blues', alpha=0.8)
    ax5.set_title(f'🎯 Matriz de Confusión\n{best_model_info["model"]}', fontsize=12, fontweight='bold', pad=20)

    ax5.set_xticks(range(len(DISEASE_CLASSES)))
    ax5.set_yticks(range(len(DISEASE_CLASSES)))
    ax5.set_xticklabels([name.replace('_', ' ') for name in DISEASE_CLASSES], rotation=45)
    ax5.set_yticklabels([name.replace('_', ' ') for name in DISEASE_CLASSES])
    ax5.set_xlabel('Predicción', fontweight='bold')
    ax5.set_ylabel('Real', fontweight='bold')

    for i in range(len(DISEASE_CLASSES)):
        for j in range(len(DISEASE_CLASSES)):
            text = ax5.text(j, i, cm[i, j], ha="center", va="center",
                            color="white" if cm[i, j] > cm.max()/2 else "black",
                            fontweight='bold', fontsize=12)

    # ===== GRÁFICO 6: Ranking de modelos (abajo derecha) =====
    ax6 = plt.subplot(2, 3, 6)

    combined_scores = []
    for i, model_name in enumerate(model_names):
        mcc = matthews_coefficients[i]['mcc']
        acc = accuracies[i]
        combined_score = (mcc + acc) / 2
        combined_scores.append(combined_score)

    sorted_indices = np.argsort(combined_scores)[::-1]
    sorted_models = [model_names[i] for i in sorted_indices]
    sorted_scores = [combined_scores[i] for i in sorted_indices]

    bars6 = ax6.barh(sorted_models, sorted_scores, color=colors[:len(sorted_models)], alpha=0.8, edgecolor='white', linewidth=2)
    ax6.set_title('🏆 Ranking de Modelos\n(MCC + Precisión)', fontsize=12, fontweight='bold', pad=20)
    ax6.set_xlabel('Score Combinado', fontweight='bold')
    ax6.grid(True, alpha=0.3)

    for bar, score in zip(bars6, sorted_scores):
        width = bar.get_width()
        ax6.text(width + 0.01, bar.get_y() + bar.get_height()/2.,
                 f'{score:.3f}', ha='left', va='center', fontweight='bold', fontsize=10)

    plt.tight_layout()
    return fig

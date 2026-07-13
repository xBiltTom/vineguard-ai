"""
Módulo de internacionalización (i18n)
Contiene todas las traducciones del sistema VineGuard AI
"""

import streamlit as st

# ======= SISTEMA DE INTERNACIONALIZACIÓN =======
TRANSLATIONS = {
    'es': {
        'app_title': 'VineGuard AI',
        'app_subtitle': 'Sistema Inteligente de Diagnóstico de Enfermedades en Viñedos',
        'app_description': 'Con Análisis Estadístico Avanzado (Matthews & McNemar)',
        'language_selector': 'Idioma / Language',
        'sidebar': {
            'config': 'Configuración',
            'load_models': 'Cargar Modelos',
            'models_loaded': 'Modelos listos',
            'available_models': 'Modelos Disponibles',
            'info_title': 'Información',
            'info_text': '''Esta aplicación utiliza modelos de deep learning para detectar enfermedades en hojas de vid:
            
- **Podredumbre Negra**
- **Esca** 
- **Tizón de la Hoja**
- **Hojas Sanas**

**Modelos Disponibles:**
- CNN Simple, MobileNetV2, EfficientNet, DenseNet
- **NUEVOS: Modelos Híbridos con CLAHE y Atención**

**Análisis Estadístico:**
- Coeficiente de Matthews (con múltiples imágenes)
- Prueba de McNemar (con múltiples imágenes)

**💡 Tip:** Use la pestaña 'Validación McNemar' para análisis estadístico completo con su propio dataset.''',
            'load_models_warning': 'Por favor, carga los modelos desde la barra lateral'
        },
        'tabs': {
            'diagnosis': 'Diagnóstico',
            'statistical': 'Análisis Estadístico',
            'mcnemar': 'Validación McNemar',
            'info': 'Información'
        },
        'diagnosis': {
            'title': 'Diagnóstico de Enfermedades',
            'input_method': 'Selecciona método de entrada:',
            'upload_image': 'Subir imagen',
            'use_camera': 'Usar cámara',
            'file_uploader': 'Selecciona una imagen de hoja de vid',
            'formats_help': 'Formatos soportados: JPG, JPEG, PNG',
            'image_loaded': 'Imagen cargada',
            'analyze_button': 'Analizar Imagen',
            'analyzing': 'Analizando imagen...',
            'analysis_complete': 'Análisis completado!',
            'results_title': 'Resultados del Diagnóstico',
            'consensus_title': 'Diagnóstico Consensuado',
            'final_diagnosis': 'Diagnóstico Final:',
            'agreement': 'Coincidencia',
            'confidence': 'Confianza',
            'probability_distribution': 'Distribución de Probabilidades',
            'treatment_recommendations': 'Recomendaciones de Tratamiento',
            'severity': 'Gravedad:',
            'recommended_treatment': 'Tratamiento Recomendado',
            'preventive_measures': 'Medidas Preventivas',
            'generate_report': 'Generar Reporte',
            'download_pdf': 'Descargar Reporte PDF',
            'generating_report': 'Generando reporte...',
            'download_pdf_button': 'Descargar PDF',
            'camera_info': 'La función de cámara requiere acceso al hardware del dispositivo',
            'camera_warning': 'Por favor, usa la opción de subir imagen por ahora'
        },
        'diseases': {
            'Black_rot': 'Podredumbre Negra',
            'Esca': 'Esca (Sarampión Negro)',
            'Healthy': 'Sana',
            'Leaf_blight': 'Tizón de la Hoja'
        },
        'disease_folders': {
            'Black_rot': {
                'name': 'Podredumbre Negra',
                'description': 'Hongos Guignardia bidwellii'
            },
            'Esca': {
                'name': 'Esca (Sarampión Negro)',
                'description': 'Complejo de hongos vasculares'
            },
            'Healthy': {
                'name': 'Hojas Sanas',
                'description': 'Sin enfermedades detectables'
            },
            'Leaf_blight': {
                'name': 'Tizón de la Hoja',
                'description': 'Hongo Isariopsis'
            }
        },
        'statistical': {
            'title': 'Análisis Estadístico de Modelos',
            'real_data_available': 'Análisis con datos reales disponible',
            'mcc_title': 'Coeficiente de Matthews (MCC) - Datos Reales',
            'mcc_description': '''El MCC es una métrica balanceada que considera todos los tipos de predicciones (verdaderos/falsos positivos/negativos). 
Valores cercanos a +1 indican predicción perfecta, 0 indica predicción aleatoria, y -1 indica predicción completamente incorrecta.''',
            'model_ranking': 'Ranking de Modelos',
            'speed_analysis': 'Análisis de Velocidad de Modelos',
            'inference_time_distribution': 'Distribución de Tiempos de Inferencia',
            'speed_comparison': 'Comparación de Velocidad',
            'fastest': 'Más Rápido',
            'slowest': 'Más Lento',
            'average': 'Promedio',
            'speed_stats': 'Estadísticas de Velocidad',
            'no_statistical_analysis': 'Análisis Estadístico No Disponible',
            'statistical_info': '''Para obtener análisis estadístico real (MCC y McNemar):
1. Ve a la pestaña 'Validación McNemar'
2. Carga al menos 30 imágenes con sus etiquetas verdaderas
3. El análisis estadístico aparecerá automáticamente aquí''',
            'why_multiple_images': '''**¿Por qué necesitas múltiples imágenes?**
- Con una sola imagen no se pueden calcular métricas estadísticas reales
- Se requieren al menos 30 muestras para resultados confiables
- MCC y McNemar comparan el rendimiento general de los modelos''',
            'perform_analysis': 'Realiza un diagnóstico o validación para generar el análisis estadístico',
            'technical_info': {
                'mcc_description': '''- Métrica balanceada para clasificación
- Rango: -1 (peor) a +1 (mejor)
- Considera todos los tipos de predicción
- Útil para datasets desbalanceados
- Interpretación:
  - MCC ≥ 0.8: Muy bueno
  - MCC ≥ 0.6: Bueno  
  - MCC ≥ 0.4: Moderado
  - MCC < 0.4: Necesita mejora''',
                'mcnemar_description': '''- Compara dos modelos estadísticamente
- Basada en distribución χ² (chi-cuadrado)
- H₀: No hay diferencia entre modelos
- H₁: Hay diferencia significativa
- Interpretación del p-valor:
  - p < 0.001: Muy significativo
  - p < 0.01: Significativo
  - p < 0.05: Marginalmente significativo
  - p ≥ 0.05: No significativo'''
            }
        },
        'treatments': {
            'Black_rot': {
                'title': '🔴 Podredumbre Negra Detectada',
                'severity': 'Alta',
                'treatment': [
                    'Aplicar fungicidas sistémicos específicos (como Miclobutanil o Tebuconazol) de inmediato.',
                    'Realizar el retiro manual y quema de "bayas momificadas" ya que son la principal fuente de inóculo.',
                    'Aplicar fungicidas de contacto (Mancozeb o Captan) en las áreas no afectadas.',
                    'Reducir la cobertura vegetal alrededor de los racimos para bajar la humedad relativa.',
                    'Detener cualquier sistema de riego por aspersión temporalmente.'
                ],
                'prevention': [
                    'Implementar deshoje temprano (Canopy Management) para maximizar la circulación del aire y penetración de luz.',
                    'Aplicar fungicidas preventivos desde la etapa de brotación hasta 4 semanas después de la floración.',
                    'Realizar control estricto de malezas debajo de las vides para reducir la humedad estancada.',
                    'Retirar y destruir todos los restos de poda y zarcillos infectados durante el invierno.'
                ]
            },
            'Esca': {
                'title': '🟤 Esca (Sarampión Negro) Detectada',
                'severity': 'Muy Alta',
                'treatment': [
                    'No existe cura química erradicante aprobada (el Arsenito de Sodio está prohibido).',
                    'Realizar "Cirugía del Tronco" (Curetaggio) para raspar y remover la madera esponjosa infectada hasta llegar a madera sana.',
                    'Si la planta está muy comprometida, cortarla por debajo de la zona necrosada y volver a formarla desde un chupón.',
                    'Marcar las cepas enfermas en verano para tratarlas por separado durante la poda de invierno.',
                    'Arrancar e incinerar cepas muertas o irrecuperables.'
                ],
                'prevention': [
                    'Retrasar la poda lo máximo posible (poda tardía) cuando las esporas de los hongos son menos activas.',
                    'Aplicar selladores biológicos (como Trichoderma spp. o Bacillus subtilis) o pastas cicatrizantes químicas en cortes de poda grandes.',
                    'Desinfectar tijeras y serruchos con alcohol al 70% entre planta y planta.',
                    'Evitar podar durante o inmediatamente después de días lluviosos.'
                ]
            },
            'Healthy': {
                'title': '✅ Planta Sana',
                'severity': 'Ninguna',
                'treatment': [
                    'El tejido foliar no presenta patrones detectables de patógenos.',
                    'No se requiere ninguna intervención correctiva en este momento.',
                    'Continuar con el esquema de fertilización planificado.'
                ],
                'prevention': [
                    'Mantener el monitoreo visual quincenal del viñedo, especialmente tras lluvias.',
                    'Continuar con el programa base de fungicidas preventivos (azufre o cobre) según el calendario fenológico.',
                    'Mantener el control de estrés hídrico y asegurar un drenaje óptimo.',
                    'Garantizar niveles adecuados de potasio y magnesio para fortalecer las paredes celulares.'
                ]
            },
            'Leaf_blight': {
                'title': '🟡 Tizón de la Hoja Detectado',
                'severity': 'Moderada',
                'treatment': [
                    'Aplicar fungicidas a base de cobre (Caldo Bordelés) o sistémicos (Difenoconazol, Azoxistrobina).',
                    'Retirar manualmente las hojas severamente manchadas para detener la esporulación.',
                    'Detener la fertilización rica en nitrógeno, ya que el crecimiento foliar excesivo favorece al hongo.',
                    'Mejorar el drenaje del suelo de inmediato si hay encharcamiento.'
                ],
                'prevention': [
                    'Evitar la sobre-fertilización nitrogenada a principios de temporada.',
                    'Realizar poda en verde para evitar un microclima excesivamente húmedo en el interior de la planta.',
                    'Destruir la hojarasca caída en otoño, ya que el hongo Isariopsis sobrevive el invierno en los restos.',
                    'Utilizar mallas antihierba para evitar salpicaduras del suelo a las hojas basales durante lluvias.'
                ]
            }
        },
        'mcnemar': {
            'title': 'Validación Estadística con Dataset Real',
            'theoretical_foundations': 'Fundamentos Teóricos',
            'mcc_theory_title': '🧮 Coeficiente de Matthews (MCC)',
            'mcc_theory_formula': 'Fórmula: MCC = (TP×TN - FP×FN) / √[(TP+FP)(TP+FN)(TN+FP)(TN+FN)]',
            'mcc_theory_purpose': 'Propósito: Métrica balanceada que evalúa la calidad general de clasificación considerando todas las categorías de predicción.',
            'mcc_theory_advantages': 'Ventajas: Robusto ante clases desbalanceadas, interpretación intuitiva (-1 a +1), y considera todos los aspectos de la matriz de confusión.',
            'mcnemar_theory_title': '🔬 Prueba de McNemar',
            'mcnemar_theory_formula': 'Fórmula: χ² = (|b - c| - 0.5)² / (b + c)',
            'mcnemar_theory_purpose': 'Propósito: Test estadístico que compara el rendimiento de dos clasificadores para determinar si sus diferencias son significativas.',
            'mcnemar_theory_application': 'Aplicación: Validación científica de que un modelo es estadísticamente superior a otro (p < 0.05 = diferencia significativa).',
            'smart_folder_system': 'Sistema de Validación por Carpetas Inteligentes',
            'instructions_title': 'Instrucciones:',
            'instructions': [
                'Organiza tus imágenes por enfermedad en cada "carpeta" digital',
                'Mínimo recomendado: 30+ imágenes totales (10+ por categoría)',
                'El sistema automáticamente etiquetará las imágenes según la carpeta elegida'
            ],
            'disease_folders': 'Carpetas de Enfermedades',
            'upload_images': 'Subir imágenes de',
            'images_loaded': 'imágenes cargadas',
            'load_images_message': 'Carga imágenes en las carpetas de enfermedades para comenzar el análisis estadístico',
            'dataset_summary': 'Resumen del Dataset',
            'distribution_by_disease': 'Distribución por enfermedad:',
            'total': 'Total:',
            'images': 'imágenes',
            'minimum_recommendation': 'Se recomienda al menos 30 imágenes para resultados estadísticamente válidos',
            'sufficient_dataset': 'Dataset suficiente para análisis estadístico robusto',
            'process_button': 'PROCESAR DATASET Y CALCULAR ESTADÍSTICAS',
            'processing': 'Procesando imágenes y realizando análisis estadístico...',
            'analysis_completed': '¡ANÁLISIS ESTADÍSTICO COMPLETADO!',
            'analysis_success': 'Datos procesados con éxito. Resultados científicamente válidos generados.',
            'complete_visualization': 'Visualización Completa de Resultados',
            'precision_summary': 'Resumen de Precisión por Modelo',
            'mcc_analysis': 'Análisis de Coeficiente de Matthews (MCC)',
            'best_model_identified': 'MEJOR MODELO IDENTIFICADO',
            'based_on_mcc': 'Basado en Coeficiente de Matthews',
            'mcc_ranking': 'Ranking por MCC:',
            'mcnemar_comparisons': 'Pruebas de McNemar - Comparaciones Estadísticas',
            'reference_model': 'Modelo de referencia:',
            'best_according_mcc': '(mejor según MCC)',
            'comparing_models': 'Comparando {model} vs los otros 3 modelos:',
            'total_comparisons': 'Total Comparaciones',
            'significant_differences': 'Diferencias Significativas',
            'confidence_level': 'Nivel de Confianza',
            'comparison': 'Comparación',
            'chi_square_statistic': 'Estadístico χ²',
            'p_value': 'p-valor',
            'significant_question': '¿Significativo?',
            'significant_difference': 'Diferencia Significativa',
            'no_difference': 'Sin Diferencia',
            'interpretation': 'Interpretación:',
            'academic_interpretation': 'INTERPRETACIÓN ACADÉMICA',
            'generate_statistical_report': 'Generar Reporte Estadístico',
            'preparing_report': 'Preparando reporte estadístico...',
            'download_statistical_pdf': 'Descargar Reporte Estadístico PDF',
            'report_ready': 'Reporte listo para descargar',
            'complete_results_available': 'Los resultados completos están disponibles en la pestaña \'Análisis Estadístico\'',
            'explore_detailed_visualizations': 'Ve a la pestaña anterior para explorar visualizaciones detalladas y métricas adicionales.'
        },
        'info': {
            'title': 'Información sobre Enfermedades',
            'diseases_info': {
                'black_rot': {
                    'name': 'Podredumbre Negra (Black Rot)',
                    'description': 'Causada por el hongo Guignardia bidwellii. Una de las enfermedades más destructivas de la vid.',
                    'symptoms': [
                        'Manchas circulares marrones en las hojas',
                        'Lesiones negras en los frutos',
                        'Momificación de las bayas',
                        'Picnidios negros en tejidos infectados'
                    ],
                    'conditions': 'Se desarrolla en condiciones de alta humedad y temperaturas de 20-27°C'
                },
                'esca': {
                    'name': 'Esca (Sarampión Negro)',
                    'description': 'Enfermedad compleja causada por varios hongos. Afecta el sistema vascular de la planta.',
                    'symptoms': [
                        'Decoloración intervenal en las hojas',
                        'Necrosis marginal',
                        'Muerte regresiva de brotes',
                        'Pudrición interna del tronco'
                    ],
                    'conditions': 'Se agrava con estrés hídrico y heridas de poda mal protegidas'
                },
                'leaf_blight': {
                    'name': 'Tizón de la Hoja (Leaf Blight)',
                    'description': 'Causada por el hongo Isariopsis. Afecta principalmente las hojas maduras.',
                    'symptoms': [
                        'Manchas angulares amarillentas',
                        'Necrosis foliar progresiva',
                        'Defoliación prematura',
                        'Reducción del vigor de la planta'
                    ],
                    'conditions': 'Favorecida por alta humedad relativa y temperaturas moderadas'
                }
            },
            'best_practices': 'Buenas Prácticas de Manejo',
            'prevention': 'Prevención:',
            'prevention_items': [
                'Monitoreo regular del viñedo',
                'Poda sanitaria adecuada',
                'Manejo del dosel vegetal',
                'Drenaje apropiado del suelo',
                'Selección de variedades resistentes'
            ],
            'integrated_management': 'Manejo Integrado:',
            'integrated_items': [
                'Uso racional de fungicidas',
                'Rotación de ingredientes activos',
                'Aplicaciones en momentos críticos',
                'Registro de aplicaciones',
                'Evaluación de eficacia'
            ],
            'statistical_tests': 'Sobre las Pruebas Estadísticas',
            'mcc_technical': 'Coeficiente de Matthews - Información Técnica',
            'mcc_formula_title': 'Fórmula del MCC:',
            'mcc_formula': 'MCC = (TP×TN - FP×FN) / √[(TP+FP)(TP+FN)(TN+FP)(TN+FN)]',
            'mcc_variables': [
                'TP = Verdaderos Positivos',
                'TN = Verdaderos Negativos',
                'FP = Falsos Positivos',
                'FN = Falsos Negativos'
            ],
            'mcc_advantages_title': 'Ventajas:',
            'mcc_advantages': [
                'Balanceado para todas las clases',
                'Robusto ante datasets desbalanceados',
                'Fácil interpretación (-1 a +1)',
                'Considera todos los aspectos de la matriz de confusión'
            ],
            'mcnemar_technical': 'Prueba de McNemar - Información Técnica',
            'mcnemar_procedure': 'Procedimiento:',
            'mcnemar_hypothesis': 'Hipótesis:',
            'mcnemar_h0': 'H₀: No hay diferencia entre modelos',
            'mcnemar_h1': 'H₁: Hay diferencia significativa',
            'mcnemar_statistic': 'Estadístico de prueba:',
            'mcnemar_statistic_formula': 'χ² = (|b - c| - 0.5)² / (b + c)',
            'mcnemar_variables': 'Donde b y c son las frecuencias de desacuerdo entre modelos',
            'mcnemar_decision': 'Decisión:',
            'mcnemar_reject': 'Si p < 0.05: Rechazar H₀ (hay diferencia)',
            'mcnemar_not_reject': 'Si p ≥ 0.05: No rechazar H₀ (sin diferencia)',
            'mcnemar_application': 'Aplicación:',
            'mcnemar_applications': [
                'Comparación objetiva de modelos',
                'Base estadística para selección de modelos',
                'Validación de mejoras en algoritmos'
            ],
            'protection_calendar': 'Calendario de Protección Fitosanitaria',
            'phenological_stage': 'Etapa Fenológica',
            'main_risk': 'Riesgo Principal',
            'recommended_action': 'Acción Recomendada',
            'calendar_data': {
                'stages': ['Brotación', 'Floración', 'Cuajado', 'Envero', 'Maduración'],
                'risks': ['Oídio', 'Black rot', 'Oídio/Black rot', 'Esca', 'Botrytis'],
                'actions': [
                    'Fungicida preventivo',
                    'Fungicida sistémico',
                    'Evaluación y aplicación según presión',
                    'Monitoreo intensivo',
                    'Aplicación pre-cosecha si es necesario'
                ]
            },
            'description': 'Descripción:',
            'symptoms': 'Síntomas:',
            'favorable_conditions': 'Condiciones favorables:'
        }
    },
    'en': {
        'app_title': 'VineGuard AI',
        'app_subtitle': 'Intelligent Disease Diagnosis System for Vineyards',
        'app_description': 'With Advanced Statistical Analysis (Matthews & McNemar)',
        'language_selector': 'Language / Idioma',
        'sidebar': {
            'config': 'Configuration',
            'load_models': 'Load Models',
            'models_loaded': 'Models ready',
            'available_models': 'Available Models',
            'info_title': 'Information',
            'info_text': '''This application uses deep learning models to detect diseases in vine leaves:
            
• **Black Rot**
• **Esca** 
• **Leaf Blight**
• **Healthy Leaves**

**Statistical Analysis:**
• Matthews Coefficient (with multiple images)
• McNemar Test (with multiple images)

**💡 Tip:** Use the 'McNemar Validation' tab for complete statistical analysis with your own dataset.''',
            'load_models_warning': 'Please load the models from the sidebar'
        },
        'tabs': {
            'diagnosis': 'Diagnosis',
            'statistical': 'Statistical Analysis',
            'mcnemar': 'McNemar Validation',
            'info': 'Information'
        },
        'diagnosis': {
            'title': 'Disease Diagnosis',
            'input_method': 'Select input method:',
            'upload_image': 'Upload image',
            'use_camera': 'Use camera',
            'file_uploader': 'Select a vine leaf image',
            'formats_help': 'Supported formats: JPG, JPEG, PNG',
            'image_loaded': 'Image loaded',
            'analyze_button': 'Analyze Image',
            'analyzing': 'Analyzing image...',
            'analysis_complete': 'Analysis completed!',
            'results_title': 'Diagnosis Results',
            'consensus_title': 'Consensus Diagnosis',
            'final_diagnosis': 'Final Diagnosis:',
            'agreement': 'Agreement',
            'confidence': 'Confidence',
            'probability_distribution': 'Probability Distribution',
            'treatment_recommendations': 'Treatment Recommendations',
            'severity': 'Severity:',
            'recommended_treatment': 'Recommended Treatment',
            'preventive_measures': 'Preventive Measures',
            'generate_report': 'Generate Report',
            'download_pdf': 'Download PDF Report',
            'generating_report': 'Generating report...',
            'download_pdf_button': 'Download PDF',
            'camera_info': 'Camera function requires device hardware access',
            'camera_warning': 'Please use the upload image option for now'
        },
        'diseases': {
            'Black_rot': 'Black Rot',
            'Esca': 'Esca (Black Measles)',
            'Healthy': 'Healthy',
            'Leaf_blight': 'Leaf Blight'
        },
        'disease_folders': {
            'Black_rot': {
                'name': 'Black Rot',
                'description': 'Guignardia bidwellii fungi'
            },
            'Esca': {
                'name': 'Esca (Black Measles)',
                'description': 'Complex of vascular fungi'
            },
            'Healthy': {
                'name': 'Healthy Leaves',
                'description': 'No detectable diseases'
            },
            'Leaf_blight': {
                'name': 'Leaf Blight',
                'description': 'Isariopsis fungus'
            }
        },
        'statistical': {
            'title': 'Statistical Analysis of Models',
            'real_data_available': 'Real data analysis available',
            'mcc_title': 'Matthews Correlation Coefficient (MCC) - Real Data',
            'mcc_description': '''MCC is a balanced metric that considers all types of predictions (true/false positives/negatives). 
Values close to +1 indicate perfect prediction, 0 indicates random prediction, and -1 indicates completely incorrect prediction.''',
            'model_ranking': 'Model Ranking',
            'speed_analysis': 'Model Speed Analysis',
            'inference_time_distribution': 'Inference Time Distribution',
            'speed_comparison': 'Speed Comparison',
            'fastest': 'Fastest',
            'slowest': 'Slowest',
            'average': 'Average',
            'speed_stats': 'Speed Statistics',
            'no_statistical_analysis': 'Statistical Analysis Not Available',
            'statistical_info': '''To get real statistical analysis (MCC and McNemar):
1. Go to the 'McNemar Validation' tab
2. Load at least 30 images with their true labels
3. The statistical analysis will appear automatically here''',
            'why_multiple_images': '''**Why do you need multiple images?**
- With a single image, real statistical metrics cannot be calculated
- At least 30 samples are required for reliable results
- MCC and McNemar compare the general performance of models''',
            'perform_analysis': 'Perform a diagnosis or validation to generate statistical analysis',
            'technical_info': {
                'mcc_description': '''- Balanced metric for classification
- Range: -1 (worst) to +1 (best)
- Considers all types of predictions
- Useful for unbalanced datasets
- Interpretation:
  - MCC ≥ 0.8: Very good
  - MCC ≥ 0.6: Good  
  - MCC ≥ 0.4: Moderate
  - MCC < 0.4: Needs improvement''',
                'mcnemar_description': '''- Compares two models statistically
- Based on χ² (chi-square) distribution
- H₀: No difference between models
- H₁: Significant difference exists
- p-value interpretation:
  - p < 0.001: Very significant
  - p < 0.01: Significant
  - p < 0.05: Marginally significant
  - p ≥ 0.05: Not significant'''
            }
        },
        'treatments': {
            'Black_rot': {
                'title': '🔴 Black Rot Detected',
                'severity': 'High',
                'treatment': [
                    'Apply protective fungicides (Mancozeb, Captan)',
                    'Remove and destroy all infected parts',
                    'Improve air circulation in the vineyard',
                    'Avoid sprinkler irrigation'
                ],
                'prevention': [
                    'Prune properly to improve ventilation',
                    'Apply preventive fungicides before flowering',
                    'Remove pruning debris and fallen leaves'
                ]
            },
            'Esca': {
                'title': '🟤 Esca (Black Measles) Detected',
                'severity': 'Very High',
                'treatment': [
                    'No direct cure - focus on prevention',
                    'Prune affected parts with disinfected tools',
                    'Apply healing paste to pruning cuts',
                    'Consider replacing severely affected plants'
                ],
                'prevention': [
                    'Avoid late pruning and on humid days',
                    'Disinfect tools between plants',
                    'Protect pruning wounds immediately'
                ]
            },
            'Healthy': {
                'title': '✅ Healthy Plant',
                'severity': 'None',
                'treatment': [
                    'No treatment required',
                    'Maintain current management practices'
                ],
                'prevention': [
                    'Continue regular monitoring',
                    'Maintain preventive fungicide program',
                    'Ensure balanced nutrition',
                    'Maintain good soil drainage'
                ]
            },
            'Leaf_blight': {
                'title': '🟡 Leaf Blight Detected',
                'severity': 'Moderate',
                'treatment': [
                    'Apply systemic fungicides (Azoxystrobin, Tebuconazole)',
                    'Remove infected leaves',
                    'Improve soil drainage',
                    'Reduce foliage density'
                ],
                'prevention': [
                    'Avoid excess nitrogen',
                    'Keep foliage dry',
                    'Apply preventive fungicides in humid seasons'
                ]
            }
        },
        'mcnemar': {
            'title': 'Statistical Validation with Real Dataset',
            'theoretical_foundations': 'Theoretical Foundations',
            'mcc_theory_title': '🧮 Matthews Correlation Coefficient (MCC)',
            'mcc_theory_formula': 'Formula: MCC = (TP×TN - FP×FN) / √[(TP+FP)(TP+FN)(TN+FP)(TN+FN)]',
            'mcc_theory_purpose': 'Purpose: Balanced metric that evaluates the overall quality of classification considering all prediction categories.',
            'mcc_theory_advantages': 'Advantages: Robust against unbalanced classes, intuitive interpretation (-1 to +1), and considers all aspects of the confusion matrix.',
            'mcnemar_theory_title': '🔬 McNemar Test',
            'mcnemar_theory_formula': 'Formula: χ² = (|b - c| - 0.5)² / (b + c)',
            'mcnemar_theory_purpose': 'Purpose: Statistical test that compares the performance of two classifiers to determine if their differences are significant.',
            'mcnemar_theory_application': 'Application: Scientific validation that one model is statistically superior to another (p < 0.05 = significant difference).',
            'smart_folder_system': 'Smart Folder Validation System',
            'instructions_title': 'Instructions:',
            'instructions': [
                'Organize your images by disease in each digital "folder"',
                'Minimum recommended: 30+ total images (10+ per category)',
                'The system will automatically label images according to the chosen folder'
            ],
            'disease_folders': 'Disease Folders',
            'upload_images': 'Upload images of',
            'images_loaded': 'images loaded',
            'load_images_message': 'Load images in disease folders to start statistical analysis',
            'dataset_summary': 'Dataset Summary',
            'distribution_by_disease': 'Distribution by disease:',
            'total': 'Total:',
            'images': 'images',
            'minimum_recommendation': 'At least 30 images recommended for statistically valid results',
            'sufficient_dataset': 'Sufficient dataset for robust statistical analysis',
            'process_button': 'PROCESS DATASET AND CALCULATE STATISTICS',
            'processing': 'Processing images and performing statistical analysis...',
            'analysis_completed': 'STATISTICAL ANALYSIS COMPLETED!',
            'analysis_success': 'Data processed successfully. Scientifically valid results generated.',
            'complete_visualization': 'Complete Results Visualization',
            'precision_summary': 'Precision Summary by Model',
            'mcc_analysis': 'Matthews Correlation Coefficient (MCC) Analysis',
            'best_model_identified': 'BEST MODEL IDENTIFIED',
            'based_on_mcc': 'Based on Matthews Correlation Coefficient',
            'mcc_ranking': 'MCC Ranking:',
            'mcnemar_comparisons': 'McNemar Tests - Statistical Comparisons',
            'reference_model': 'Reference model:',
            'best_according_mcc': '(best according to MCC)',
            'comparing_models': 'Comparing {model} vs the other 3 models:',
            'total_comparisons': 'Total Comparisons',
            'significant_differences': 'Significant Differences',
            'confidence_level': 'Confidence Level',
            'comparison': 'Comparison',
            'chi_square_statistic': 'χ² Statistic',
            'p_value': 'p-value',
            'significant_question': 'Significant?',
            'significant_difference': 'Significant Difference',
            'no_difference': 'No Difference',
            'interpretation': 'Interpretation:',
            'academic_interpretation': 'ACADEMIC INTERPRETATION',
            'generate_statistical_report': 'Generate Statistical Report',
            'preparing_report': 'Preparing statistical report...',
            'download_statistical_pdf': 'Download Statistical Report PDF',
            'report_ready': 'Report ready for download',
            'complete_results_available': 'Complete results are available in the \'Statistical Analysis\' tab',
            'explore_detailed_visualizations': 'Go to the previous tab to explore detailed visualizations and additional metrics.'
        },
        'info': {
            'title': 'Disease Information',
            'diseases_info': {
                'black_rot': {
                    'name': 'Black Rot',
                    'description': 'Caused by the fungus Guignardia bidwellii. One of the most destructive diseases of grapevines.',
                    'symptoms': [
                        'Circular brown spots on leaves',
                        'Black lesions on fruits',
                        'Berry mummification',
                        'Black pycnidia in infected tissues'
                    ],
                    'conditions': 'Develops in high humidity conditions and temperatures of 20-27°C'
                },
                'esca': {
                    'name': 'Esca (Black Measles)',
                    'description': 'Complex disease caused by various fungi. Affects the vascular system of the plant.',
                    'symptoms': [
                        'Interveinal discoloration in leaves',
                        'Marginal necrosis',
                        'Shoot dieback',
                        'Internal trunk rot'
                    ],
                    'conditions': 'Aggravated by water stress and poorly protected pruning wounds'
                },
                'leaf_blight': {
                    'name': 'Leaf Blight',
                    'description': 'Caused by the fungus Isariopsis. Mainly affects mature leaves.',
                    'symptoms': [
                        'Angular yellowish spots',
                        'Progressive leaf necrosis',
                        'Premature defoliation',
                        'Reduced plant vigor'
                    ],
                    'conditions': 'Favored by high relative humidity and moderate temperatures'
                }
            },
            'best_practices': 'Best Management Practices',
            'prevention': 'Prevention:',
            'prevention_items': [
                'Regular vineyard monitoring',
                'Proper sanitary pruning',
                'Canopy management',
                'Proper soil drainage',
                'Selection of resistant varieties'
            ],
            'integrated_management': 'Integrated Management:',
            'integrated_items': [
                'Rational use of fungicides',
                'Active ingredient rotation',
                'Applications at critical times',
                'Application records',
                'Efficacy evaluation'
            ],
            'statistical_tests': 'About Statistical Tests',
            'mcc_technical': 'Matthews Coefficient - Technical Information',
            'mcc_formula_title': 'MCC Formula:',
            'mcc_formula': 'MCC = (TP×TN - FP×FN) / √[(TP+FP)(TP+FN)(TN+FP)(TN+FN)]',
            'mcc_variables': [
                'TP = True Positives',
                'TN = True Negatives',
                'FP = False Positives',
                'FN = False Negatives'
            ],
            'mcc_advantages_title': 'Advantages:',
            'mcc_advantages': [
                'Balanced for all classes',
                'Robust against unbalanced datasets',
                'Easy interpretation (-1 to +1)',
                'Considers all aspects of confusion matrix'
            ],
            'mcnemar_technical': 'McNemar Test - Technical Information',
            'mcnemar_procedure': 'Procedure:',
            'mcnemar_hypothesis': 'Hypothesis:',
            'mcnemar_h0': 'H₀: No difference between models',
            'mcnemar_h1': 'H₁: Significant difference exists',
            'mcnemar_statistic': 'Test statistic:',
            'mcnemar_statistic_formula': 'χ² = (|b - c| - 0.5)² / (b + c)',
            'mcnemar_variables': 'Where b and c are disagreement frequencies between models',
            'mcnemar_decision': 'Decision:',
            'mcnemar_reject': 'If p < 0.05: Reject H₀ (difference exists)',
            'mcnemar_not_reject': 'If p ≥ 0.05: Do not reject H₀ (no difference)',
            'mcnemar_application': 'Application:',
            'mcnemar_applications': [
                'Objective model comparison',
                'Statistical basis for model selection',
                'Validation of algorithm improvements'
            ],
            'protection_calendar': 'Phytosanitary Protection Calendar',
            'phenological_stage': 'Phenological Stage',
            'main_risk': 'Main Risk',
            'recommended_action': 'Recommended Action',
            'calendar_data': {
                'stages': ['Bud break', 'Flowering', 'Fruit set', 'Veraison', 'Maturation'],
                'risks': ['Powdery mildew', 'Black rot', 'Powdery mildew/Black rot', 'Esca', 'Botrytis'],
                'actions': [
                    'Preventive fungicide',
                    'Systemic fungicide',
                    'Evaluation and application according to pressure',
                    'Intensive monitoring',
                    'Pre-harvest application if necessary'
                ]
            },
            'description': 'Description:',
            'symptoms': 'Symptoms:',
            'favorable_conditions': 'Favorable conditions:'
        }
    },
    'pt': {
        'app_title': 'VineGuard AI',
        'app_subtitle': 'Sistema Inteligente de Diagnóstico de Doenças em Vinhedos',
        'app_description': 'Com Análise Estatística Avançada (Matthews e McNemar)',
        'language_selector': 'Idioma / Language',
        'sidebar': {
            'config': 'Configuração',
            'load_models': 'Carregar Modelos',
            'models_loaded': 'Modelos prontos',
            'available_models': 'Modelos Disponíveis',
            'info_title': 'Informação',
            'info_text': '''Esta aplicação usa modelos de deep learning para detectar doenças em folhas de videira:
            
• **Podridão Negra**
• **Esca** 
• **Requeima da Folha**
• **Folhas Saudáveis**

**Análise Estatística:**
• Coeficiente de Matthews (com múltiplas imagens)
• Teste de McNemar (com múltiplas imagens)

**💡 Dica:** Use a aba 'Validação McNemar' para análise estatística completa com seu próprio conjunto de dados.''',
            'load_models_warning': 'Por favor, carregue os modelos da barra lateral'
        },
        'tabs': {
            'diagnosis': 'Diagnóstico',
            'statistical': 'Análise Estatística',
            'mcnemar': 'Validação McNemar',
            'info': 'Informação'
        },
        'diagnosis': {
            'title': 'Diagnóstico de Doenças',
            'input_method': 'Selecione o método de entrada:',
            'upload_image': 'Enviar imagem',
            'use_camera': 'Usar câmera',
            'file_uploader': 'Selecione uma imagem de folha de videira',
            'formats_help': 'Formatos suportados: JPG, JPEG, PNG',
            'image_loaded': 'Imagem carregada',
            'analyze_button': 'Analisar Imagem',
            'analyzing': 'Analisando imagem...',
            'analysis_complete': 'Análise concluída!',
            'results_title': 'Resultados do Diagnóstico',
            'consensus_title': 'Diagnóstico de Consenso',
            'final_diagnosis': 'Diagnóstico Final:',
            'agreement': 'Concordância',
            'confidence': 'Confiança',
            'probability_distribution': 'Distribuição de Probabilidades',
            'treatment_recommendations': 'Recomendações de Tratamento',
            'severity': 'Gravidade:',
            'recommended_treatment': 'Tratamento Recomendado',
            'preventive_measures': 'Medidas Preventivas',
            'generate_report': 'Gerar Relatório',
            'download_pdf': 'Baixar Relatório PDF',
            'generating_report': 'Gerando relatório...',
            'download_pdf_button': 'Baixar PDF',
            'camera_info': 'A função da câmera requer acesso ao hardware do dispositivo',
            'camera_warning': 'Por favor, use a opção de enviar imagem por enquanto'
        },
        'diseases': {
            'Black_rot': 'Podridão Negra',
            'Esca': 'Esca (Sarampo Negro)',
            'Healthy': 'Saudável',
            'Leaf_blight': 'Requeima da Folha'
        },
        'disease_folders': {
            'Black_rot': {
                'name': 'Podridão Negra',
                'description': 'Fungos Guignardia bidwellii'
            },
            'Esca': {
                'name': 'Esca (Sarampo Negro)',
                'description': 'Complexo de fungos vasculares'
            },
            'Healthy': {
                'name': 'Folhas Saudáveis',
                'description': 'Sem doenças detectáveis'
            },
            'Leaf_blight': {
                'name': 'Requeima da Folha',
                'description': 'Fungo Isariopsis'
            }
        },
        'statistical': {
            'title': 'Análise Estatística de Modelos',
            'real_data_available': 'Análise com dados reais disponível',
            'mcc_title': 'Coeficiente de Correlação de Matthews (MCC) - Dados Reais',
            'mcc_description': '''O MCC é uma métrica equilibrada que considera todos os tipos de previsões (verdadeiros/falsos positivos/negativos). 
Valores próximos a +1 indicam previsão perfeita, 0 indica previsão aleatória, e -1 indica previsão completamente incorreta.''',
            'model_ranking': 'Classificação de Modelos',
            'speed_analysis': 'Análise de Velocidade dos Modelos',
            'inference_time_distribution': 'Distribuição do Tempo de Inferência',
            'speed_comparison': 'Comparação de Velocidade',
            'fastest': 'Mais Rápido',
            'slowest': 'Mais Lento',
            'average': 'Média',
            'speed_stats': 'Estatísticas de Velocidade',
            'no_statistical_analysis': 'Análise Estatística Não Disponível',
            'statistical_info': '''Para obter análise estatística real (MCC e McNemar):
1. Vá para a aba 'Validação McNemar'
2. Carregue pelo menos 30 imagens com seus rótulos verdadeiros
3. A análise estatística aparecerá automaticamente aqui''',
            'why_multiple_images': '''**Por que você precisa de múltiplas imagens?**
- Com uma única imagem, métricas estatísticas reais não podem ser calculadas
- Pelo menos 30 amostras são necessárias para resultados confiáveis
- MCC e McNemar comparam o desempenho geral dos modelos''',
            'perform_analysis': 'Realize um diagnóstico ou validação para gerar análise estatística',
            'technical_info': {
                'mcc_description': '''- Métrica equilibrada para classificação
- Faixa: -1 (pior) a +1 (melhor)
- Considera todos os tipos de previsões
- Útil para conjuntos de dados desbalanceados
- Interpretação:
  - MCC ≥ 0.8: Muito bom
  - MCC ≥ 0.6: Bom  
  - MCC ≥ 0.4: Moderado
  - MCC < 0.4: Precisa melhoria''',
                'mcnemar_description': '''- Compara dois modelos estatisticamente
- Baseado na distribuição χ² (qui-quadrado)
- H₀: Não há diferença entre modelos
- H₁: Existe diferença significativa
- Interpretação do valor-p:
  - p < 0.001: Muito significativo
  - p < 0.01: Significativo
  - p < 0.05: Marginalmente significativo
  - p ≥ 0.05: Não significativo'''
            }
        },
        'treatments': {
            'Black_rot': {
                'title': '🔴 Podridão Negra Detectada',
                'severity': 'Alta',
                'treatment': [
                    'Aplicar fungicidas protetores (Mancozeb, Captan)',
                    'Remover e destruir todas as partes infectadas',
                    'Melhorar a circulação de ar no vinhedo',
                    'Evitar irrigação por aspersão'
                ],
                'prevention': [
                    'Podar adequadamente para melhorar ventilação',
                    'Aplicar fungicidas preventivos antes da floração',
                    'Remover restos de poda e folhas caídas'
                ]
            },
            'Esca': {
                'title': '🟤 Esca (Sarampo Negro) Detectada',
                'severity': 'Muito Alta',
                'treatment': [
                    'Não existe cura direta - foco na prevenção',
                    'Podar partes afetadas com ferramentas desinfetadas',
                    'Aplicar pasta cicatrizante em cortes de poda',
                    'Considerar substituição de plantas severamente afetadas'
                ],
                'prevention': [
                    'Evitar podas tardias e em dias úmidos',
                    'Desinfetar ferramentas entre plantas',
                    'Proteger feridas de poda imediatamente'
                ]
            },
            'Healthy': {
                'title': '✅ Planta Saudável',
                'severity': 'Nenhuma',
                'treatment': [
                    'Nenhum tratamento necessário',
                    'Manter práticas atuais de manejo'
                ],
                'prevention': [
                    'Continuar monitoramento regular',
                    'Manter programa preventivo de fungicidas',
                    'Garantir nutrição equilibrada',
                    'Manter boa drenagem do solo'
                ]
            },
            'Leaf_blight': {
                'title': '🟡 Requeima da Folha Detectada',
                'severity': 'Moderada',
                'treatment': [
                    'Aplicar fungicidas sistêmicos (Azoxistrobina, Tebuconazol)',
                    'Remover folhas infectadas',
                    'Melhorar drenagem do solo',
                    'Reduzir densidade da folhagem'
                ],
                'prevention': [
                    'Evitar excesso de nitrogênio',
                    'Manter folhagem seca',
                    'Aplicar fungicidas preventivos em épocas úmidas'
                ]
            }
        },
        'mcnemar': {
            'title': 'Validação Estatística com Conjunto de Dados Real',
            'theoretical_foundations': 'Fundamentos Teóricos',
            'mcc_theory_title': '🧮 Coeficiente de Correlação de Matthews (MCC)',
            'mcc_theory_formula': 'Fórmula: MCC = (TP×TN - FP×FN) / √[(TP+FP)(TP+FN)(TN+FP)(TN+FN)]',
            'mcc_theory_purpose': 'Propósito: Métrica equilibrada que avalia a qualidade geral de classificação considerando todas as categorias de previsão.',
            'mcc_theory_advantages': 'Vantagens: Robusto contra classes desbalanceadas, interpretação intuitiva (-1 a +1), e considera todos os aspectos da matriz de confusão.',
            'mcnemar_theory_title': '🔬 Teste de McNemar',
            'mcnemar_theory_formula': 'Fórmula: χ² = (|b - c| - 0.5)² / (b + c)',
            'mcnemar_theory_purpose': 'Propósito: Teste estatístico que compara o desempenho de dois classificadores para determinar se suas diferenças são significativas.',
            'mcnemar_theory_application': 'Aplicação: Validação científica de que um modelo é estatisticamente superior a outro (p < 0.05 = diferença significativa).',
            'smart_folder_system': 'Sistema de Validação por Pastas Inteligentes',
            'instructions_title': 'Instruções:',
            'instructions': [
                'Organize suas imagens por doença em cada "pasta" digital',
                'Mínimo recomendado: 30+ imagens totais (10+ por categoria)',
                'O sistema automaticamente rotulará as imagens de acordo com a pasta escolhida'
            ],
            'disease_folders': 'Pastas de Doenças',
            'upload_images': 'Enviar imagens de',
            'images_loaded': 'imagens carregadas',
            'load_images_message': 'Carregue imagens nas pastas de doenças para começar a análise estatística',
            'dataset_summary': 'Resumo do Conjunto de Dados',
            'distribution_by_disease': 'Distribuição por doença:',
            'total': 'Total:',
            'images': 'imagens',
            'minimum_recommendation': 'Pelo menos 30 imagens recomendadas para resultados estatisticamente válidos',
            'sufficient_dataset': 'Conjunto de dados suficiente para análise estatística robusta',
            'process_button': 'PROCESSAR CONJUNTO DE DADOS E CALCULAR ESTATÍSTICAS',
            'processing': 'Processando imagens e realizando análise estatística...',
            'analysis_completed': 'ANÁLISE ESTATÍSTICA CONCLUÍDA!',
            'analysis_success': 'Dados processados com sucesso. Resultados cientificamente válidos gerados.',
            'complete_visualization': 'Visualização Completa de Resultados',
            'precision_summary': 'Resumo de Precisão por Modelo',
            'mcc_analysis': 'Análise do Coeficiente de Correlação de Matthews (MCC)',
            'best_model_identified': 'MELHOR MODELO IDENTIFICADO',
            'based_on_mcc': 'Baseado no Coeficiente de Correlação de Matthews',
            'mcc_ranking': 'Classificação por MCC:',
            'mcnemar_comparisons': 'Testes de McNemar - Comparações Estatísticas',
            'reference_model': 'Modelo de referência:',
            'best_according_mcc': '(melhor de acordo com MCC)',
            'comparing_models': 'Comparando {model} vs os outros 3 modelos:',
            'total_comparisons': 'Total de Comparações',
            'significant_differences': 'Diferenças Significativas',
            'confidence_level': 'Nível de Confiança',
            'comparison': 'Comparação',
            'chi_square_statistic': 'Estatística χ²',
            'p_value': 'valor-p',
            'significant_question': 'Significativo?',
            'significant_difference': 'Diferença Significativa',
            'no_difference': 'Sem Diferença',
            'interpretation': 'Interpretação:',
            'academic_interpretation': 'INTERPRETAÇÃO ACADÊMICA',
            'generate_statistical_report': 'Gerar Relatório Estatístico',
            'preparing_report': 'Preparando relatório estatístico...',
            'download_statistical_pdf': 'Baixar Relatório Estatístico PDF',
            'report_ready': 'Relatório pronto para download',
            'complete_results_available': 'Resultados completos estão disponíveis na aba \'Análise Estatística\'',
            'explore_detailed_visualizations': 'Vá para a aba anterior para explorar visualizações detalhadas e métricas adicionais.'
        },
        'info': {
            'title': 'Informações sobre Doenças',
            'diseases_info': {
                'black_rot': {
                    'name': 'Podridão Negra',
                    'description': 'Causada pelo fungo Guignardia bidwellii. Uma das doenças mais destrutivas da videira.',
                    'symptoms': [
                        'Manchas circulares marrons nas folhas',
                        'Lesões negras nos frutos',
                        'Mumificação das bagas',
                        'Picnídios negros em tecidos infectados'
                    ],
                    'conditions': 'Desenvolve-se em condições de alta umidade e temperaturas de 20-27°C'
                },
                'esca': {
                    'name': 'Esca (Sarampo Negro)',
                    'description': 'Doença complexa causada por vários fungos. Afeta o sistema vascular da planta.',
                    'symptoms': [
                        'Descoloração intervenal nas folhas',
                        'Necrose marginal',
                        'Morte regressiva de brotos',
                        'Podridão interna do tronco'
                    ],
                    'conditions': 'Agravada por estresse hídrico e feridas de poda mal protegidas'
                },
                'leaf_blight': {
                    'name': 'Requeima da Folha',
                    'description': 'Causada pelo fungo Isariopsis. Afeta principalmente folhas maduras.',
                    'symptoms': [
                        'Manchas angulares amareladas',
                        'Necrose foliar progressiva',
                        'Desfolhação prematura',
                        'Redução do vigor da planta'
                    ],
                    'conditions': 'Favorecida por alta umidade relativa e temperaturas moderadas'
                }
            },
            'best_practices': 'Melhores Práticas de Manejo',
            'prevention': 'Prevenção:',
            'prevention_items': [
                'Monitoramento regular do vinhedo',
                'Poda sanitária adequada',
                'Manejo do dossel vegetal',
                'Drenagem apropriada do solo',
                'Seleção de variedades resistentes'
            ],
            'integrated_management': 'Manejo Integrado:',
            'integrated_items': [
                'Uso racional de fungicidas',
                'Rotação de ingredientes ativos',
                'Aplicações em momentos críticos',
                'Registro de aplicações',
                'Avaliação de eficácia'
            ],
            'statistical_tests': 'Sobre os Testes Estatísticos',
            'mcc_technical': 'Coeficiente de Matthews - Informação Técnica',
            'mcc_formula_title': 'Fórmula do MCC:',
            'mcc_formula': 'MCC = (TP×TN - FP×FN) / √[(TP+FP)(TP+FN)(TN+FP)(TN+FN)]',
            'mcc_variables': [
                'TP = Verdadeiros Positivos',
                'TN = Verdadeiros Negativos',
                'FP = Falsos Positivos',
                'FN = Falsos Negativos'
            ],
            'mcc_advantages_title': 'Vantagens:',
            'mcc_advantages': [
                'Equilibrado para todas as classes',
                'Robusto contra conjuntos de dados desbalanceados',
                'Interpretação fácil (-1 a +1)',
                'Considera todos os aspectos da matriz de confusão'
            ],
            'mcnemar_technical': 'Teste de McNemar - Informação Técnica',
            'mcnemar_procedure': 'Procedimento:',
            'mcnemar_hypothesis': 'Hipótese:',
            'mcnemar_h0': 'H₀: Não há diferença entre modelos',
            'mcnemar_h1': 'H₁: Existe diferença significativa',
            'mcnemar_statistic': 'Estatística de teste:',
            'mcnemar_statistic_formula': 'χ² = (|b - c| - 0.5)² / (b + c)',
            'mcnemar_variables': 'Onde b e c são frequências de desacordo entre modelos',
            'mcnemar_decision': 'Decisão:',
            'mcnemar_reject': 'Se p < 0.05: Rejeitar H₀ (diferença existe)',
            'mcnemar_not_reject': 'Se p ≥ 0.05: Não rejeitar H₀ (sem diferença)',
            'mcnemar_application': 'Aplicação:',
            'mcnemar_applications': [
                'Comparação objetiva de modelos',
                'Base estatística para seleção de modelos',
                'Validação de melhorias em algoritmos'
            ],
            'protection_calendar': 'Calendário de Proteção Fitossanitária',
            'phenological_stage': 'Estágio Fenológico',
            'main_risk': 'Risco Principal',
            'recommended_action': 'Ação Recomendada',
            'calendar_data': {
                'stages': ['Brotação', 'Floração', 'Frutificação', 'Veraison', 'Maturação'],
                'risks': ['Oídio', 'Podridão negra', 'Oídio/Podridão negra', 'Esca', 'Botrítis'],
                'actions': [
                    'Fungicida preventivo',
                    'Fungicida sistêmico',
                    'Avaliação e aplicação conforme pressão',
                    'Monitoramento intensivo',
                    'Aplicação pré-colheita se necessário'
                ]
            },
            'description': 'Descrição:',
            'symptoms': 'Sintomas:',
            'favorable_conditions': 'Condições favoráveis:'
        }
    },
    'zh': {
        'app_title': 'VineGuard AI',
        'app_subtitle': '葡萄园智能疾病诊断系统',
        'app_description': '具有高级统计分析功能 (Matthews & McNemar)',
        'language_selector': '语言 / Language',
        'sidebar': {
            'config': '配置',
            'load_models': '加载模型',
            'models_loaded': '模型已就绪',
            'available_models': '可用模型',
            'info_title': '信息',
            'info_text': '''此应用程序使用深度学习模型检测葡萄叶疾病：
            
• **黑腐病**
• **埃斯卡病** 
• **叶枯病**
• **健康叶子**

**统计分析:**
• Matthews系数 (使用多张图像)
• McNemar测试 (使用多张图像)

**💡 提示:** 使用'McNemar验证'选项卡对您自己的数据集进行完整统计分析。''',
            'load_models_warning': '请从侧边栏加载模型'
        },
        'tabs': {
            'diagnosis': '诊断',
            'statistical': '统计分析',
            'mcnemar': 'McNemar验证',
            'info': '信息'
        },
        'diagnosis': {
            'title': '疾病诊断',
            'input_method': '选择输入方法：',
            'upload_image': '上传图像',
            'use_camera': '使用相机',
            'file_uploader': '选择葡萄叶图像',
            'formats_help': '支持的格式：JPG、JPEG、PNG',
            'image_loaded': '图像已加载',
            'analyze_button': '分析图像',
            'analyzing': '正在分析图像...',
            'analysis_complete': '分析完成！',
            'results_title': '诊断结果',
            'consensus_title': '共识诊断',
            'final_diagnosis': '最终诊断：',
            'agreement': '一致性',
            'confidence': '置信度',
            'probability_distribution': '概率分布',
            'treatment_recommendations': '治疗建议',
            'severity': '严重程度：',
            'recommended_treatment': '推荐治疗',
            'preventive_measures': '预防措施',
            'generate_report': '生成报告',
            'download_pdf': '下载PDF报告',
            'generating_report': '正在生成报告...',
            'download_pdf_button': '下载PDF',
            'camera_info': '相机功能需要设备硬件访问',
            'camera_warning': '请暂时使用上传图像选项'
        },
        'diseases': {
            'Black_rot': '黑腐病',
            'Esca': '埃斯卡病',
            'Healthy': '健康',
            'Leaf_blight': '叶枯病'
        },
        'disease_folders': {
            'Black_rot': {
                'name': '黑腐病',
                'description': 'Guignardia bidwellii真菌'
            },
            'Esca': {
                'name': '埃斯卡病',
                'description': '血管真菌复合体'
            },
            'Healthy': {
                'name': '健康叶子',
                'description': '无可检测疾病'
            },
            'Leaf_blight': {
                'name': '叶枯病',
                'description': 'Isariopsis真菌'
            }
        },
        'statistical': {
            'title': '模型统计分析',
            'real_data_available': '可获得真实数据分析',
            'mcc_title': 'Matthews相关系数 (MCC) - 真实数据',
            'mcc_description': '''MCC是一个平衡的度量，考虑所有类型的预测（真/假正例/负例）。
接近+1的值表示完美预测，0表示随机预测，-1表示完全错误的预测。''',
            'model_ranking': '模型排名',
            'speed_analysis': '模型速度分析',
            'inference_time_distribution': '推理时间分布',
            'speed_comparison': '速度比较',
            'fastest': '最快',
            'slowest': '最慢',
            'average': '平均',
            'speed_stats': '速度统计',
            'no_statistical_analysis': '统计分析不可用',
            'statistical_info': '''要获得真实的统计分析（MCC和McNemar）：
1. 转到'McNemar验证'选项卡
2. 加载至少30张带有真实标签的图像
3. 统计分析将自动出现在这里''',
            'why_multiple_images': '''**为什么需要多张图像？**
- 使用单张图像无法计算真实的统计指标
- 至少需要30个样本才能获得可靠的结果
- MCC和McNemar比较模型的整体性能''',
            'perform_analysis': '执行诊断或验证以生成统计分析',
            'technical_info': {
                'mcc_description': '''- 分类的平衡指标
- 范围：-1（最差）到+1（最好）
- 考虑所有类型的预测
- 对不平衡数据集有用
- 解释：
  - MCC ≥ 0.8：非常好
  - MCC ≥ 0.6：好  
  - MCC ≥ 0.4：中等
  - MCC < 0.4：需要改进''',
                'mcnemar_description': '''- 统计比较两个模型
- 基于χ²（卡方）分布
- H₀：模型间无差异
- H₁：存在显著差异
- p值解释：
  - p < 0.001：非常显著
  - p < 0.01：显著
  - p < 0.05：边际显著
  - p ≥ 0.05：不显著'''
            }
        },
        'treatments': {
            'Black_rot': {
                'title': '🔴 检测到黑腐病',
                'severity': '高',
                'treatment': [
                    '施用保护性杀菌剂（代森锰锌、克菌丹）',
                    '清除并销毁所有感染部位',
                    '改善葡萄园空气流通',
                    '避免喷灌'
                ],
                'prevention': [
                    '适当修剪以改善通风',
                    '开花前施用预防性杀菌剂',
                    '清除修剪残留物和落叶'
                ]
            },
            'Esca': {
                'title': '🟤 检测到埃斯卡病（黑麻疹）',
                'severity': '很高',
                'treatment': [
                    '没有直接治愈方法 - 重点预防',
                    '用消毒工具修剪受影响部位',
                    '在修剪切口涂抹愈合膏',
                    '考虑更换严重受影响的植株'
                ],
                'prevention': [
                    '避免晚期修剪和在潮湿天气修剪',
                    '在植株间消毒工具',
                    '立即保护修剪伤口'
                ]
            },
            'Healthy': {
                'title': '✅ 健康植株',
                'severity': '无',
                'treatment': [
                    '无需治疗',
                    '维持当前管理做法'
                ],
                'prevention': [
                    '继续定期监测',
                    '维持预防性杀菌剂计划',
                    '确保营养平衡',
                    '保持土壤排水良好'
                ]
            },
            'Leaf_blight': {
                'title': '🟡 检测到叶枯病',
                'severity': '中等',
                'treatment': [
                    '施用内吸性杀菌剂（嘧菌酯、戊唑醇）',
                    '清除感染叶片',
                    '改善土壤排水',
                    '减少叶面密度'
                ],
                'prevention': [
                    '避免过量氮肥',
                    '保持叶面干燥',
                    '在潮湿季节施用预防性杀菌剂'
                ]
            }
        },
        'mcnemar': {
            'title': '真实数据集统计验证',
            'theoretical_foundations': '理论基础',
            'mcc_theory_title': '🧮 Matthews相关系数 (MCC)',
            'mcc_theory_formula': '公式: MCC = (TP×TN - FP×FN) / √[(TP+FP)(TP+FN)(TN+FP)(TN+FN)]',
            'mcc_theory_purpose': '目的: 平衡指标，通过考虑所有预测类别来评估分类的整体质量。',
            'mcc_theory_advantages': '优势: 对不平衡类别鲁棒，直观解释（-1到+1），并考虑混淆矩阵的所有方面。',
            'mcnemar_theory_title': '🔬 McNemar测试',
            'mcnemar_theory_formula': '公式: χ² = (|b - c| - 0.5)² / (b + c)',
            'mcnemar_theory_purpose': '目的: 统计测试，比较两个分类器的性能，确定它们的差异是否显著。',
            'mcnemar_theory_application': '应用: 科学验证一个模型在统计上优于另一个模型（p < 0.05 = 显著差异）。',
            'smart_folder_system': '智能文件夹验证系统',
            'instructions_title': '说明:',
            'instructions': [
                '按疾病在每个数字"文件夹"中组织您的图像',
                '建议最少: 30+张总图像（每类10+张）',
                '系统将根据选择的文件夹自动标记图像'
            ],
            'disease_folders': '疾病文件夹',
            'upload_images': '上传图像',
            'images_loaded': '张图像已加载',
            'load_images_message': '在疾病文件夹中加载图像以开始统计分析',
            'dataset_summary': '数据集摘要',
            'distribution_by_disease': '按疾病分布:',
            'total': '总计:',
            'images': '张图像',
            'minimum_recommendation': '建议至少30张图像以获得统计有效结果',
            'sufficient_dataset': '足够的数据集进行稳健的统计分析',
            'process_button': '处理数据集并计算统计数据',
            'processing': '正在处理图像并进行统计分析...',
            'analysis_completed': '统计分析完成！',
            'analysis_success': '数据处理成功。生成了科学有效的结果。',
            'complete_visualization': '完整结果可视化',
            'precision_summary': '按模型精度摘要',
            'mcc_analysis': 'Matthews相关系数 (MCC) 分析',
            'best_model_identified': '识别出最佳模型',
            'based_on_mcc': '基于Matthews相关系数',
            'mcc_ranking': 'MCC排名:',
            'mcnemar_comparisons': 'McNemar测试 - 统计比较',
            'reference_model': '参考模型:',
            'best_according_mcc': '（根据MCC最佳）',
            'comparing_models': '比较{model}与其他3个模型:',
            'total_comparisons': '总比较次数',
            'significant_differences': '显著差异',
            'confidence_level': '置信水平',
            'comparison': '比较',
            'chi_square_statistic': 'χ²统计量',
            'p_value': 'p值',
            'significant_question': '显著？',
            'significant_difference': '显著差异',
            'no_difference': '无差异',
            'interpretation': '解释:',
            'academic_interpretation': '学术解释',
            'generate_statistical_report': '生成统计报告',
            'preparing_report': '正在准备统计报告...',
            'download_statistical_pdf': '下载统计报告PDF',
            'report_ready': '报告准备下载',
            'complete_results_available': '完整结果在"统计分析"选项卡中可用',
            'explore_detailed_visualizations': '转到上一个选项卡以探索详细可视化和其他指标。'
        },
        'info': {
            'title': '疾病信息',
            'diseases_info': {
                'black_rot': {
                    'name': '黑腐病',
                    'description': '由Guignardia bidwellii真菌引起。葡萄藤最具破坏性的疾病之一。',
                    'symptoms': [
                        '叶片上出现圆形褐色斑点',
                        '果实上出现黑色病变',
                        '浆果木乃伊化',
                        '感染组织中的黑色分生孢子器'
                    ],
                    'conditions': '在高湿度和20-27°C温度条件下发展'
                },
                'esca': {
                    'name': '埃斯卡病（黑麻疹）',
                    'description': '由多种真菌引起的复杂疾病。影响植物的维管系统。',
                    'symptoms': [
                        '叶片脉间变色',
                        '边缘坏死',
                        '枝梢回枯',
                        '主干内部腐烂'
                    ],
                    'conditions': '因水分胁迫和修剪伤口保护不当而加剧'
                },
                'leaf_blight': {
                    'name': '叶枯病',
                    'description': '由Isariopsis真菌引起。主要影响成熟叶片。',
                    'symptoms': [
                        '角状黄色斑点',
                        '进行性叶片坏死',
                        '过早落叶',
                        '植物活力下降'
                    ],
                    'conditions': '在高相对湿度和适中温度下有利'
                }
            },
            'best_practices': '最佳管理实践',
            'prevention': '预防:',
            'prevention_items': [
                '定期葡萄园监测',
                '适当的卫生修剪',
                '冠层管理',
                '适当的土壤排水',
                '选择抗性品种'
            ],
            'integrated_management': '综合管理:',
            'integrated_items': [
                '合理使用杀菌剂',
                '活性成分轮换',
                '在关键时期施用',
                '施用记录',
                '效果评估'
            ],
            'statistical_tests': '关于统计测试',
            'mcc_technical': 'Matthews系数 - 技术信息',
            'mcc_formula_title': 'MCC公式:',
            'mcc_formula': 'MCC = (TP×TN - FP×FN) / √[(TP+FP)(TP+FN)(TN+FP)(TN+FN)]',
            'mcc_variables': [
                'TP = 真正例',
                'TN = 真负例',
                'FP = 假正例',
                'FN = 假负例'
            ],
            'mcc_advantages_title': '优势:',
            'mcc_advantages': [
                '对所有类别平衡',
                '对不平衡数据集鲁棒',
                '易于解释（-1到+1）',
                '考虑混淆矩阵的所有方面'
            ],
            'mcnemar_technical': 'McNemar测试 - 技术信息',
            'mcnemar_procedure': '程序:',
            'mcnemar_hypothesis': '假设:',
            'mcnemar_h0': 'H₀: 模型间无差异',
            'mcnemar_h1': 'H₁: 存在显著差异',
            'mcnemar_statistic': '测试统计量:',
            'mcnemar_statistic_formula': 'χ² = (|b - c| - 0.5)² / (b + c)',
            'mcnemar_variables': '其中b和c是模型间的不一致频率',
            'mcnemar_decision': '决策:',
            'mcnemar_reject': '如果p < 0.05: 拒绝H₀（存在差异）',
            'mcnemar_not_reject': '如果p ≥ 0.05: 不拒绝H₀（无差异）',
            'mcnemar_application': '应用:',
            'mcnemar_applications': [
                '客观模型比较',
                '模型选择的统计基础',
                '算法改进的验证'
            ],
            'protection_calendar': '植保防护日历',
            'phenological_stage': '物候期',
            'main_risk': '主要风险',
            'recommended_action': '推荐行动',
            'calendar_data': {
                'stages': ['萌芽期', '开花期', '座果期', '转色期', '成熟期'],
                'risks': ['白粉病', '黑腐病', '白粉病/黑腐病', '埃斯卡病', '灰霉病'],
                'actions': [
                    '预防性杀菌剂',
                    '内吸性杀菌剂',
                    '根据压力评估和施用',
                    '密集监测',
                    '必要时采前施用'
                ]
            },
            'description': '描述:',
            'symptoms': '症状:',
            'favorable_conditions': '有利条件:'
        },
        'detailed_recommendations': '详细建议',
        'for_diagnosis': '诊断结果',
        'additional_info': '附加信息',
        'consult_specialist': '咨询葡萄栽培专家',
        'follow_treatment_schedule': '遵循定期治疗计划',
        'monitor_evolution': '监测疾病进展',
        'document_treatments': '记录所有应用的治疗',
        'no_specific_recommendations': '无特定建议可用',
        'disease_classes': {
            'Black_rot': '黑腐病',
            'Esca': '埃斯卡病（黑麻疹)',
            'Healthy': '健康',
            'Leaf_blight': '叶枯病'
        }
    }
}


def t(key, lang=None):
    """
    Función helper para obtener texto traducido
    Args:
        key: Clave de traducción (ej: 'app_title' o 'sidebar.config')
        lang: Idioma (si no se especifica, usa el del session_state)
    """
    if lang is None:
        lang = st.session_state.get('language', 'es')

    # Navegar por claves anidadas (ej: 'sidebar.config')
    keys = key.split('.')
    value = TRANSLATIONS[lang]

    try:
        for k in keys:
            value = value[k]
        return value
    except (KeyError, TypeError):
        # Fallback al español si no se encuentra la traducción
        try:
            value = TRANSLATIONS['es']
            for k in keys:
                value = value[k]
            return f"[ES] {value}"
        except:
            return f"Missing translation: {key}"

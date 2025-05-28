import pandas as pd
import os

def analyze_crates(pgn_file, modules_file, plc_templates_dir, scada_templates_dir):
    """
    Анализирует крейты в файле PGN на основе списка модулей Regul и проверяет наличие файлов с именами типов модулей.

    Args:
        pgn_file (str): Путь к файлу "PGN.xlsx".
        modules_file (str): Путь к файлу "Список_модулей_Regul.xlsx".
        plc_templates_dir (str): Путь к папке "_templates/PLC" с XML файлами для PLC.
        scada_templates_dir (str): Путь к папке "_templates/SCADA" с XML файлами для SCADA.

    Returns:
        tuple: Кортеж, содержащий:
            - crates (list): Список словарей, где каждый словарь представляет крейт.
                              Каждый крейт содержит список модулей и информацию о них:
                              [{'modules': [{'BOX': ..., 'UNIT_POSITION': ..., 'MODULE_CATALOG': ...}, ...]}, ...]
            - is_redundant (bool): True, если система резервированная, иначе False.
    """

    # 1. Чтение данных из файлов Excel
    try:
        ascfg = pd.read_excel(pgn_file, sheet_name="AsCfg")
        astags = pd.read_excel(pgn_file, sheet_name="AsTags")
        list_modules = pd.read_excel(modules_file, sheet_name="Sheet1")
    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден: {e.filename}")
        return [], False
    except Exception as e:
        print(f"Ошибка при чтении файлов Excel: {e}")
        return [], False

    # 2. Подготовка данных из списка модулей
    start_modules = list_modules[list_modules['TYPE'].astype(str).str.contains("ST_IN", na=False)]['NAME'].tolist()
    end_modules = list_modules[list_modules['TYPE'].astype(str).str.contains("ST_OUT", na=False)]['NAME'].tolist()

    # 3. Определение крейтов
    crates = []
    current_crate = None

    for index, row in ascfg.iterrows():
        module_name = row['MODULE_CATALOG']
        module_name_str = str(module_name).strip()

        if module_name_str in start_modules and current_crate is None:
            current_crate = {'modules': []}
            current_crate['modules'].append({
                'BOX': row['BOX'],
                'UNIT_POSITION': row['UNIT_POSITION'],
                'MODULE_CATALOG': row['MODULE_CATALOG']
            })
        elif current_crate is not None:
            current_crate['modules'].append({
                'BOX': row['BOX'],
                'UNIT_POSITION': row['UNIT_POSITION'],
                'MODULE_CATALOG': row['MODULE_CATALOG']
            })

            if module_name_str in end_modules:
                crates.append(current_crate)
                current_crate = None

    # 4. Определение резервированности системы
    is_redundant = False
    if len(crates) >= 2:
        if len(crates[0]['modules']) == len(crates[1]['modules']):
            is_redundant = True
            for i in range(len(crates[0]['modules'])):
                if crates[0]['modules'][i]['MODULE_CATALOG'] != crates[1]['modules'][i]['MODULE_CATALOG']:
                    is_redundant = False
                    break

    # 5. Проверка наличия файлов с именами типов модулей
    def check_module_file(module_catalog, templates_dir, system_name):
        # Обрезаем строку до символа "[" , если он есть
        if "[" in module_catalog:
            module_catalog = module_catalog.split("[")[0].strip()  # Разделяем по "[" и берем первую часть, убираем пробелы
        filename = f"{module_catalog}.xml"
        file_path = os.path.join(templates_dir, filename)
        if not os.path.exists(file_path):
            print(f"Неизвестный для {system_name} тип модуля: отсутствует файл {filename}")


    if crates:
        module_catalogs = set()
        for crate in crates:
            for module in crate['modules']:
                module_catalogs.add(module['MODULE_CATALOG'])

        for module_catalog in module_catalogs:
            check_module_file(module_catalog, plc_templates_dir, "PLC")
            check_module_file(module_catalog, scada_templates_dir, "SCADA")

    return crates, is_redundant


# Пример использования:
if __name__ == "__main__":
    pgn_file = "_files/PGN_Krasnodar2_SURG_v9_KVI.xlsx"  # Замените на фактический путь к вашему файлу
    modules_file = "_files/Список_модулей_Regul.xlsx"  # Замените на фактический путь к вашему файлу
    plc_templates_dir = "_templates/PLC"  # Замените на фактический путь к вашей папке PLC templates
    scada_templates_dir = "_templates/SCADA"  # Замените на фактический путь к вашей папке SCADA templates

    crates, is_redundant = analyze_crates(pgn_file, modules_file, plc_templates_dir, scada_templates_dir)

    if crates:
        print("Крейты:")
        for i, crate in enumerate(crates):
            print(f"Крейт {i+1}:")
            for module in crate['modules']:
                print(f"  BOX: {module['BOX']}, UNIT_POSITION: {module['UNIT_POSITION']}, MODULE_CATALOG: {module['MODULE_CATALOG']}")
    else:
        print("Крейты не найдены.")

    if is_redundant:
        print("Система является резервированной.")
    else:
        print("Система не является резервированной.")

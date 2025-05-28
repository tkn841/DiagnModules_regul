
import pandas as pd
import os
# Импортируем классы RegulBus и RegulBusOs
from _templates.PLC.regulBus import RegulBus
from _templates.PLC.regulBusOs import RegulBusOs

class DataProcessor:
    def __init__(self):
        self.info_df = None
        self.ascfg_df = None
        self.list_modules = None
        self.info_data = None # Добавляем атрибут для хранения info_data

        # Define column name mappings
        self.column_mapping = {
            "<@BOX>": "BOX",
            "<@UNIT_POSITION>": "UNIT_POSITION",
            "<@MODULE_CATALOG>": "MODULE_CATALOG",
            "<@ADDR_IN>": "ADDR_IN",
            "<@ADDR_OUT>": "ADDR_OUT",
            "<@MODULE_SN>": "MODULE_SN",
            "<@MODULE_FW>": "MODULE_FW",
            "<@RESERVE_TYPE>": "RESERVE_TYPE",
            "<@THERMAL_SRC>": "THERMAL_SRC",
            "<@№>": "№",
            "<@NAME>": "NAME",
            "<@Regul_Bus>": "Regul_Bus",
            "<@Regul_Bus_OS>": "Regul_Bus_OS",
            "<@TYPE>": "TYPE",
            "<@PROFILE>": "PROFILE",
            "<@1>": "1"  # Represents the first column mentioned in the problem description.
        }


    def read_excel_file(self, file_path, sheet_name, header_row=1):
        """
        Читает XLSX файл и возвращает DataFrame.

        Args:
            file_path (str): Путь к файлу XLSX.
            sheet_name (str): Имя листа для чтения.
            header_row (int): Номер строки, используемой в качестве заголовка (1 или 2).

        Returns:
            pandas.DataFrame: DataFrame, созданный из данных листа.
        """
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row - 1)

            # Rename columns using the mapping
            df = df.rename(columns=self.column_mapping)
            return df
        except FileNotFoundError:
            print(f"Ошибка: Файл не найден по пути: {file_path}")
            return None
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}, лист {sheet_name}: {e}")
            return None

    def read_data(self):
        """
        Читает данные из файлов "PGN.xlsx" и "Список_модулей_Regul.xlsx".
        """
        self.info_df = self.read_excel_file("_files/PGN.xlsx", "Info", header_row=2)
        self.ascfg_df = self.read_excel_file("_files/PGN.xlsx", "AsCfg", header_row=1)
        self.list_modules = self.read_excel_file("_files/Список_модулей_Regul.xlsx", "Sheet1", header_row=1)

        if self.info_df is None or self.ascfg_df is None or self.list_modules is None:
            raise ValueError("Ошибка при чтении файлов. Проверьте пути и формат файлов.")

    def extract_info_data(self):
        """
        Извлекает данные из info_df и возвращает словарь.

        Returns:
            dict: Словарь, где ключ - PROFILE, значение - значение в столбце 1.
        """
        if self.info_df is None:
            print("Ошибка: info_df не загружен.")
            return None

        profile_keys = [
            "INFO_KKS_a1", "INFO_KKS_a2", "INFO_KKS_a3",
            "INFO_DESCRIPTION_a1", "INFO_DESCRIPTION_a2", "INFO_DESCRIPTION_a3", "INFO_BOX_MSKU",
            "INFO_BOX_RIO1", "INFO_BOX_RIO2", "INFO_BOX_RIO3", "INFO_BOX_RIO4",
            "INFO_BOX_RIO5", "INFO_BOX_RIO6", "INFO_BOX_RIO7", "INFO_BOX_RIO8",
            "INFO_BOX_RIO9", "INFO_BOX_RIO10", "INFO_BOX_RIO11", "INFO_BOX_RIO12",
            "INFO_BOX_RIO13", "INFO_BOX_RIO14", "INFO_BOX_RIO15", "INFO_BUS_TYPE"
        ]

        data_dict = {}
        for key in profile_keys:
            try:
                # Используем .loc для доступа к строкам по значению в столбце 'PROFILE'
                row = self.info_df.loc[self.info_df['PROFILE'] == key]

                # Проверяем, что строка найдена, и берем значение из столбца '1'
                if not row.empty:
                    data_dict[key] = row['1'].values[0]  # .values[0] чтобы получить значение, а не Series
                else:
                    data_dict[key] = None  # Или другое значение по умолчанию, если строка не найдена
                    print(f"Предупреждение: Значение для PROFILE '{key}' не найдено.")

            except KeyError as e:
                print(f"Ошибка: Столбец '{e}' не найден в DataFrame info_df.")
                return None
            except Exception as e:
                print(f"Произошла ошибка при обработке ключа '{key}': {e}")
                return None

        return data_dict


    def find_crates(self):
        """
        Определяет корзины с устройствами на основе ascfg_df и list_modules.

        Returns:
            list: Список корзин, где каждая корзина - это список словарей с информацией о модуле.
        """
        if self.ascfg_df is None or self.list_modules is None:
            print("Ошибка: ascfg_df или list_modules не загружены.")
            return None

        crates = []
        current_crate = []
        in_crate = False

        # Преобразуем столбец 'TYPE' в list_modules в множество для быстрого поиска
        st_in_modules = set(
            self.list_modules[self.list_modules['TYPE'] == 'ST_IN']['NAME'])
        st_out_modules = set(
            self.list_modules[self.list_modules['TYPE'] == 'ST_OUT']['NAME'])

        for index, row in self.ascfg_df.iterrows():
            module_name = row['MODULE_CATALOG']
            if module_name in st_in_modules:
                if in_crate:  # Закрываем предыдущий крейт, если он был открыт
                    crates.append(current_crate)
                    current_crate = []
                in_crate = True
                current_crate.append({
                    "BOX": row['BOX'],
                    "UNIT_POSITION": row['UNIT_POSITION'],
                    "MODULE_CATALOG": row['MODULE_CATALOG']
                })
            elif module_name in st_out_modules:
                if in_crate:
                    current_crate.append({
                        "BOX": row['BOX'],
                        "UNIT_POSITION": row['UNIT_POSITION'],
                        "MODULE_CATALOG": row['MODULE_CATALOG']
                    })
                    crates.append(current_crate)
                    current_crate = []
                    in_crate = False
            elif in_crate:
                current_crate.append({
                    "BOX": row['BOX'],
                    "UNIT_POSITION": row['UNIT_POSITION'],
                    "MODULE_CATALOG": row['MODULE_CATALOG']
                })

        # Если крейт остался открытым в конце, закрываем его
        if current_crate:
            crates.append(current_crate)

        return crates

    def is_redundant_system(self, crates):
        """
        Определяет, является ли система резервированной, сравнивая первые два крейта.

        Args:
            crates (list): Список корзин, полученный из find_crates().

        Returns:
            bool: True, если система резервированная, False в противном случае.
        """
        if len(crates) < 2:
            return False

        crate1 = crates[0]
        crate2 = crates[1]

        if len(crate1) != len(crate2):
            return False

        for i in range(len(crate1)):
            if crate1[i]["MODULE_CATALOG"] != crate2[i]["MODULE_CATALOG"]:
                return False

        return True

    def check_module_types(self, crates):
        """
        Проверяет, известны ли все типы модулей в crates классам RegulBus и RegulBusOs.

        Args:
            crates (list): Список корзин, полученный из find_crates().
        """
        regul_bus = RegulBus()
        regul_bus_os = RegulBusOs()

        known_modules = set(regul_bus.dispatch_table.keys()) | set(regul_bus_os.dispatch_table.keys())

        for crate in crates:
            for module in crate:
                module_catalog = module["MODULE_CATALOG"]


                if module_catalog not in known_modules:
                    if module_catalog in RegulBus().dispatch_table:
                        print("Неизвестный для SCADA тип модуля", module_catalog)
                    elif module_catalog in RegulBusOs().dispatch_table:
                        print("Неизвестный для PLC тип модуля", module_catalog)
                    else:
                        print(f"Тип модуля '{module_catalog}' не найден ни в RegulBus, ни в RegulBusOs.")

    def generate_diag_cpu_modules(self, crates):
        """
        Создает текстовый файл DIAG_CPU_MODULES.txt на основе данных из крейтов.

        Args:
            crates (list): Список корзин, полученный из find_crates().
        """
        if self.info_data is None:
            print("Ошибка: info_data не загружена. Сначала вызовите extract_info_data().")
            return

        bus_type = self.info_data['INFO_BUS_TYPE']
        output_dir = "_output/DiagnModules/PLC"
        output_file = os.path.join(output_dir, "DIAG_CPU_MODULES.txt")

        # Создаем директории, если их нет
        os.makedirs(output_dir, exist_ok=True)

        try:
            with open(output_file, "w") as f:
                for crate in crates:
                    for module in crate:
                        module_catalog = module["MODULE_CATALOG"]
                        # Исключаем модуль "R500-PP-00-011 [PS 75W]"
                        if module_catalog == "R500-PP-00-011 [PS 75W]":
                            continue

                        # Выбираем класс RegulBus или RegulBusOs в зависимости от bus_type
                        if bus_type == "Regul_Bus":
                            try:
                                module_string = RegulBus().dispatch_table[module_catalog]
                                f.write(module_string + "\n")
                            except KeyError:
                                print(f"Предупреждение: Модуль '{module_catalog}' не найден в RegulBus.")

                        elif bus_type == "Regul_Bus_OS":
                            try:
                                module_string = RegulBusOs().dispatch_table[module_catalog]
                                f.write(module_string + "\n")
                            except KeyError:
                                print(f"Предупреждение: Модуль '{module_catalog}' не найден в RegulBusOs.")
                        else:
                            print(f"Ошибка: Неизвестный тип шины '{bus_type}'.")
                            return

            print(f"Файл '{output_file}' успешно создан.")

        except Exception as e:
            print(f"Ошибка при записи в файл '{output_file}': {e}")


if __name__ == '__main__':
    # Создаем экземпляр класса DataProcessor
    processor = DataProcessor()

    # Читаем данные из файлов
    try:
        processor.read_data()
    except ValueError as e:
        print(e)
        exit()

    # Извлекаем данные из info_df
    processor.info_data = processor.extract_info_data()  # Сохраняем в атрибут класса
    if processor.info_data:
        print("Извлеченные данные из info_df:", processor.info_data)

    # Находим корзины с устройствами
    crates = processor.find_crates()
    if crates:
        print("\nНайденные крейты:")
        for i, crate in enumerate(crates):
            print(f"Крейт {i + 1}:")
            for module in crate:
                print(f"  {module}")

        # Определяем, является ли система резервированной
        is_redundant = processor.is_redundant_system(crates)
        print("\nЯвляется ли система резервированной:", is_redundant)

        # Проверяем типы модулей
        print("\nПроверка типов модулей:")
        processor.check_module_types(crates)

        # Генерируем DIAG_CPU_MODULES.txt
        processor.generate_diag_cpu_modules(crates)
    else:
        print("Крейты не найдены.")

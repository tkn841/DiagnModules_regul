
import pandas as pd
import os


class PGNAnalyzer:
    def __init__(self, pgn_file, modules_file, plc_templates_dir, scada_templates_dir):
        self.pgn_file = pgn_file
        self.modules_file = modules_file
        self.plc_templates_dir = plc_templates_dir
        self.scada_templates_dir = scada_templates_dir
        self.info_df = None
        self.ascfg_df = None
        self.list_modules = None

    def read_excel_file(self, file_path, sheet_name, header_row):
        """
        Читает XLSX файл и возвращает DataFrame.
        """
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row - 1)
            return df
        except FileNotFoundError:
            print(f"Ошибка: Файл не найден: {file_path}")
            return None
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path} (лист {sheet_name}): {e}")
            return None

    def load_data(self):
        """
        Загружает данные из файлов.
        """
        self.info_df = self.read_excel_file(self.pgn_file, "Info", 2)

        # Переименовываем столбец 1 в "VALUE", если он существует
        if 1 in self.info_df.columns:
            self.info_df = self.info_df.rename(columns={1: 'VALUE'})

        self.ascfg_df = self.read_excel_file(self.pgn_file, "AsCfg", 1)
        self.list_modules = self.read_excel_file(self.modules_file, "Sheet1", 1)

        if any(df is None for df in [self.info_df, self.ascfg_df, self.list_modules]):
            raise ValueError("Не удалось загрузить все необходимые данные.")

    def extract_info_profile(self):
       """
       Извлекает значения из info_df для указанных PROFILE.
       """
       if self.info_df is None:
           print("Ошибка: info_df не загружен. Сначала вызовите load_data().")
           return None

       profile_keys = [
           "INFO_KKS_a1", "INFO_KKS_a2", "INFO_KKS_a3",
           "INFO_DESCRIPTION_a1", "INFO_DESCRIPTION_a2", "INFO_DESCRIPTION_a3", "INFO_BOX_MSKU",
           "INFO_BOX_RIO1", "INFO_BOX_RIO2", "INFO_BOX_RIO3", "INFO_BOX_RIO4",
           "INFO_BOX_RIO5", "INFO_BOX_RIO6", "INFO_BOX_RIO7", "INFO_BOX_RIO8",
           "INFO_BOX_RIO9", "INFO_BOX_RIO10", "INFO_BOX_RIO11", "INFO_BOX_RIO12",
           "INFO_BOX_RIO13", "INFO_BOX_RIO14", "INFO_BOX_RIO15", "INFO_BUS_TYPE"
       ]

       result = {}
       for key in profile_keys:
           try:
               #  Если переименовали столбец
               value = self.info_df.loc[self.info_df['PROFILE'] == key, 'VALUE'].values[0]
               # Если не переименовали столбец
               #value = self.info_df.loc[self.info_df['PROFILE'] == key, 1].values[0]
               result[key] = value
           except KeyError as e:
               print(f"KeyError: Столбец '{e}' не найден в info_df.")
               result[key] = None
           except IndexError:
               print(f"Предупреждение: PROFILE '{key}' не найден в info_df или столбец 'VALUE' не существует.")
               result[key] = None

       return result

    def identify_crates(self):
        """
        Определяет корзины (крейты) на основе данных из ascfg_df и list_modules.
        """
        if self.ascfg_df is None or self.list_modules is None:
            print("Ошибка: ascfg_df или list_modules не загружены. Сначала вызовите load_data().")
            return None

        crates = []
        current_crate = []
        in_crate = False

        start_modules = set(self.list_modules[self.list_modules['TYPE'].str.contains("ST_IN", na=False)]['NAME'].tolist())
        end_modules = set(self.list_modules[self.list_modules['TYPE'].str.contains("ST_OUT", na=False)]['NAME'].tolist())

        for index, row in self.ascfg_df.iterrows():
            module_name = row['MODULE_CATALOG']

            if row['MODULE_CATALOG'] in start_modules and not in_crate:
                in_crate = True
                current_crate.append({
                    'BOX': row['BOX'],
                    'UNIT_POSITION': row['UNIT_POSITION'],
                    'MODULE_CATALOG': row['MODULE_CATALOG']
                })
            elif in_crate:
                 current_crate.append({
                    'BOX': row['BOX'],
                    'UNIT_POSITION': row['UNIT_POSITION'],
                    'MODULE_CATALOG': row['MODULE_CATALOG']
                })
            if row['MODULE_CATALOG'] in end_modules:
                in_crate = False
                crates.append(current_crate)
                current_crate = []

        return crates

    def is_redundant(self, crates):
        """
        Определяет, является ли система резервированной.
        """
        if not crates or len(crates) < 2:
            return False

        crate1 = crates[0]
        crate2 = crates[1]

        if len(crate1) != len(crate2):
            return False

        for i in range(len(crate1)):
            if crate1[i]['MODULE_CATALOG'] != crate2[i]['MODULE_CATALOG']:
                return False

        return True

    def check_module_types(self, crates):
        """
        Проверяет наличие типов модулей в папках _templates/PLC и _templates/SCADA.
        """
        plc_modules = set(os.listdir(self.plc_templates_dir))
        scada_modules = set(os.listdir(self.scada_templates_dir))

        for crate in crates:
            for module in crate:
                module_type = module['MODULE_CATALOG']
                if "[" in module_type:
                    module_type = module_type.split("[")[0].strip()

                if f"{module_type}.xml" not in plc_modules:
                    print(f"Неизвестный для PLC тип модуля {module_type}")
                if f"{module_type}.xml" not in scada_modules:
                    print(f"Неизвестный для SCADA тип модуля {module_type}")

# Пример использования
if __name__ == '__main__':
    # Замените на фактические пути к вашим файлам и папкам
    pgn_file = "_files/PGN.xlsx"
    modules_file = "_files/Список_модулей_Regul.xlsx"
    plc_templates_dir = "_templates/PLC"
    scada_templates_dir = "_templates/SCADA"

    try:
        analyzer = PGNAnalyzer(pgn_file, modules_file, plc_templates_dir, scada_templates_dir)
        analyzer.load_data()

        # Извлечение информации о профиле
        profile_info = analyzer.extract_info_profile()
        if profile_info:
            print("Информация о профиле:")
            for key, value in profile_info.items():
                print(f"{key}: {value}")

        # Определение корзин
        crates = analyzer.identify_crates()
        if crates:
            print("\nКорзины:")
            for i, crate in enumerate(crates):
                print(f"Крейт {i+1}:")
                for module in crate:
                    print(f"  {module}")

            # Определение резервирования
            is_redundant = analyzer.is_redundant(crates)
            print(f"\nСистема резервированная: {is_redundant}")

            # Проверка типов модулей
            print("\nПроверка типов модулей:")
            analyzer.check_module_types(crates)

    except ValueError as e:
        print(f"Ошибка: {e}")

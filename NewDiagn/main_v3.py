import pandas as pd
import os

# Импортируем классы RegulBus и RegulBusOs
from _templates.PLC.Astra1720RegulBus import Astra1720RegulBus
from _templates.PLC.Astra1720RegulBusOS import Astra1720RegulBusOS
from _templates.PLC.EpsilonRegulBusV161xx import EpsilonRegulBusV161xx
from _templates.PLC.EpsilonRegulBusOSV161xx import EpsilonRegulBusOSV161xx
from _templates.SCADA.AlphaHmi import AlphaHmi
class DataProcessor:
    def __init__(self):
        self.info_df = None
        self.ascfg_df = None
        self.list_modules = None
        self.info_data = None  # Добавляем атрибут для хранения info_data

        self.output_dir_plc = "_output\DiagnModules\PLC"
        self.output_dir_scada = "_output\DiagnModules\SCADA"
        self.output_fb_cpu_diagn_modules = os.path.join(self.output_dir_plc, "FB_DIAG_CPU_MODULES.txt")
        self.output_db_cpu_diagn_modules = os.path.join(self.output_dir_plc, "DB_DIAG_CPU_MODULES.txt")
        self.output_crmem_cpu_diagn_modules = os.path.join(self.output_dir_plc, "CrossMem_DIAG_CPU_MODULES.txt")

        self.pathOmobj = '_omobj'
        self.extension = r'.omobj'  # расширение заданных файлов
        self.containNameFile = '_Diagn_Rack_'  # строка которая находится в имени файла

        # Необходимые ключи из вкладки INFO
        self.profile_keys = [
            "INFO_KKS_a1", "INFO_KKS_a2", "INFO_KKS_a3",
            "INFO_DESCRIPTION_a1", "INFO_DESCRIPTION_a2", "INFO_DESCRIPTION_a3", "INFO_BOX_MSKU",
            "INFO_BOX_RIO1", "INFO_BOX_RIO2", "INFO_BOX_RIO3", "INFO_BOX_RIO4",
            "INFO_BOX_RIO5", "INFO_BOX_RIO6", "INFO_BOX_RIO7", "INFO_BOX_RIO8",
            "INFO_BOX_RIO9", "INFO_BOX_RIO10", "INFO_BOX_RIO11", "INFO_BOX_RIO12",
            "INFO_BOX_RIO13", "INFO_BOX_RIO14", "INFO_BOX_RIO15", "INFO_BUS_TYPE", "INFO_RED_TYPE",
            "INFO_DEVELOP"
        ]

        # Экземпляры всех функции для генерации кода PLC
        self.astra1720_regul_bus = Astra1720RegulBus()
        self.astra1720_regul_bus_os = Astra1720RegulBusOS()
        self.epsilon_regul_bus = EpsilonRegulBusV161xx()
        self.epsilon_regul_bus_os = EpsilonRegulBusOSV161xx()
        self.alpha_hmi = AlphaHmi()

        # Тип резервирования, тип среды разработки
        self.type_redundant = None
        self.type_dev = None

        self.creates = None
        self.name_db = 'DIAG_CPU_MODULES'  # имя DB, где хранятся все STATE по всем модулям
        self.is_redundant = False
        self.create_is_redundant = []  # Крейт который является резервным

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

        data_dict = {}
        for key in self.profile_keys:
            try:
                # Используем .loc для доступа к строкам по значению в столбце 'PROFILE'
                row = self.info_df.loc[self.info_df['PROFILE'] == key]

                # Проверяем, что строка найдена, и берем значение из столбца '1'
                if not row.empty:
                    data_dict[key] = row[1].values[0]  # .values[0] чтобы получить значение, а не Series
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
                    "MODULE_CATALOG": row['MODULE_CATALOG'],
                    "MODULE_FW": row['MODULE_FW']
                })
            elif module_name in st_out_modules:
                if in_crate:
                    current_crate.append({
                        "BOX": row['BOX'],
                        "UNIT_POSITION": row['UNIT_POSITION'],
                        "MODULE_CATALOG": row['MODULE_CATALOG'],
                        "MODULE_FW": row['MODULE_FW']
                    })
                    crates.append(current_crate)
                    current_crate = []
                    in_crate = False
            elif in_crate:
                current_crate.append({
                    "BOX": row['BOX'],
                    "UNIT_POSITION": row['UNIT_POSITION'],
                    "MODULE_CATALOG": row['MODULE_CATALOG'],
                    "MODULE_FW": row['MODULE_FW']
                })

        # Если крейт остался открытым в конце, закрываем его
        if current_crate:
            crates.append(current_crate)
        self.creates = crates
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

        dev = self.info_data['INFO_DEVELOP']
        reg_bus = self.info_data['INFO_BUS_TYPE']

        known_modules = (set(self.astra1720_regul_bus.dispatch_table.keys()) |
                         set(self.astra1720_regul_bus_os.dispatch_table.keys()) |
                         set(self.epsilon_regul_bus.dispatch_table.keys()) |
                         set(self.epsilon_regul_bus_os.dispatch_table.keys()) |
                         set(self.alpha_hmi.dispatch_table.keys()))

        for crate in crates:
            for module in crate:
                module_catalog = module["MODULE_CATALOG"]
                if module_catalog not in known_modules:
                    if module_catalog in self.alpha_hmi.dispatch_table:
                        print("Неизвестный для SCADA тип модуля", module_catalog)
                    match self.info_data['INFO_DEVELOP']:
                        case 'Epsilon':
                            if module_catalog in self.epsilon_regul_bus.dispatch_table and reg_bus == 'Regul_Bus':
                                print(f'Неизвестный для Epsilon (Regul_Bus) модуль {module_catalog}')
                            if module_catalog in self.epsilon_regul_bus_os.dispatch_table and reg_bus == 'Regul_Bus_OS':
                                print(f'Неизвестный для Epsilon (Regul_Bus_OS) модуль {module_catalog}')
                        case 'Astra':
                            if module_catalog in self.astra1720_regul_bus.dispatch_table and reg_bus == 'Regul_Bus':
                                print(f'Неизвестный для Astra (Regul_Bus) модуль {module_catalog}')
                            if module_catalog in self.astra1720_regul_bus_os.dispatch_table and reg_bus == 'Regul_Bus_OS':
                                print(f'Неизвестный для Astra (Regul_Bus_OS) модуль {module_catalog}')

    def generate_handle_fb(self, crates):
        """
        Функция создает список тегов для FB_DIAGN_MODULES
        """

        codePLC = list()

        codePLC.append('FUNCTION_BLOCK FB_DIAGNOSTICS_MODULES\n')
        codePLC.append('VAR_INPUT\n')
        codePLC.append('\tT_SAMPLE: TIME;\n')
        codePLC.append('\t// величина задержки\n')
        codePLC.append('\tt_delay: TIME := TIME#1s0ms;\n')
        codePLC.append('END_VAR\n')
        codePLC.append('VAR\n')
        codePLC.append('\t/// Таймер на задержку чтения диагностики\n')
        codePLC.append('\tct_delay: TIME;\n')
        codePLC.append('\ti: INT;\n')
        codePLC.append('\tname: STRING;\n')

        if str(self.info_data['INFO_DEVELOP']).startswith('Epsilon'):
            codePLC.append('\tsi3: sys_info3_t;\n')
        elif str(self.info_data['INFO_DEVELOP']).startswith('Astra'):
            codePLC.append('\tsi4: sys_info4_t;\n')

        if str(self.info_data['INFO_RED_TYPE']).startswith('RED_OS'):
            codePLC.append('\ttAppInfo: PsRedundancy_OS.TAppInfo;\n')
        elif str(self.info_data['INFO_RED_TYPE']).startswith('RED'):
            codePLC.append('\ttAppInfo: PsRedundancy.TAppInfo;\n')

        codePLC.append('\tSYSTIME: RTS_SYSTIMEDATE;\n')
        codePLC.append('\tError_CODE: DWORD;\n')
        codePLC.append('\tPLC_TIME: DWORD;\n')
        codePLC.append('\tPLC_LEFT_MASTER: BOOL;\n')
        codePLC.append('\tPLC_LEFT_SLAVE: BOOL;\n')
        codePLC.append('\tPLC_RIGHT_MASTER: BOOL;\n')
        codePLC.append('\tPLC_RIGHT_SLAVE: BOOL;\n')
        codePLC.append('\tSTR_LWORD: TYPE_LWORD;\n\n')

        setModules = set()
        for jndex, crate in enumerate(crates):
            # Проходим резервный крейт
            if self.is_redundant and jndex == 1:
                continue
            for index, module in enumerate(crate):
                if module["MODULE_CATALOG"] != 'R500-PP-00-011 [PS 75W]' and module["MODULE_CATALOG"] != 'R500-PP-00-021 [PS 75W]':
                    # Создание тегов HeartBeat_Old
                    codePLC.append(f'\t{module["BOX"]}_{module["UNIT_POSITION"]}_HeartBeat_old: UINT;\n')

                    # создание тегов PsIoDrvRegulBus_OS.TR500
                    # создаем только для RegulBusOS и Astra
                    if (str(self.info_data['INFO_BUS_TYPE']).startswith('Regul_Bus_OS') and
                        str(self.info_data['INFO_DEVELOP']).startswith('Astra')):

                        if 'nan' in str(module["MODULE_FW"]):
                            continue
                        # Определяем версию PdoSdo
                        pdo_sdo = str(module["MODULE_FW"])[5:7]
                        if pdo_sdo.startswith('0'):
                            pdo_sdo = pdo_sdo.replace('0', '')

                        str_module = str(module["MODULE_CATALOG"])[str(module["MODULE_CATALOG"]).find('-'):str(module["MODULE_CATALOG"]).find(' ')].replace('-', '')
                        if ('-AI-' in str(module["MODULE_CATALOG"]) or
                            '-AO-' in str(module["MODULE_CATALOG"])):
                            setModules.add(f'\t{str_module}_{pdo_sdo}_IN: PsIoDrvRegulBus_OS.TR500_{str_module}_Inputs_v{pdo_sdo};\n')
                        if ('-DI-' in str(module["MODULE_CATALOG"]) or
                            '-DO-' in str(module["MODULE_CATALOG"]) or
                            '-DA-' in str(module["MODULE_CATALOG"]) or
                            '-DS-' in str(module["MODULE_CATALOG"])):
                            setModules.add(f'\t{str_module}_{pdo_sdo}_IN: PsIoDrvRegulBus_OS.TR500_{str_module}_Inputs_v{pdo_sdo};\n')
                            setModules.add(f'\t{str_module}_{pdo_sdo}_IN: PsIoDrvRegulBus_OS.TR500_{str_module}_Outputs_v{pdo_sdo};\n')
        codePLC.extend(setModules)
        codePLC.append('END_VAR\n\n\n\n')
        match self.info_data['INFO_DEVELOP']:
            case 'Epsilon':
                codePLC.append('GetSysInfo3(si3);\n')
                if self.info_data['INFO_RED_TYPE'] == 'RED':
                    codePLC.append('PsRedundancy.GetAppInfo(appInfo := tAppInfo);\n')
                if self.info_data['INFO_RED_TYPE'] == 'RED_OS':
                    codePLC.append('PsRedundancy_OS.GetAppInfo(appInfo := tAppInfo);\n')

                codePLC.append('// работа таймера задержки\n')
                codePLC.append('IF ct_delay >= T_SAMPLE THEN\n')
                codePLC.append('\tct_delay := ct_delay - T_SAMPLE;\n')
                codePLC.append('END_IF\n\n')

                codePLC.append('// таймер досчитал до нуля\n')
                codePLC.append('IF ct_delay < T_SAMPLE THEN\n')
                codePLC.append('\tct_delay := t_delay;	// присвоить время задержки\n\n\n')
            case 'Astra':
                codePLC.append('PsPlcInfoGetSysInfo4(si4);\n')
                if self.info_data['INFO_RED_TYPE'] == 'RED':
                    codePLC.append('PsRedundancy.GetAppInfo(tAppInfo);\n')
                if self.info_data['INFO_RED_TYPE'] == 'RED_OS':
                    codePLC.append('PsRedundancy_OS.GetAppInfo(tAppInfo);\n')

                codePLC.append('// работа таймера задержки\n')
                codePLC.append('IF ct_delay >= T_SAMPLE THEN\n')
                codePLC.append('\tct_delay := ct_delay - T_SAMPLE;\n')
                codePLC.append('END_IF\n\n')

                codePLC.append('// таймер досчитал до нуля\n')
                codePLC.append('IF ct_delay < T_SAMPLE THEN\n')
                codePLC.append('\tct_delay := t_delay;	// присвоить время задержки\n\n')
        return codePLC

    def generate_diag_cpu_modules(self, crates):
        """
        Создает текстовый файл DIAG_CPU_MODULES.txt на основе данных из крейтов.

        Args:
            crates (list): Список корзин, полученный из find_crates().
        """
        if self.info_data is None:
            print("Ошибка: info_data не загружена. Сначала вызовите extract_info_data().")
            return

        try:
            txt = []
            txt.extend(self.generate_handle_fb(crates))
            for jndex, crate in enumerate(crates):
                # Проходим резервный крейт
                if self.is_redundant and jndex == 1:
                    continue
                for index, module in enumerate(crate):
                    module_catalog = module["MODULE_CATALOG"]

                    # Исключаем модуль "R500-PP-00-011 [PS 75W]"
                    if module_catalog == "R500-PP-00-011 [PS 75W]":
                        continue

                    match self.info_data['INFO_DEVELOP']:
                        case 'Epsilon':
                            if self.info_data['INFO_BUS_TYPE'] == 'Regul_Bus':
                                try:
                                    self.epsilon_regul_bus.box = module["BOX"]
                                    self.epsilon_regul_bus.unit_pos = module["UNIT_POSITION"]
                                    self.epsilon_regul_bus.modul = module["MODULE_CATALOG"]
                                    self.epsilon_regul_bus.name_db = self.name_db
                                    self.epsilon_regul_bus.systemRes = self.is_redundant
                                    self.epsilon_regul_bus.racks = crates
                                    self.epsilon_regul_bus.crateRes = self.is_redundant and jndex == 0

                                    if self.is_redundant and jndex == 0:
                                        self.epsilon_regul_bus.unit_pos_res = f'{self.create_is_redundant[index]["UNIT_POSITION"]}'

                                    pdo_sdo = str(module["MODULE_FW"])[5:7]
                                    if pdo_sdo.startswith('0'):
                                        pdo_sdo = pdo_sdo.replace('0', '')
                                    self.epsilon_regul_bus.verPdoSdo = pdo_sdo

                                    module_string = self.epsilon_regul_bus.dispatch_table[module_catalog]
                                    txt.extend(module_string())
                                except KeyError:
                                    print(f"Предупреждение: Модуль '{module_catalog}' не найден в RegulBus.")

                            elif self.info_data['INFO_BUS_TYPE'] == 'Regul_Bus_OS':
                                try:
                                    self.epsilon_regul_bus_os.box = module["BOX"]
                                    self.epsilon_regul_bus_os.unit_pos = module["UNIT_POSITION"]
                                    self.epsilon_regul_bus_os.modul = module["MODULE_CATALOG"]
                                    self.epsilon_regul_bus_os.name_db = self.name_db
                                    self.epsilon_regul_bus_os.systemRes = self.is_redundant
                                    self.epsilon_regul_bus_os.racks = crates
                                    self.epsilon_regul_bus_os.crateRes = self.is_redundant and jndex == 0

                                    if self.is_redundant and jndex == 0:
                                        self.epsilon_regul_bus_os.unit_pos_res = f'{self.create_is_redundant[index]["UNIT_POSITION"]}'

                                    pdo_sdo = str(module["MODULE_FW"])[5:7]
                                    if pdo_sdo.startswith('0'):
                                        pdo_sdo = pdo_sdo.replace('0', '')
                                    self.epsilon_regul_bus_os.verPdoSdo = pdo_sdo

                                    module_string = self.epsilon_regul_bus_os.dispatch_table[module_catalog]
                                    txt.extend(module_string())
                                except KeyError:
                                    print(f"Предупреждение: Модуль '{module_catalog}' не найден в RegulBus.")

                        case 'Astra':
                            if self.info_data['INFO_BUS_TYPE'] == 'Regul_Bus':
                                try:
                                    self.astra1720_regul_bus.box = module["BOX"]
                                    self.astra1720_regul_bus.unit_pos = module["UNIT_POSITION"]
                                    self.astra1720_regul_bus.modul = module["MODULE_CATALOG"]
                                    self.astra1720_regul_bus.name_db = self.name_db
                                    self.astra1720_regul_bus.systemRes = self.is_redundant
                                    self.astra1720_regul_bus.racks = crates
                                    self.astra1720_regul_bus.crateRes = self.is_redundant and jndex == 0

                                    if self.is_redundant and jndex == 0:
                                        self.astra1720_regul_bus.unit_pos_res = f'{self.create_is_redundant[index]["UNIT_POSITION"]}'

                                    pdo_sdo = str(module["MODULE_FW"])[5:7]
                                    if pdo_sdo.startswith('0'):
                                        pdo_sdo = pdo_sdo.replace('0', '')
                                    self.astra1720_regul_bus.verPdoSdo = pdo_sdo

                                    module_string = self.astra1720_regul_bus.dispatch_table[module_catalog]
                                    txt.extend(module_string())
                                except KeyError:
                                    print(f"Предупреждение: Модуль '{module_catalog}' не найден в RegulBus.")

                            elif self.info_data['INFO_BUS_TYPE'] == 'Regul_Bus_OS':
                                try:
                                    self.astra1720_regul_bus_os.box = module["BOX"]
                                    self.astra1720_regul_bus_os.unit_pos = module["UNIT_POSITION"]
                                    self.astra1720_regul_bus_os.modul = module["MODULE_CATALOG"]
                                    self.astra1720_regul_bus_os.name_db = self.name_db
                                    self.astra1720_regul_bus_os.systemRes = self.is_redundant
                                    self.astra1720_regul_bus_os.racks = crates
                                    self.astra1720_regul_bus_os.crateRes = self.is_redundant and jndex == 0

                                    if self.is_redundant and jndex == 0:
                                        self.astra1720_regul_bus_os.unit_pos_res = f'{self.create_is_redundant[index]["UNIT_POSITION"]}'

                                    pdo_sdo = str(module["MODULE_FW"])[5:7]
                                    if pdo_sdo.startswith('0'):
                                        pdo_sdo = pdo_sdo.replace('0', '')
                                    self.astra1720_regul_bus_os.verPdoSdo = pdo_sdo

                                    module_string = self.astra1720_regul_bus_os.dispatch_table[module_catalog]
                                    txt.extend(module_string())
                                except KeyError:
                                    print(f"Предупреждение: Модуль '{module_catalog}' не найден в RegulBus.")
                        case _:
                            pass

            # вывод данных по всем блокам питания
            match self.info_data['INFO_DEVELOP']:
                case 'Epsilon':
                    if self.info_data['INFO_BUS_TYPE'] == 'Regul_Bus':
                        module_string = self.epsilon_regul_bus.dispatch_table['R500-PP-00-011 [PS 75W]']
                        txt.extend(module_string())
                    elif self.info_data['INFO_BUS_TYPE'] == 'Regul_Bus_OS':
                        module_string = self.epsilon_regul_bus_os.dispatch_table['R500-PP-00-011 [PS 75W]']
                        txt.extend(module_string())
                case 'Astra':
                    if self.info_data['INFO_BUS_TYPE'] == 'Regul_Bus':
                        module_string = self.astra1720_regul_bus.dispatch_table['R500-PP-00-011 [PS 75W]']
                        txt.extend(module_string())
                    elif self.info_data['INFO_BUS_TYPE'] == 'Regul_Bus_OS':
                        module_string = self.astra1720_regul_bus_os.dispatch_table['R500-PP-00-011 [PS 75W]']
                        txt.extend(module_string())

            txt.append('END_IF')

            with open(self.output_fb_cpu_diagn_modules, 'w') as f:
                f.write(''.join(txt))
                f.close()
                print(f"Файл '{self.output_fb_cpu_diagn_modules}' успешно создан.")

        except Exception as e:
            print(f"Ошибка при записи в файл '{self.output_fb_cpu_diagn_modules}': {e}")

    def generate_global_DB(self, crates):
        codeGlobal = list()  # список для глобальных переменных
        codeGlobal.append('VAR_GLOBAL\n')

        for jndex, crate in enumerate(crates):
            for index, module in enumerate(crate):
                module_catalog = module["MODULE_CATALOG"]

                # Исключаем модуль "R500-PP-00-011 [PS 75W]"
                if module_catalog == "R500-PP-00-011 [PS 75W]":
                    continue
                if self.is_redundant and jndex == 0:
                    if ('-AI-' in str(module["MODULE_CATALOG"]) or
                        '-AO-' in str(module["MODULE_CATALOG"]) or
                        '-ST-' in str(module["MODULE_CATALOG"]) or
                        '-DI-' in str(module["MODULE_CATALOG"]) or
                        '-DO-' in str(module["MODULE_CATALOG"]) or
                        '-DA-' in str(module["MODULE_CATALOG"]) or
                        '-CP-' in str(module["MODULE_CATALOG"])):
                        codeGlobal.append(f"\t{module['BOX']}_{module['UNIT_POSITION']}_LOCAL: LWORD;\n")
                        codeGlobal.append(f"\t{module['BOX']}_{module['UNIT_POSITION']}_REMOTE: LWORD;\n")
                    # для данного модуля особое отношение
                    elif 'R500-DO-32-041 [SM 32DO DC24V]' in str(module["MODULE_CATALOG"]):
                        codeGlobal.append(f"\t{module['BOX']}_{module['UNIT_POSITION']}_LOCAL2: LWORD;\n")
                        codeGlobal.append(f"\t{module['BOX']}_{module['UNIT_POSITION']}_REMOTE2: LWORD;\n")
                        codeGlobal.append(f"\t{module['BOX']}_{module['UNIT_POSITION']}_LOCAL3: LWORD;\n")
                        codeGlobal.append(f"\t{module['BOX']}_{module['UNIT_POSITION']}_REMOTE3: LWORD;\n")
                        codeGlobal.append(f"\t{module['BOX']}_{module['UNIT_POSITION']}_STATE2: LWORD; // Передаем на SCADA\n")
                        codeGlobal.append(f"\t{module['BOX']}_{module['UNIT_POSITION']}_STATE3: LWORD; // Передаем на SCADA\n")

                if '-CU-' in str(module["MODULE_CATALOG"]):
                    if self.is_redundant and jndex == 0:
                        codeGlobal.append(f"\t{module['BOX']}_{module['UNIT_POSITION']}_LOCAL: STRUCT_STATUS_PLC;\n")
                        codeGlobal.append(f"\t{module['BOX']}_{module['UNIT_POSITION']}_REMOTE: STRUCT_STATUS_PLC;\n")
                    codeGlobal.append(f"\t{module['BOX']}_{module['UNIT_POSITION']}_STATE: STRUCT_STATUS_PLC; // Передаем на SCADA\n")
                else:
                    codeGlobal.append(f"\t{module['BOX']}_{module['UNIT_POSITION']}_STATE: LWORD; // Передаем на SCADA\n")

        # переменные для блоков питания
        if self.is_redundant:
            codeGlobal.append('\tPS_LOCAL: LWORD;\n')
            codeGlobal.append('\tPS_REMOTE: LWORD;\n')
        codeGlobal.append('\tPS_STATE: LWORD; // Передаем на SCADA\n')

        # переменные ErrorRACK
        if self.is_redundant:
            codeGlobal.append('\tErrorRACK_LOCAL: LWORD;\n')
            codeGlobal.append('\tErrorRACK_REMOTE: LWORD;\n')
        codeGlobal.append('\tErrorRACK: LWORD; // Передаем на SCADA\n')
        codeGlobal.append('END_VAR')

        with open(self.output_db_cpu_diagn_modules, 'w') as globalDb_txt:
            globalDb_txt.write(''.join(codeGlobal))
            globalDb_txt.close()

    def generate_crosMem(self, crates):
        if self.info_data['INFO_RED_TYPE'] == 'RED_OS':
            return

        codeCrossMemory = list()  # список для CrossMemory
        codeCrossMemory.append('// Cross Memory PLC\n')
        for jndex, crate in enumerate(crates):
            for index, module in enumerate(crate):
                module_catalog = module["MODULE_CATALOG"]

                # Исключаем модуль "R500-PP-00-011 [PS 75W]"
                if module_catalog == "R500-PP-00-011 [PS 75W]":
                    continue
                if self.is_redundant and jndex == 0:
                    if ('-AI-' in str(module["MODULE_CATALOG"]) or
                        '-AO-' in str(module["MODULE_CATALOG"]) or
                        '-ST-' in str(module["MODULE_CATALOG"]) or
                        '-DI-' in str(module["MODULE_CATALOG"]) or
                        '-DO-' in str(module["MODULE_CATALOG"]) or
                        '-DA-' in str(module["MODULE_CATALOG"]) or
                        '-CP-' in str(module["MODULE_CATALOG"]) or
                        '-CU-' in str(module["MODULE_CATALOG"])):
                        codeCrossMemory.append(f"shStatuS_{module['BOX']}_{module['UNIT_POSITION']}: PsRedundancy.CrossMemory(SIZEOF({self.name_db}.{module['BOX']}_{module['UNIT_POSITION']}_LOCAL), ADR({self.name_db}.{module['BOX']}_{module['UNIT_POSITION']}_LOCAL), ADR({self.name_db}.{module['BOX']}_{module['UNIT_POSITION']}_REMOTE));\n")
                    # для данного модуля особое отношение
                    elif 'R500-DO-32-041 [SM 32DO DC24V]' in str(module["MODULE_CATALOG"]):
                        codeCrossMemory.append(f"shStatuS_{module['BOX']}_{module['UNIT_POSITION']}: PsRedundancy.CrossMemory(SIZEOF({self.name_db}.{module['BOX']}_{module['UNIT_POSITION']}_LOCAL), ADR({self.name_db}.{module['BOX']}_{module['UNIT_POSITION']}_LOCAL), ADR({self.name_db}.{module['BOX']}_{module['UNIT_POSITION']}_REMOTE));\n")
                        codeCrossMemory.append(f"shStatuS_{module['BOX']}_{module['UNIT_POSITION']}: PsRedundancy.CrossMemory(SIZEOF({self.name_db}.{module['BOX']}_{module['UNIT_POSITION']}_LOCAL2), ADR({self.name_db}.{module['BOX']}_{module['UNIT_POSITION']}_LOCAL2), ADR({self.name_db}.{module['BOX']}_{module['UNIT_POSITION']}_REMOTE2));\n")
                        codeCrossMemory.append(f"shStatuS_{module['BOX']}_{module['UNIT_POSITION']}: PsRedundancy.CrossMemory(SIZEOF({self.name_db}.{module['BOX']}_{module['UNIT_POSITION']}_LOCAL3), ADR({self.name_db}.{module['BOX']}_{module['UNIT_POSITION']}_LOCAL3), ADR({self.name_db}.{module['BOX']}_{module['UNIT_POSITION']}_REMOTE3));\n")

        codeCrossMemory.append('shStatuS_PS_STATE: PsRedundancy.CrossMemory(SIZEOF(DIAG_CPU_MODULES.PS_LOCAL), ADR(DIAG_CPU_MODULES.PS_LOCAL), ADR(DIAG_CPU_MODULES.PS_REMOTE));\n')
        codeCrossMemory.append('shStatuS_ErrorRACK: PsRedundancy.CrossMemory(SIZEOF(DIAG_CPU_MODULES.ErrorRACK_LOCAL), ADR(DIAG_CPU_MODULES.ErrorRACK_LOCAL), ADR(DIAG_CPU_MODULES.ErrorRACK_REMOTE));\n')
        with open(self.output_crmem_cpu_diagn_modules, 'w', encoding='utf16') as crossMemorytxt:
            crossMemorytxt.write(''.join(codeCrossMemory))
            crossMemorytxt.close()

    # функция определения uuid и имени существующих экранов
    def defineUUID(self):
        """
            Функция находит все файлы в указанной директории по правилам:
            1. заканчивается на ".omobj"
            2. содержит в своем названии "_Diagn_Rack_" или "GlobalDiagn_"

            Забираем только номера uuid для необходимых объектов
            Содаем файл .txt с именем файла и номером uuid
        """
        fileNameList = list()
        uuidList = list()
        nameList = list()
        # проверка существование папки
        if not os.path.exists(self.pathOmobj):
            os.mkdir(self.pathOmobj)
        # читаем каждый файл в указанной директории
        for filename in os.listdir(self.pathOmobj):
            # фильтр на файлы
            if filename.endswith(self.extension) and (self.containNameFile in filename)):
                file_path = os.path.join(self.pathOmobj, filename)
                print(file_path)
                with open(file_path, 'r') as file:
                    # парсинг xml и выделение uuid
                    parser = ET.XMLParser(strip_cdata=False)
                    tree = ET.parse(file, parser)
                    root_node = tree.getroot()

                    # собираем списки
                    fileNameList.append(filename)
                    uuidList.append(root_node.attrib['uuid'])
                    nameList.append(root_node.attrib['name'])
        # заполняем DataFrame
        # в этом ссаном питоне эти датафреймы создавать просто дичь
        data = {'fileName': fileNameList,
                'uuid': uuidList,
                'name': nameList}
        df = pd.DataFrame(data)
        self.uuid = df.copy()
        # запись в файл
        df.to_csv(self.pathOutputFolder + r'\uuid.csv', sep=';', index=True)

    def generate_uuid(self, curObject):
        self.newUuid = False
        for indx in range(0, self.uuid['fileName'].__len__(), 1):
            fileName = str(self.uuid['fileName'].iloc[indx])
            if fileName.startswith(curObject):
                uuidStr = self.uuid['uuid'].values[indx]
                name = self.uuid['name'].values[indx]
                self.newUuid = True
                return uuidStr, name
        # если не нашли нужный экран
        uuidUniq = False
        while (not uuidUniq):
            uuidNew = str(uuid.uuid4())
            if self.uuid['uuid'].__len__() == 0:
                uuidUniq = True
            for indx in range(0, self.uuid['uuid'].__len__(), 1):
                uuidFile = str(self.uuid['uuid'].iloc[indx])
                uuidUniq = False if uuidNew == uuidFile else True # если uuid уникальный, то заканчиваем цикл While
        return uuidNew, curObject

if __name__ == '__main__':
    # 1. Создаем экземпляр класса DataProcessor
    processor = DataProcessor()

    # 2. Читаем данные из файлов
    try:
        processor.read_data()
    except ValueError as e:
        print(e)
        exit()

    # 3. Извлекаем данные из info_df
    processor.info_data = processor.extract_info_data()  # Сохраняем в атрибут класса
    if processor.info_data:
        print("Извлеченные данные из info_df:", processor.info_data)

    # 4. Определяем "Тип шины в ОС контроллера", "Тип резервирования", "Среду разработки"

    # 5. Находим корзины с устройствами
    crates = processor.find_crates()
    if crates:
        print("\nНайденные крейты:")
        for i, crate in enumerate(crates):
            print(f"Крейт {i + 1}:")
            for module in crate:
                print(f"  {module}")

        # 6. Определяем, является ли система резервированной
        is_redundant = processor.is_redundant_system(crates)
        # Если система является резервной, то сразуопредедляем его резервный крейт
        if is_redundant:
            processor.create_is_redundant = crates[1]
        processor.is_redundant = is_redundant
        print("\nЯвляется ли система резервированной:", is_redundant)

        # 7. Проверяем типы модулей
        print("\nПроверка типов модулей:")
        processor.check_module_types(crates)

        # 8. Создаем директории, если их нет
        os.makedirs(processor.output_dir_plc, exist_ok=True)
        os.makedirs(processor.output_dir_scada, exist_ok=True)

        # 9. Генерация для PLC
        processor.generate_crosMem(crates)
        processor.generate_global_DB(crates)
        processor.generate_diag_cpu_modules(crates)

        #Генерация для SCADA

    else:
        print("Крейты не найдены.")

class Astra1720RegulBusOS:
    def __init__(self):
        # словарь с типами модулей с их функциями
        self.dispatch_table = {'R500-ST-02-012': self.st_02_012,
                               'R500-ST-02-022': self.st_02_012,

                               'R500-CU-00-051 [CPU R500]': self.cpu,
                               'R500-CU-00-061 [CPU R500]': self.cpu,
                               'R500-CU-00-161 [CPU R500]': self.cpu,

                               'R500-PP-00-011 [PS 75W]': self.ps,

                               'R500-AI-08-021 [SM 8AI I]': self.ai_08_021,
                               'R500-AI-08-041 [SM 8AI I]': self.ai_08_021,
                               'R500-AI-08-051 [SM 8AI I]': self.ai_08_021,

                               'R500-AI-08-022 [SM 8AI I]': self.ai_08_022,
                               'R500-AI-08-042 [SM 8AI I]': self.ai_08_022,
                               'R500-AI-08-052 [SM 8AI I]': self.ai_08_022,
                               'R500-AI-08-242 [SM 8AI I]': self.ai_08_022,

                               'R500-AI-08-142 [SM 8AI I]': self.ai_08_142,
                               'R500-AI-08-342 [SM 8AI I]': self.ai_08_142,

                               'R500-AI-08-031 [SM 8AI RTD/TC]': self.ai_08_031,
                               'R500-AI-08-131 [SM 8AI RTD/TC]': self.ai_08_031,

                               'R500-AI-16-011 [SM 16AI I]': self.ai_16_011,
                               'R500-AI-16-081 [SM 16AI I]': self.ai_16_011,

                               'R500-AI-16-012 [SM 16AI I]': self.ai_16_012,

                               'R500-AO-08-011 [SM 8AO I]': self.ao_08_011,
                               'R500-AO-08-021 [SM 8AO I]': self.ao_08_011,
                               'R500-AO-08-031 [SM 8AO I]': self.ao_08_011,

                               'R500-AS-08-011 [SM 8AI I]': self.as_08_011,

                               'R500-DI-16-021 [SM 16DI AC220V]': self.di_16_021,

                               'R500-DI-16-032 [SM 16DI AC220V]': self.di_16_032,

                               'R500-DI-32-011 [SM 32DI DC24V]': self.di_32_011,
                               'R500-DI-32-012 [SM 32DI DC24V]': self.di_32_011,
                               'R500-DI-32-013 [SM 32DI DC24V]': self.di_32_011,
                               'R500-DI-32-111 [SM 32DI DC24V]': self.di_32_011,

                               'R500-DO-16-021 [SM 16DO AC220V]': self.do_16_021,

                               'R500-DO-32-011 [SM 32DO DC24V]': self.do_32_011,

                               'R500-DO-32-012 [SM 32DO DC24V]': self.do_32_012,
                               'R500-DO-32-013 [SM 32DO DC24V]': self.do_32_012,

                               'R500-DO-32-041 [SM 32DO DC24V]': self.do_32_041,

                               'R500-DS-32-011 [SM 24DI 8DO DC24V]': self.ds_32_011,

                               'R500-DS-32-012 [SM 24DI 8DO DC24V]': self.ds_32_012,

                               'R500-CP-02-021': self.cp_02_021,

                               'R500-CP-04-011 [4 RS485]': self.cp_04_011,

                               'R500-CP-06-111 [6 ETHERNET]': self.cp_06_111,

                               'R500-DA-03-011 [SM 3FI 1FO 6DI 6DO] ENC': self.da_03_011}
        self.box = ''
        self.unit_pos = ''
        self.modul = ''
        self.crateRes = ''
        self.name_db = ''
        self.unit_pos_res = ''
        self.systemRes = ''
        self.racks = []
        self.verPdoSdo = ''

    def part_start(self):
        codePLC = list()
        codePLC.append('PsPlcInfoGetSysInfo4(si4);\n')
        codePLC.append('PsRedundancy_OS.GetAppInfo(tAppInfo);\n\n')

        codePLC.append('// работа таймера задержки\n')
        codePLC.append('IF ct_delay >= T_SAMPLE THEN\n')
        codePLC.append('\tct_delay := ct_delay - T_SAMPLE;\n')
        codePLC.append('END_IF\n\n')

        codePLC.append('// таймер досчитал до нуля\n')
        codePLC.append('IF ct_delay < T_SAMPLE THEN\n')
        codePLC.append('\tct_delay := t_delay;	// присвоить время задержки\n')

        codePLC.append('\t// Определение ведующего и ведомого ПЛК (задержка на t_delay)\n')
        codePLC.append('\tPLC_LEFT_MASTER := MSKU_1A2_STATE.STATE.10;\n')
        codePLC.append('\tPLC_LEFT_SLAVE := MSKU_1A2_STATE.STATE.8;\n')

        codePLC.append('\tPLC_RIGHT_MASTER := MSKU_2A2_STATE.STATE.10;\n')
        codePLC.append('\tPLC_RIGHT_SLAVE := MSKU_2A2_STATE.STATE.8;)\n\n\n')

        return codePLC

    def part_end(self):
        codePLC = list()
        codePLC.append('END_IF')

        return codePLC

    def st_02_012(self):
        """
        функция генерации кода для
        R500-ST-02-012
        R500-ST-02-022
        :return: codePLC = list()
        """
        codePLC = list()

        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n')
        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0;\n\n')

        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}.PortLink;	// Модуль в работе\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}.PortLink;	// Модуль установлен в слоте \n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\t\tSTR_LWORD._LWORD.BIT_03 := {self.box}_{self.unit_pos}.PortLink AND PLC_LEFT_MASTER; // Наличие линка на B1 (зеленый)\n')
                codePLC.append(
                    f'\t\tSTR_LWORD._LWORD.BIT_04 := {self.box}_{self.unit_pos}.PortLink AND PLC_LEFT_SLAVE; // Наличие линка на B1 (желтый)\n')
                codePLC.append(
                    f'\t\tSTR_LWORD._LWORD.BIT_05 := FALSE; // {self.box}_{self.unit_pos}.PortLink AND PLC_RIGHT_MASTER; // Наличие линка на B2 (зеленый)\n')
                codePLC.append(
                    f'\t\tSTR_LWORD._LWORD.BIT_06 := FALSE; // {self.box}_{self.unit_pos}.PortLink AND PLC_RIGHT_SLAVE; // Наличие линка на B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(
                    f'\t\tSTR_LWORD._LWORD.BIT_03 := FALSE; // {self.box}_{self.unit_pos}.PortLink AND PLC_LEFT_MASTER; // Наличие линка на B1 (зеленый)\n')
                codePLC.append(
                    f'\t\tSTR_LWORD._LWORD.BIT_04 := FALSE; // {self.box}_{self.unit_pos}.PortLink AND PLC_LEFT_SLAVE; // Наличие линка на B1 (желтый)\n')
                codePLC.append(
                    f'\t\tSTR_LWORD._LWORD.BIT_05 := {self.box}_{self.unit_pos}.PortLink AND PLC_RIGHT_MASTER; // Наличие линка на B2 (зеленый)\n')
                codePLC.append(
                    f'\t\tSTR_LWORD._LWORD.BIT_06 := {self.box}_{self.unit_pos}.PortLink AND PLC_RIGHT_SLAVE; // Наличие линка на B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := {self.box}_{self.unit_pos}.PortLink AND PLC_LEFT_MASTER; // Наличие линка на B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := {self.box}_{self.unit_pos}.PortLink AND PLC_LEFT_SLAVE; // Наличие линка на B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := {self.box}_{self.unit_pos}.PortLink AND PLC_RIGHT_MASTER; // Наличие линка на B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := {self.box}_{self.unit_pos}.PortLink AND PLC_RIGHT_SLAVE; // Наличие линка на B2 (желтый)\n\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := {self.box}_{self.unit_pos}.PortLink; // Наличие линка на B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // Наличие линка на B1 (желтый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_05 := {self.box}_{self.unit_pos}.PortLink; // Наличие линка на B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // Наличие линка на B2 (желтый)\n\n')

        if self.crateRes:
            codePLC.append(
                f'\t{self.name_db}.{self.box}_{self.unit_pos}_LOCAL := STR_LWORD.LWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def cpu(self):
        """
        функция генерации кода для
        R500-CU-00-061
        R500-CU-00-051
        :return: codePLC = list()
        """
        codePLC = list()

        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0; \n\n')

        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_00 := GLOBAL.STATUS_PLC > 0;	// Модуль в работе\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError OR Regul_Bus_OS.HwError; // Светодиод HF (красный цвет)\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_02 := GLOBAL.STATUS_PLC = -3; // Резервироание. Ошибка соединения\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := GLOBAL.STATUS_PLC = -2; // Резервироание. Критическая ошибка\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := GLOBAL.STATUS_PLC = -1; // Резервироание. В ошибке\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := GLOBAL.STATUS_PLC = 0; // Резервироание. Выключено\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := GLOBAL.STATUS_PLC = 1; // Резервироание. Инициализация\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_07 := GLOBAL.STATUS_PLC = 2; // Резервироание. Синхронизация\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_08 := GLOBAL.STATUS_PLC = 3; // Резервироание. Ведомый\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_09 := GLOBAL.STATUS_PLC = 4; // Резервироание. Автономный\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_10 := GLOBAL.STATUS_PLC = 5; // Резервироание. Активный\n')
        codePLC.append(f'\tFOR i := 0 TO 5 DO\n')
        codePLC.append(f'\t\tname := si4.net_itf_info[i].name;\n')
        codePLC.append("\t\tIF name = 'port30' THEN\n")
        codePLC.append(f'\t\t\tSTR_LWORD._LWORD.BIT_11 := si4.net_itf_info[i].link; // Наличие линка (порт 3)\n')
        codePLC.append("\t\tELSIF name = 'port40' THEN\n")
        codePLC.append(f'\t\t\tSTR_LWORD._LWORD.BIT_12 := si4.net_itf_info[i].link; // Наличие линка (порт 4)\n')
        codePLC.append("\t\tELSIF name = 'port50' THEN\n")
        codePLC.append(f'\t\t\tSTR_LWORD._LWORD.BIT_13 := si4.net_itf_info[i].link; // Наличие линка (порт 5)\n')
        codePLC.append("\t\tELSIF name = 'port60' THEN\n")
        codePLC.append(f'\t\t\tSTR_LWORD._LWORD.BIT_14 := si4.net_itf_info[i].link; // Наличие линка (порт 6)\n')
        codePLC.append(f'\t\tEND_IF\n')
        codePLC.append(f'\tEND_FOR\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_15 := (PSLed.PsLedGetRun() = 1); // Положение переключателя RUN/STOP (0 - STOP, 1 - RUN)\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_16 := (PSLed.PsLedGetKeyAutoStartApp() = 1); // Положение переключателя KEY (положение 1)\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_17 := (PSLed.PsLedGetKeyAutoStartApp() = 2); // Положение переключателя KEY (положение 2)\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_18 := (PSLed.PsLedGetMBSPosition() = 1); // Положение переключателя MBS (положение 1)\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_19 := (PSLed.PsLedGetMBSPosition() = 2); // Положение переключателя MBS (положение 2)\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_20 := GLOBAL.IsStateActive;\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_21 := GLOBAL.IsDefaultPlc;\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_22 := ({self.name_db}.{self.box}_{self.unit_pos}_STATE.DataCuid = {self.name_db}.{self.box}_{self.unit_pos_res}_STATE.DataCuid) AND ({self.name_db}.{self.box}_{self.unit_pos}_STATE.CodeCuid = {self.name_db}.{self.box}_{self.unit_pos_res}_STATE.CodeCuid); // Синхронизации ПЛК (ВНИМАНИЕ ЗАПАЗДЫВАНИЕ 1 ТАКТ)\n\n')

        # Если система резервированная
        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_LOCAL.STATE := STR_LWORD.LWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Загрузка ядер ПЛК\n')
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_LOCAL.LOAD_CORE_1 := UDINT_TO_REAL(si4.cpu_load[0])/10.0;\n')
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_LOCAL.LOAD_CORE_2 := UDINT_TO_REAL(si4.cpu_load[1])/10.0;\n')
            # codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL.LOAD_CORE_3 := UDINT_TO_REAL(si4.cpu_load[2])/10.0;\n')
            # codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL.LOAD_CORE_4 := UDINT_TO_REAL(si4.cpu_load[3])/10.0;\n\n')

            codePLC.append(f'\t// Время последнего изменения ПО контроллера\n')
            codePLC.append(
                f'\t{self.name_db}.{self.box}_{self.unit_pos}_LOCAL.TLastChangesPLC := DWORD_TO_DT(tAPPInfo.dtLastChanges);\n\n')

            codePLC.append(f'\t// Текущее время контроллера\n')
            codePLC.append(f'\tSysTimeRtcConvertUtcToLocal(SysTimeRtcGet(Error_CODE), PLC_TIME);\n')
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_LOCAL.SysTimePLC := ((DWORD_TO_DT(PLC_TIME)));\n\n')

            codePLC.append(f'\t// Индентификатор IEC данных\n')
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_LOCAL.DataCuid := tappInfo.dataGuid.data1;\n')
            codePLC.append(f'\t// Индентификатор IEC кода\n')
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_LOCAL.CodeCuid := tappInfo.codeGuid.data1;\n\n')

            codePLC.append(
                f'\t// Обнуление массива от второго PLC, если контроллер не ведущий и не ведомый\n')
            codePLC.append(f'\tIF (GLOBAL.STATUS_PLC <> 3 AND GLOBAL.STATUS_PLC <> 5)  THEN\n')
            codePLC.append(
                f'\t\tmem.MemFill(ADR({self.name_db}.{self.box}_{self.unit_pos}_REMOTE), SIZEOF({self.name_db}.{self.box}_{self.unit_pos}_REMOTE), 0);\n')
            codePLC.append(f'\tEND_IF\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL.STATE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.LOAD_CORE_1 := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL.LOAD_CORE_1;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.LOAD_CORE_2 := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL.LOAD_CORE_2;\n')
            # codePLC.append(f'\t\t{self.name_db}.{self.box}_STATE.LOAD_CORE_3 := {self.name_db}.{self.box}_LOCAL.LOAD_CORE_3;\n')
            # codePLC.append(f'\t\t{self.name_db}.{self.box}_STATE.LOAD_CORE_4 := {self.name_db}.{self.box}_LOCAL.LOAD_CORE_4;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.TLastChangesPLC := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL.TLastChangesPLC;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.SysTimePLC := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL.SysTimePLC;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.DataCuid := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL.DataCuid;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.CodeCuid := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL.CodeCuid;\n\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.STATE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.LOAD_CORE_1 := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.LOAD_CORE_1;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.LOAD_CORE_2 := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.LOAD_CORE_2;\n')
            # codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.LOAD_CORE_3 := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.LOAD_CORE_3;\n')
            # codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.LOAD_CORE_4 := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.LOAD_CORE_4;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.TLastChangesPLC := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.TLastChangesPLC;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.SysTimePLC := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.SysTimePLC;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.DataCuid := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.DataCuid;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.CodeCuid := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.CodeCuid;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.STATE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.LOAD_CORE_1 := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.LOAD_CORE_1;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.LOAD_CORE_2 := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.LOAD_CORE_2;\n')
            # codePLC.append(f'\t\t{self.name_db}.{self.box}__{self.unit_pos}_STATE.LOAD_CORE_3 := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.LOAD_CORE_3;\n')
            # codePLC.append(f'\t\t{self.name_db}.{self.box}__{self.unit_pos}_STATE.LOAD_CORE_4 := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.LOAD_CORE_4;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.TLastChangesPLC := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.TLastChangesPLC;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.SysTimePLC := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.SysTimePLC;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.DataCuid := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.DataCuid;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.CodeCuid := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE.CodeCuid;\n\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL.STATE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.LOAD_CORE_1 := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL.LOAD_CORE_1;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.LOAD_CORE_2 := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL.LOAD_CORE_2;\n')
            # codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.LOAD_CORE_3 := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL.LOAD_CORE_3;\n')
            # codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.LOAD_CORE_4 := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL.LOAD_CORE_4;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.TLastChangesPLC := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL.TLastChangesPLC;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.SysTimePLC := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL.SysTimePLC;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.DataCuid := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL.DataCuid;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE.CodeCuid := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL.CodeCuid;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.STATE := STR_LWORD.LWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Загрузка ядер ПЛК\n')
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.LOAD_CORE_1 := UDINT_TO_REAL(si4.cpu_load[0])/10.0;\n')
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.LOAD_CORE_2 := UDINT_TO_REAL(si4.cpu_load[1])/10.0;\n')
            # codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.LOAD_CORE_3 := UDINT_TO_REAL(si4.cpu_load[2])/10.0;\n')
            # codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.LOAD_CORE_4 := UDINT_TO_REAL(si4.cpu_load[3])/10.0;\n\n')

            codePLC.append(f'\t// Время последнего изменения ПО контроллера\n')
            codePLC.append(
                f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.TLastChangesPLC := DWORD_TO_DT(tAPPInfo.dtLastChanges);\n\n')

            codePLC.append(f'\t// Текущее время контроллера\n')
            codePLC.append(f'\t\tSysTimeRtcConvertUtcToLocal(SysTimeRtcGet(Error_CODE), PLC_TIME);\n')
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE.SysTimePLC := ((DWORD_TO_DT(PLC_TIME)));\n\n')
        return codePLC

    def ps(self):
        """
        функция генерации кода для блоков питания (ИБП)
        :return: codePLC = list()
        """
        codePLC = list()

        n_bit = 0  # номер бита для STATE БП
        flg = True  # флаг для записи данных между мастером и ведомым

        codePLC.append(f'\t// Сборка данных по БП (по всем)\n')
        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0; \n\n')

        for jndex, create in enumerate(self.racks):
            self.crateRes = self.systemRes and (jndex == 0)
            if self.systemRes and jndex == 1:
                continue
            for index, module in enumerate(create):
                self.box = module['BOX']
                self.unit_pos = module['UNIT_POSITION']
                self.modul = module['MODULE_CATALOG']
                if ((self.modul == 'R500-PP-00-011 [PS 75W]') or
                    (self.modul == 'R500-PP-00-021 [PS 75W]')):

                    # Система резервированная
                    if self.systemRes:
                        # мы на резервном крейте
                        if self.crateRes:
                            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_0{n_bit} := {self.box}_{self.unit_pos}.ExternPowerIsOk; // {self.box}_{self.unit_pos}. Наличие внешного питания БП\n')
                            n_bit += 1
                        elif not self.crateRes and flg:  # мы записываем обмен между ведущим и ведомым
                            flg = False
                            codePLC.append(f'\n\t{self.name_db}.PS_LOCAL := STR_LWORD.LWORD_IMAGE;\n')
                            codePLC.append(f'\t{self.name_db}.PS_STATE := 0;\n\n')

                            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                            codePLC.append(f'\t\t{self.name_db}.PS_STATE := ({self.name_db}.PS_STATE OR {self.name_db}.PS_LOCAL) OR SHL({self.name_db}.PS_REMOTE, 2);\n')
                            codePLC.append(f'\tELSE\n')
                            codePLC.append(f'\t\t{self.name_db}.PS_STATE := ({self.name_db}.PS_STATE OR {self.name_db}.PS_REMOTE) OR SHL({self.name_db}.PS_LOCAL, 2);\n')
                            codePLC.append(f'\tEND_IF\n\n')
                            codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0; \n\n')
                            n_bit = 4

                        # сборка битов для остальных Rack
                        if jndex > 0:
                            if n_bit <= 9:
                                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_0{n_bit} := {self.box}_{self.unit_pos}.ExternPowerIsOk; // {self.box}_{self.unit_pos}. Наличие внешного питания БП\n')
                            else:
                                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_{n_bit} := {self.box}_{self.unit_pos}.ExternPowerIsOk; // {self.box}_{self.unit_pos}. Наличие внешного питания БП\n')
                            n_bit += 1
                    else:
                        if n_bit <= 9:
                            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_0{n_bit} := {self.box}_{self.unit_pos}.ExternPowerIsOk; // {self.box}_{self.unit_pos}. Наличие внешного питания БП\n')
                        else:
                            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_{n_bit} := {self.box}_{self.unit_pos}.ExternPowerIsOk; // {self.box}_{self.unit_pos}. Наличие внешного питания БП\n')
                        n_bit += 1
        if self.systemRes:
            codePLC.append(f'\n\tDIAG_CPU_self.modulES.PS_STATE := DIAG_CPU_self.modulES.PS_STATE OR STR_LWORD.LWORD_IMAGE; \n\n\n')
        else:
            codePLC.append(f'\n\t{self.name_db}.PS_STATE := STR_LWORD.LWORD_IMAGE; \n\n\n')
        return codePLC

    # функция генерации кода по ошибкам всех модулей
    # def error_racks(self.box, self.modul, self.crateRes, self.name_db, self.unit_pos_res, self.systemRes, self.racks, list_other, list_pp, list_cpu):
    #     # Данная функция отличается от остальных, т.к.
    #     # в ней нужно снова пройтись по всем модулям и
    #     # собрать все ошибки по модулям одного крейта в один бит
    #
    #     codePLC = list()
    #
    #     flg = True  # флаг для записи данных между мастером и ведомым
    #
    #     codePLC.append(f'\t// Сборка данных по ошибкам всех модулей\n')
    #     codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0; \n\n')
    #
    #     # собираем код для каждого крейта
    #     for n_rack in range(0, len(self.racks), 1):
    #         # сам Rack
    #         rack = self.racks[n_rack]
    #
    #         self.crateRes = self.systemRes and (n_rack == 0)
    #
    #         resOprMode = str()
    #         resError = str()
    #
    #         for indx in range(0, len(rack[0]), 1):
    #             self.box = rack[0][indx]
    #             self.modul = rack[1][indx]
    #             if not (self.modul in list_other):
    #                 if self.modul in list_pp:
    #                     resOprMode += str(self.box) + '.ExternPowerIsOk AND '
    #                 elif self.modul in list_cpu:
    #                     resOprMode += str(self.box) + '_STATE.STATE.0 AND '
    #                 else:
    #                     resOprMode += str(self.box) + '_STATE.2 AND '
    #                 resError += str(self.box) + '.HwError OR '
    #
    #         resOprMode = 'NOT (' + resOprMode[: resOprMode.rfind(' AND ')] + ')'
    #         resError = resError[: resError.rfind(' OR ')]
    #         # система резервированная и нашли блок питания
    #         if self.systemRes:
    #             # мы на резервном крейте
    #             if self.crateRes:
    #                 codePLC.append(
    #                     f'\tSTR_LWORD._LWORD.BIT_0{2 * n_rack} := {resOprMode}; // Модуль не установлен в слоте\n')
    #                 codePLC.append(f'\tSTR_LWORD._LWORD.BIT_0{2 * n_rack + 1} := {resError}; // Ошибки крейта\n')
    #             elif not self.crateRes and flg:  # мы записываем обмен между ведущим и ведомым
    #                 flg = False
    #                 codePLC.append(f'\n\t{self.name_db}.ErrorRACK_LOCAL := STR_LWORD.LWORD_IMAGE;\n\n')
    #
    #                 codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
    #                 codePLC.append(
    #                     f'\t\tSTR_LWORD.LWORD_IMAGE := ({self.name_db}.ErrorRACK OR {self.name_db}.ErrorRACK_LOCAL) OR SHL({self.name_db}.ErrorRACK_REMOTE, 2);\n')
    #                 codePLC.append(f'\tELSE\n')
    #                 codePLC.append(
    #                     f'\t\tSTR_LWORD.LWORD_IMAGE := ({self.name_db}.ErrorRACK OR {self.name_db}.ErrorRACK_REMOTE) OR SHL({self.name_db}.ErrorRACK_LOCAL, 2);\n')
    #                 codePLC.append(f'\tEND_IF\n\n')
    #                 codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0; \n\n')
    #
    #             # сборка битов для остальных Rack
    #             if (n_rack > 1) and (n_rack < 5):
    #                 codePLC.append(
    #                     f'\tSTR_LWORD._LWORD.BIT_0{2 * n_rack} := {resOprMode}; // Модуль не установлен в слоте\n')
    #                 codePLC.append(f'\tSTR_LWORD._LWORD.BIT_0{2 * n_rack + 1} := {resError}; // Ошибки крейта\n')
    #
    #             elif (n_rack >= 5):
    #                 codePLC.append(
    #                     f'\tSTR_LWORD._LWORD.BIT_{2 * n_rack} := {resOprMode}; // Модуль не установлен в слоте\n')
    #                 codePLC.append(f'\tSTR_LWORD._LWORD.BIT_{2 * n_rack + 1} := {resError}; // Ошибки крейта\n')
    #
    #         # система не резервированная
    #         elif (not self.systemRes):
    #             if n_rack == 0:
    #                 codePLC.append(
    #                     f'\tSTR_LWORD._LWORD.BIT_0{2 * n_rack} := {resOprMode}; // Модуль не установлен в слоте\n')
    #                 codePLC.append(f'\tSTR_LWORD._LWORD.BIT_0{2 * n_rack + 1} := {resError}; // Ошибки крейта\n')
    #             elif ((n_rack >= 1) and (n_rack < 5)):
    #                 codePLC.append(
    #                     f'\tSTR_LWORD._LWORD.BIT_0{2 * n_rack} := {resOprMode}; // Модуль не установлен в слоте\n')
    #                 codePLC.append(f'\tSTR_LWORD._LWORD.BIT_0{2 * n_rack + 1} := {resError}; // Ошибки крейта\n')
    #             elif (n_rack >= 5):
    #                 codePLC.append(
    #                     f'\tSTR_LWORD._LWORD.BIT_{2 * n_rack} := {resOprMode}; // Модуль не установлен в слоте\n')
    #                 codePLC.append(f'\tSTR_LWORD._LWORD.BIT_{2 * n_rack + 1} := {resError}; // Ошибки крейта\n')
    #
    #     if self.systemRes:
    #         codePLC.append(f'\n\tDIAG_CPU_self.modulES.ErrorRACK := STR_LWORD.LWORD_IMAGE; \n\n\n')
    #     else:
    #         codePLC.append(f'\n\t{self.name_db}.ErrorRACK := STR_LWORD.LWORD_IMAGE; \n\n\n')
    #     return codePLC

    # функция генерации кода для 8AI_I (R500-AI-08-021 [SM 8AI I]; R500-AI-08-041 [SM 8AI I];
    # R500-AI-08-051 [SM 8AI I])
    def ai_08_021(self):
        codePLC = list()
        if self.modul.startswith('R500-AI-08-021 [SM 8AI I]'):
            type_module = f'AI08021_{self.verPdoSdo}_IN'
        elif self.modul.startswith('R500-AI-08-041 [SM 8AI I]'):
            type_module = f'AI08041_{self.verPdoSdo}_IN'
        elif self.modul.startswith('R500-AI-08-051 [SM 8AI I]'):
            type_module = f'AI08051_{self.verPdoSdo}_IN'
        else:
            type_module = 'ERROR********/// '

        match self.verPdoSdo:
            case '05':
                type_break = 'Discarded'
            case '30':
                type_break = 'Break'
            case _:
                type_break = 'ERROR********///'

        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_module} := {self.box}_{self.unit_pos}.Inputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0;\n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль в работе\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль установлен в слоте \n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*(*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*)*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*(*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*)*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 0); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := ({self.box}_{self.unit_pos}.ActiveBusNum = 1); // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_07 := {type_module}.ch[0].Status.{type_break} OR {type_module}.ch[0].Status.Failure OR {type_module}.ch[0].Status.LowerADC OR {type_module}.ch[0].Status.UpperADC;	// Неисправность канала 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_08 := {type_module}.ch[1].Status.{type_break} OR {type_module}.ch[1].Status.Failure OR {type_module}.ch[1].Status.LowerADC OR {type_module}.ch[1].Status.UpperADC;	// Неисправность канала 2 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_09 := {type_module}.ch[2].Status.{type_break} OR {type_module}.ch[2].Status.Failure OR {type_module}.ch[2].Status.LowerADC OR {type_module}.ch[2].Status.UpperADC;	// Неисправность канала 3 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_10 := {type_module}.ch[3].Status.{type_break} OR {type_module}.ch[3].Status.Failure OR {type_module}.ch[3].Status.LowerADC OR {type_module}.ch[3].Status.UpperADC;	// Неисправность канала 4 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_11 := {type_module}.ch[4].Status.{type_break} OR {type_module}.ch[4].Status.Failure OR {type_module}.ch[4].Status.LowerADC OR {type_module}.ch[4].Status.UpperADC;	// Неисправность канала 5 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_12 := {type_module}.ch[5].Status.{type_break} OR {type_module}.ch[5].Status.Failure OR {type_module}.ch[5].Status.LowerADC OR {type_module}.ch[5].Status.UpperADC;	// Неисправность канала 6 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_13 := {type_module}.ch[6].Status.{type_break} OR {type_module}.ch[6].Status.Failure OR {type_module}.ch[6].Status.LowerADC OR {type_module}.ch[6].Status.UpperADC;	// Неисправность канала 7 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_14 := {type_module}.ch[7].Status.{type_break} OR {type_module}.ch[7].Status.Failure OR {type_module}.ch[7].Status.LowerADC OR {type_module}.ch[7].Status.UpperADC;	// Неисправность канала 8 \n\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_15 := {type_module}.ch[0].Status.UpperElectrical OR {type_module}.ch[0].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_16 := {type_module}.ch[1].Status.UpperElectrical OR {type_module}.ch[1].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 2 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_17 := {type_module}.ch[2].Status.UpperElectrical OR {type_module}.ch[2].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 3 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_18 := {type_module}.ch[3].Status.UpperElectrical OR {type_module}.ch[3].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 4 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_19 := {type_module}.ch[4].Status.UpperElectrical OR {type_module}.ch[4].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 5 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_20 := {type_module}.ch[5].Status.UpperElectrical OR {type_module}.ch[5].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 6 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_21 := {type_module}.ch[6].Status.UpperElectrical OR {type_module}.ch[6].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 7 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_22 := {type_module}.ch[7].Status.UpperElectrical OR {type_module}.ch[7].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 8 \n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_module}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_LOCAL := STR_LWORD.LWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(
                f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def ai_08_022(self):
        """
        функция генерации кода для
        R500-AI-08-022 [SM 8AI I]
        R500-AI-08-042 [SM 8AI I]
        R500-AI-08-052 [SM 8AI I]
        R500-AI-08-242 [SM 8AI I]
        :return: codePLC = list()
        """
        codePLC = list()

        if self.modul.startswith('R500-AI-08-022 [SM 8AI I]'):
            type_module = f'AI08022_{self.verPdoSdo}_IN'
        elif self.modul.startswith('R500-AI-08-042 [SM 8AI I]'):
            type_module = f'AI08042_{self.verPdoSdo}_IN'
        elif self.modul.startswith('R500-AI-08-052 [SM 8AI I]'):
            type_module = f'AI08052_{self.verPdoSdo}_IN'
        elif self.modul.startswith('R500-AI-08-242 [SM 8AI I]'):
            type_module = f'AI08242_{self.verPdoSdo}_IN'
        else:
            type_module = 'ERROR********/// '

        match self.verPdoSdo:
            case '05':
                type_break = 'Break'
            case '01' | '30':
                type_break = 'Discarded'
            case _:
                type_break = 'ERROR********///'

        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        #codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_module} := {self.box}_{self.unit_pos}.Inputs;\n')
        #codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0;\n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль в работе\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль установлен в слоте \n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 1); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := ({self.box}_{self.unit_pos}.ActiveBusNum = 2); // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_07 := {type_module}.ch[0].Status.{type_break} OR {type_module}.ch[0].Status.Failure OR {type_module}.ch[0].Status.LowerADC OR {type_module}.ch[0].Status.UpperADC;	// Неисправность канала 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_08 := {type_module}.ch[1].Status.{type_break} OR {type_module}.ch[1].Status.Failure OR {type_module}.ch[1].Status.LowerADC OR {type_module}.ch[1].Status.UpperADC;	// Неисправность канала 2 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_09 := {type_module}.ch[2].Status.{type_break} OR {type_module}.ch[2].Status.Failure OR {type_module}.ch[2].Status.LowerADC OR {type_module}.ch[2].Status.UpperADC;	// Неисправность канала 3 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_10 := {type_module}.ch[3].Status.{type_break} OR {type_module}.ch[3].Status.Failure OR {type_module}.ch[3].Status.LowerADC OR {type_module}.ch[3].Status.UpperADC;	// Неисправность канала 4 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_11 := {type_module}.ch[4].Status.{type_break} OR {type_module}.ch[4].Status.Failure OR {type_module}.ch[4].Status.LowerADC OR {type_module}.ch[4].Status.UpperADC;	// Неисправность канала 5 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_12 := {type_module}.ch[5].Status.{type_break} OR {type_module}.ch[5].Status.Failure OR {type_module}.ch[5].Status.LowerADC OR {type_module}.ch[5].Status.UpperADC;	// Неисправность канала 6 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_13 := {type_module}.ch[6].Status.{type_break} OR {type_module}.ch[6].Status.Failure OR {type_module}.ch[6].Status.LowerADC OR {type_module}.ch[6].Status.UpperADC;	// Неисправность канала 7 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_14 := {type_module}.ch[7].Status.{type_break} OR {type_module}.ch[7].Status.Failure OR {type_module}.ch[7].Status.LowerADC OR {type_module}.ch[7].Status.UpperADC;	// Неисправность канала 8 \n\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_15 := {type_module}.ch[0].Status.UpperElectrical OR {type_module}.ch[0].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_16 := {type_module}.ch[1].Status.UpperElectrical OR {type_module}.ch[1].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 2 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_17 := {type_module}.ch[2].Status.UpperElectrical OR {type_module}.ch[2].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 3 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_18 := {type_module}.ch[3].Status.UpperElectrical OR {type_module}.ch[3].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 4 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_19 := {type_module}.ch[4].Status.UpperElectrical OR {type_module}.ch[4].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 5 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_20 := {type_module}.ch[5].Status.UpperElectrical OR {type_module}.ch[5].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 6 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_21 := {type_module}.ch[6].Status.UpperElectrical OR {type_module}.ch[6].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 7 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_22 := {type_module}.ch[7].Status.UpperElectrical OR {type_module}.ch[7].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 8 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_23 := {type_module}.PowerState.IntPowerState_0;	// Состояние питания внутренней шины 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_24 := {type_module}.PowerState.IntPowerState_1;	// Состояние питания внутренней шины 2 \n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_module}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_LWORD.LWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def ai_08_142(self):
        """
        функция генерации кода для
        R500-AI-08-142 [SM 8AI I]
        R500-AI-08-342 [SM 8AI I]
        :return: codePLC = list()
        """
        codePLC = list()

        if self.modul.startswith('R500-AI-08-142 [SM 8AI I]'):
            type_module = f'AI08142_{self.verPdoSdo}_IN'
        elif self.modul.startswith('R500-AI-08-342 [SM 8AI I]'):
            type_module = f'AI08342_{self.verPdoSdo}_IN'
        else:
            type_module = 'ERROR********/// '

        match self.verPdoSdo:
            case '05':
                type_break = 'Discarded'
            case '30':
                type_break = 'Break'
            case _:
                type_break = 'ERROR********///'

        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        #codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_module} := {self.box}_{self.unit_pos}.Inputs;\n')
        #codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0;\n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль в работе\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль установлен в слоте \n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 1); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := ({self.box}_{self.unit_pos}.ActiveBusNum = 2); // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_07 := {type_module}.ch[0].Status.{type_break} OR {type_module}.ch[0].Status.Failure OR {type_module}.ch[0].Status.LowerADC OR {type_module}.ch[0].Status.UpperADC;	// Неисправность канала 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_08 := {type_module}.ch[1].Status.{type_break} OR {type_module}.ch[1].Status.Failure OR {type_module}.ch[1].Status.LowerADC OR {type_module}.ch[1].Status.UpperADC;	// Неисправность канала 2 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_09 := {type_module}.ch[2].Status.{type_break} OR {type_module}.ch[2].Status.Failure OR {type_module}.ch[2].Status.LowerADC OR {type_module}.ch[2].Status.UpperADC;	// Неисправность канала 3 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_10 := {type_module}.ch[3].Status.{type_break} OR {type_module}.ch[3].Status.Failure OR {type_module}.ch[3].Status.LowerADC OR {type_module}.ch[3].Status.UpperADC;	// Неисправность канала 4 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_11 := {type_module}.ch[4].Status.{type_break} OR {type_module}.ch[4].Status.Failure OR {type_module}.ch[4].Status.LowerADC OR {type_module}.ch[4].Status.UpperADC;	// Неисправность канала 5 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_12 := {type_module}.ch[5].Status.{type_break} OR {type_module}.ch[5].Status.Failure OR {type_module}.ch[5].Status.LowerADC OR {type_module}.ch[5].Status.UpperADC;	// Неисправность канала 6 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_13 := {type_module}.ch[6].Status.{type_break} OR {type_module}.ch[6].Status.Failure OR {type_module}.ch[6].Status.LowerADC OR {type_module}.ch[6].Status.UpperADC;	// Неисправность канала 7 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_14 := {type_module}.ch[7].Status.{type_break} OR {type_module}.ch[7].Status.Failure OR {type_module}.ch[7].Status.LowerADC OR {type_module}.ch[7].Status.UpperADC;	// Неисправность канала 8 \n\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_15 := {type_module}.ch[0].Status.UpperElectrical OR {type_module}.ch[0].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_16 := {type_module}.ch[1].Status.UpperElectrical OR {type_module}.ch[1].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 2 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_17 := {type_module}.ch[2].Status.UpperElectrical OR {type_module}.ch[2].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 3 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_18 := {type_module}.ch[3].Status.UpperElectrical OR {type_module}.ch[3].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 4 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_19 := {type_module}.ch[4].Status.UpperElectrical OR {type_module}.ch[4].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 5 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_20 := {type_module}.ch[5].Status.UpperElectrical OR {type_module}.ch[5].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 6 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_21 := {type_module}.ch[6].Status.UpperElectrical OR {type_module}.ch[6].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 7 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_22 := {type_module}.ch[7].Status.UpperElectrical OR {type_module}.ch[7].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 8 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_23 := {type_module}.PowerState.IntPowerState_0	// Состояние питания внутренней шины 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_24 := {type_module}.PowerState.IntPowerState_1	// Состояние питания внутренней шины 2 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_25 := {type_module}.PowerState.ExtPowerState_1	// Состояние питания внешней шины 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_26 := {type_module}.PowerState.ExtPowerState_1	// Состояние питания внешней шины 2 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_27 := {type_module}.PowerStatus.Channel1_PowerStatus	// Состояние питания канала 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_28 := {type_module}.PowerStatus.Channel2_PowerStatus	// Состояние питания канала 2 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_29 := {type_module}.PowerStatus.Channel3_PowerStatus	// Состояние питания канала 3 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_30 := {type_module}.PowerStatus.Channel4_PowerStatus	// Состояние питания канала 4 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_31 := {type_module}.PowerStatus.Channel5_PowerStatus	// Состояние питания канала 5 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_32 := {type_module}.PowerStatus.Channel6_PowerStatus	// Состояние питания канала 6 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_33 := {type_module}.PowerStatus.Channel7_PowerStatus	// Состояние питания канала 7 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_34 := {type_module}.PowerStatus.Channel8_PowerStatus	// Состояние питания канала 8 \n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_module}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def ai_08_031(self):
        """
        функция генерации кода для
        R500-AI-08-031 [SM 8AI RTD/TC]
        R500-AI-08-131 [SM 8AI RTD/TC]
        :return: codePLC = list()
        """
        codePLC = list()

        if self.modul.startswith('R500-AI-08-031 [SM 8AI RTD/TC]'):
            type_module = f'AI08031_{self.verPdoSdo}_IN'
        elif self.modul.startswith('R500-AI-08-131 [SM 8AI RTD/TC]'):
            type_module = f'AI08131_{self.verPdoSdo}_IN'
        else:
            type_module = 'ERROR********/// '

        match self.verPdoSdo:
            case '05':
                type_break = 'Discarded'
            case '30':
                type_break = 'Break'
            case _:
                type_break = 'ERROR********///'

        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_module} := {self.box}_{self.unit_pos}.Inputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0; \n\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль в работе \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль установлен в слоте \n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 0); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := ({self.box}_{self.unit_pos}.ActiveBusNum = 1); // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_07 := {type_module}.ch[0].Status.{type_break} OR {type_module}.ch[0].Status.Failure OR {type_module}.ch[0].Status.LowerADC OR {type_module}.ch[0].Status.UpperADC;	// Неисправность канала 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_08 := {type_module}.ch[1].Status.{type_break} OR {type_module}.ch[1].Status.Failure OR {type_module}.ch[1].Status.LowerADC OR {type_module}.ch[1].Status.UpperADC;	// Неисправность канала 2 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_09 := {type_module}.ch[2].Status.{type_break} OR {type_module}.ch[2].Status.Failure OR {type_module}.ch[2].Status.LowerADC OR {type_module}.ch[2].Status.UpperADC;	// Неисправность канала 3 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_10 := {type_module}.ch[3].Status.{type_break} OR {type_module}.ch[3].Status.Failure OR {type_module}.ch[3].Status.LowerADC OR {type_module}.ch[3].Status.UpperADC;	// Неисправность канала 4 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_11 := {type_module}.ch[4].Status.{type_break} OR {type_module}.ch[4].Status.Failure OR {type_module}.ch[4].Status.LowerADC OR {type_module}.ch[4].Status.UpperADC;	// Неисправность канала 5 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_12 := {type_module}.ch[5].Status.{type_break} OR {type_module}.ch[5].Status.Failure OR {type_module}.ch[5].Status.LowerADC OR {type_module}.ch[5].Status.UpperADC;	// Неисправность канала 6 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_13 := {type_module}.ch[6].Status.{type_break} OR {type_module}.ch[6].Status.Failure OR {type_module}.ch[6].Status.LowerADC OR {type_module}.ch[6].Status.UpperADC;	// Неисправность канала 7 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_14 := {type_module}.ch[7].Status.{type_break} OR {type_module}.ch[7].Status.Failure OR {type_module}.ch[7].Status.LowerADC OR {type_module}.ch[7].Status.UpperADC;	// Неисправность канала 8 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_15 := {type_module}.ch[0].Status.UpperElectrical OR {type_module}.ch[0].Status.LowerElectrical; // Выход за пределы эл.ед. канала 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_16 := {type_module}.ch[1].Status.UpperElectrical OR {type_module}.ch[1].Status.LowerElectrical; // Выход за пределы эл.ед. канала 2 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_17 := {type_module}.ch[2].Status.UpperElectrical OR {type_module}.ch[2].Status.LowerElectrical; // Выход за пределы эл.ед. канала 3 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_18 := {type_module}.ch[3].Status.UpperElectrical OR {type_module}.ch[3].Status.LowerElectrical; // Выход за пределы эл.ед. канала 4 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_19 := {type_module}.ch[4].Status.UpperElectrical OR {type_module}.ch[4].Status.LowerElectrical; // Выход за пределы эл.ед. канала 5 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_20 := {type_module}.ch[5].Status.UpperElectrical OR {type_module}.ch[5].Status.LowerElectrical; // Выход за пределы эл.ед. канала 6 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_21 := {type_module}.ch[6].Status.UpperElectrical OR {type_module}.ch[6].Status.LowerElectrical; // Выход за пределы эл.ед. канала 7 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_22 := {type_module}.ch[7].Status.UpperElectrical OR {type_module}.ch[7].Status.LowerElectrical; // Выход за пределы эл.ед. канала 8 \n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_module}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def ai_16_011(self):
        """
        функция генерации кода для
        R500-AI-16-011 [SM 16AI I]
        R500-AI-16-012 [SM 16AI I]
        R500-AI-16-081 [SM 16AI I])
        :return: codePLC = list()
        """
        codePLC = list()
        if self.modul.startswith('R500-AI-16-011 [SM 16AI I]'):
            type_module = f'AI16011_{self.verPdoSdo}_IN'
        elif self.modul.startswith('R500-AI-16-081 [SM 16AI I]'):
            type_module = f'AI16081_{self.verPdoSdo}_IN'
        elif self.modul.startswith('R500-AI-16-012 [SM 16AI I]'):
            type_module = f'AI16012_{self.verPdoSdo}_IN'
        else:
            type_module = 'ERROR********/// '

        match self.verPdoSdo:
            case '05':
                type_break = 'Break'
            case '02' | '30':
                type_break = 'Discarded'
            case _:
                type_break = 'ERROR********///'

        # код сбора STATE
        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_module} := {self.box}_{self.unit_pos}.Inputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0; \n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль в работе \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль установлен в слоте \n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 0); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := ({self.box}_{self.unit_pos}.ActiveBusNum = 1); // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_07 := {type_module}.ch[0].Status.{type_break} OR {type_module}.ch[0].Status.Failure OR {type_module}.ch[0].Status.LowerADC OR {type_module}.ch[0].Status.UpperADC;	// Неисправность канала 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_08 := {type_module}.ch[1].Status.{type_break} OR {type_module}.ch[1].Status.Failure OR {type_module}.ch[1].Status.LowerADC OR {type_module}.ch[1].Status.UpperADC;	// Неисправность канала 2 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_09 := {type_module}.ch[2].Status.{type_break} OR {type_module}.ch[2].Status.Failure OR {type_module}.ch[2].Status.LowerADC OR {type_module}.ch[2].Status.UpperADC;	// Неисправность канала 3 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_10 := {type_module}.ch[3].Status.{type_break} OR {type_module}.ch[3].Status.Failure OR {type_module}.ch[3].Status.LowerADC OR {type_module}.ch[3].Status.UpperADC;	// Неисправность канала 4 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_11 := {type_module}.ch[4].Status.{type_break} OR {type_module}.ch[4].Status.Failure OR {type_module}.ch[4].Status.LowerADC OR {type_module}.ch[4].Status.UpperADC;	// Неисправность канала 5 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_12 := {type_module}.ch[5].Status.{type_break} OR {type_module}.ch[5].Status.Failure OR {type_module}.ch[5].Status.LowerADC OR {type_module}.ch[5].Status.UpperADC;	// Неисправность канала 6 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_13 := {type_module}.ch[6].Status.{type_break} OR {type_module}.ch[6].Status.Failure OR {type_module}.ch[6].Status.LowerADC OR {type_module}.ch[6].Status.UpperADC;	// Неисправность канала 7 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_14 := {type_module}.ch[7].Status.{type_break} OR {type_module}.ch[7].Status.Failure OR {type_module}.ch[7].Status.LowerADC OR {type_module}.ch[7].Status.UpperADC;	// Неисправность канала 8 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_15 := {type_module}.ch[8].Status.{type_break} OR {type_module}.ch[8].Status.Failure OR {type_module}.ch[8].Status.LowerADC OR {type_module}.ch[8].Status.UpperADC;	// Неисправность канала 9 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_16 := {type_module}.ch[9].Status.{type_break} OR {type_module}.ch[9].Status.Failure OR {type_module}.ch[9].Status.LowerADC OR {type_module}.ch[9].Status.UpperADC;	// Неисправность канала 10 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_17 := {type_module}.ch[10].Status.{type_break} OR {type_module}.ch[10].Status.Failure OR {type_module}.ch[10].Status.LowerADC OR {type_module}.ch[10].Status.UpperADC;	// Неисправность канала 11 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_18 := {type_module}.ch[11].Status.{type_break} OR {type_module}.ch[11].Status.Failure OR {type_module}.ch[11].Status.LowerADC OR {type_module}.ch[11].Status.UpperADC;	// Неисправность канала 12 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_19 := {type_module}.ch[12].Status.{type_break} OR {type_module}.ch[12].Status.Failure OR {type_module}.ch[12].Status.LowerADC OR {type_module}.ch[12].Status.UpperADC;	// Неисправность канала 13 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_20 := {type_module}.ch[13].Status.{type_break} OR {type_module}.ch[13].Status.Failure OR {type_module}.ch[13].Status.LowerADC OR {type_module}.ch[13].Status.UpperADC;	// Неисправность канала 14 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_21 := {type_module}.ch[14].Status.{type_break} OR {type_module}.ch[14].Status.Failure OR {type_module}.ch[14].Status.LowerADC OR {type_module}.ch[14].Status.UpperADC;	// Неисправность канала 15 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_22 := {type_module}.ch[15].Status.{type_break} OR {type_module}.ch[15].Status.Failure OR {type_module}.ch[15].Status.LowerADC OR {type_module}.ch[15].Status.UpperADC;	// Неисправность канала 16 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_23 := {type_module}.ch[0].Status.UpperElectrical OR {type_module}.ch[0].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_24 := {type_module}.ch[1].Status.UpperElectrical OR {type_module}.ch[1].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 2 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_25 := {type_module}.ch[2].Status.UpperElectrical OR {type_module}.ch[2].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 3 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_26 := {type_module}.ch[3].Status.UpperElectrical OR {type_module}.ch[3].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 4 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_27 := {type_module}.ch[4].Status.UpperElectrical OR {type_module}.ch[4].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 5 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_28 := {type_module}.ch[5].Status.UpperElectrical OR {type_module}.ch[5].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 6 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_29 := {type_module}.ch[6].Status.UpperElectrical OR {type_module}.ch[6].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 7 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_30 := {type_module}.ch[7].Status.UpperElectrical OR {type_module}.ch[7].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 8 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_31 := {type_module}.ch[8].Status.UpperElectrical OR {type_module}.ch[8].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 9 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_32 := {type_module}.ch[9].Status.UpperElectrical OR {type_module}.ch[9].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 10 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_33 := {type_module}.ch[10].Status.UpperElectrical OR {type_module}.ch[10].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 11 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_34 := {type_module}.ch[11].Status.UpperElectrical OR {type_module}.ch[11].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 12 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_35 := {type_module}.ch[12].Status.UpperElectrical OR {type_module}.ch[12].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 13 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_36 := {type_module}.ch[13].Status.UpperElectrical OR {type_module}.ch[13].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 14 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_37 := {type_module}.ch[14].Status.UpperElectrical OR {type_module}.ch[14].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 15 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_38 := {type_module}.ch[15].Status.UpperElectrical OR {type_module}.ch[15].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 16 \n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_module}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def ai_16_012(self):
        """
        функция генерации кода для
        R500-AI-16-012 [SM 16AI I]
        :return: codePLC = list()
        """
        codePLC = list()
        if self.modul.startswith('R500-AI-16-012 [SM 16AI I]'):
            type_module = f'AI16012_{self.verPdoSdo}_IN'
        else:
            type_module = 'ERROR********/// '

        match self.verPdoSdo:
            case '05':
                type_break = 'Break'
            case '30':
                type_break = 'Discarded'
            case _:
                type_break = 'ERROR********///'

        # код сбора STATE
        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_module} := {self.box}_{self.unit_pos}.Inputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0; \n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль в работе \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль установлен в слоте \n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 0); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := ({self.box}_{self.unit_pos}.ActiveBusNum = 1); // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_07 := {type_module}.PowerState.IntPowerState_0;	// Внутреняя шина 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_08 := {type_module}.PowerState.IntPowerState_1;	// Внутреняя шина 2 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_09 := {type_module}.ch[0].Status.{type_break} OR {type_module}.ch[0].Status.Failure OR {type_module}.ch[0].Status.LowerADC OR {type_module}.ch[0].Status.UpperADC;	// Неисправность канала 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_10 := {type_module}.ch[1].Status.{type_break} OR {type_module}.ch[1].Status.Failure OR {type_module}.ch[1].Status.LowerADC OR {type_module}.ch[1].Status.UpperADC;	// Неисправность канала 2 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_11 := {type_module}.ch[2].Status.{type_break} OR {type_module}.ch[2].Status.Failure OR {type_module}.ch[2].Status.LowerADC OR {type_module}.ch[2].Status.UpperADC;	// Неисправность канала 3 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_12 := {type_module}.ch[3].Status.{type_break} OR {type_module}.ch[3].Status.Failure OR {type_module}.ch[3].Status.LowerADC OR {type_module}.ch[3].Status.UpperADC;	// Неисправность канала 4 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_13 := {type_module}.ch[4].Status.{type_break} OR {type_module}.ch[4].Status.Failure OR {type_module}.ch[4].Status.LowerADC OR {type_module}.ch[4].Status.UpperADC;	// Неисправность канала 5 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_14 := {type_module}.ch[5].Status.{type_break} OR {type_module}.ch[5].Status.Failure OR {type_module}.ch[5].Status.LowerADC OR {type_module}.ch[5].Status.UpperADC;	// Неисправность канала 6 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_15 := {type_module}.ch[6].Status.{type_break} OR {type_module}.ch[6].Status.Failure OR {type_module}.ch[6].Status.LowerADC OR {type_module}.ch[6].Status.UpperADC;	// Неисправность канала 7 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_16 := {type_module}.ch[7].Status.{type_break} OR {type_module}.ch[7].Status.Failure OR {type_module}.ch[7].Status.LowerADC OR {type_module}.ch[7].Status.UpperADC;	// Неисправность канала 8 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_17 := {type_module}.ch[8].Status.{type_break} OR {type_module}.ch[8].Status.Failure OR {type_module}.ch[8].Status.LowerADC OR {type_module}.ch[8].Status.UpperADC;	// Неисправность канала 9 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_18 := {type_module}.ch[9].Status.{type_break} OR {type_module}.ch[9].Status.Failure OR {type_module}.ch[9].Status.LowerADC OR {type_module}.ch[9].Status.UpperADC;	// Неисправность канала 10 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_19 := {type_module}.ch[10].Status.{type_break} OR {type_module}.ch[10].Status.Failure OR {type_module}.ch[10].Status.LowerADC OR {type_module}.ch[10].Status.UpperADC;	// Неисправность канала 11 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_20 := {type_module}.ch[11].Status.{type_break} OR {type_module}.ch[11].Status.Failure OR {type_module}.ch[11].Status.LowerADC OR {type_module}.ch[11].Status.UpperADC;	// Неисправность канала 12 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_21 := {type_module}.ch[12].Status.{type_break} OR {type_module}.ch[12].Status.Failure OR {type_module}.ch[12].Status.LowerADC OR {type_module}.ch[12].Status.UpperADC;	// Неисправность канала 13 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_22 := {type_module}.ch[13].Status.{type_break} OR {type_module}.ch[13].Status.Failure OR {type_module}.ch[13].Status.LowerADC OR {type_module}.ch[13].Status.UpperADC;	// Неисправность канала 14 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_23 := {type_module}.ch[14].Status.{type_break} OR {type_module}.ch[14].Status.Failure OR {type_module}.ch[14].Status.LowerADC OR {type_module}.ch[14].Status.UpperADC;	// Неисправность канала 15 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_24 := {type_module}.ch[15].Status.{type_break} OR {type_module}.ch[15].Status.Failure OR {type_module}.ch[15].Status.LowerADC OR {type_module}.ch[15].Status.UpperADC;	// Неисправность канала 16 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_25 := {type_module}.ch[0].Status.UpperElectrical OR {type_module}.ch[0].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_26 := {type_module}.ch[1].Status.UpperElectrical OR {type_module}.ch[1].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 2 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_27 := {type_module}.ch[2].Status.UpperElectrical OR {type_module}.ch[2].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 3 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_28 := {type_module}.ch[3].Status.UpperElectrical OR {type_module}.ch[3].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 4 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_29 := {type_module}.ch[4].Status.UpperElectrical OR {type_module}.ch[4].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 5 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_30 := {type_module}.ch[5].Status.UpperElectrical OR {type_module}.ch[5].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 6 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_31 := {type_module}.ch[6].Status.UpperElectrical OR {type_module}.ch[6].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 7 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_32 := {type_module}.ch[7].Status.UpperElectrical OR {type_module}.ch[7].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 8 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_33 := {type_module}.ch[8].Status.UpperElectrical OR {type_module}.ch[8].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 9 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_34 := {type_module}.ch[9].Status.UpperElectrical OR {type_module}.ch[9].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 10 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_35 := {type_module}.ch[10].Status.UpperElectrical OR {type_module}.ch[10].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 11 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_36 := {type_module}.ch[11].Status.UpperElectrical OR {type_module}.ch[11].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 12 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_37 := {type_module}.ch[12].Status.UpperElectrical OR {type_module}.ch[12].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 13 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_38 := {type_module}.ch[13].Status.UpperElectrical OR {type_module}.ch[13].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 14 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_39 := {type_module}.ch[14].Status.UpperElectrical OR {type_module}.ch[14].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 15 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_40 := {type_module}.ch[15].Status.UpperElectrical OR {type_module}.ch[15].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 16 \n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_module}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def ao_08_011(self):
        """
        функция генерации кода для
        R500-AO-08-011 [SM 8AO I]
        R500-AO-08-021 [SM 8AO I]
        R500-AO-08-031 [SM 8AO I]
        :return: codePLC = list()
        """
        codePLC = list()

        if self.modul.startswith('R500-AO-08-011 [SM 8AO I]'):
            type_module = f'AO08011_{self.verPdoSdo}_IN'
        elif self.modul.startswith('R500-AO-08-021 [SM 8AO I]'):
            type_module = f'AO08021_{self.verPdoSdo}_IN'
        elif self.modul.startswith('R500-AO-08-031 [SM 8AO I]'):
            type_module = f'AO08031_{self.verPdoSdo}_IN'
        else:
            type_module = 'ERROR********/// '

        # код сбора STATE
        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_module} := {self.box}_{self.unit_pos}.Inputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0; \n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль в работе \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль установлен в слоте \n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 0); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := ({self.box}_{self.unit_pos}.ActiveBusNum = 1); // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_07 := {type_module}.Status.NoOuterPowerSupply;// Нет внешнего питания; \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_08 := {type_module}.Status.Breakage0; // Обрыв канала 1 \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_09 := {type_module}.Status.Breakage1; // Обрыв канала 2 \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_10 := {type_module}.Status.Breakage2; // Обрыв канала 3 \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_11 := {type_module}.Status.Breakage3; // Обрыв канала 4 \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_12 := {type_module}.Status.Breakage4; // Обрыв канала 5 \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_13 := {type_module}.Status.Breakage5; // Обрыв канала 6 \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_14 := {type_module}.Status.Breakage6; // Обрыв канала 7 \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_15 := {type_module}.Status.Breakage7; // Обрыв канала 8 \n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_module}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def as_08_011(self):
        """
        функция генерации кода для
        R500-AS-08-011 [SM 8AI I]
        :return: codePLC = list()
        """
        codePLC = list()

        if self.modul.startswith('R500-AS-08-011 [SM 8AI I]'):
            type_module = f'AS08011_{self.verPdoSdo}_IN'
        else:
            type_module = 'ERROR********/// '

        match self.verPdoSdo:
            case '05':
                type_break = 'Break'
            case '30':
                type_break = 'Discarded'
            case _:
                type_break = 'ERROR********///'

        # код сбора STATE
        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_module} := {self.box}_{self.unit_pos}.Inputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_DWORD.DWORD_IMAGE := 0;\n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль в работе\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль установлен в слоте \n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 1); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := ({self.box}_{self.unit_pos}.ActiveBusNum = 2); // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_07 := {type_module}.ch[0].Status.{type_break} OR {type_module}.ch[0].Status.Failure OR {type_module}.ch[0].Status.LowerADC OR {type_module}.ch[0].Status.UpperADC;	// Неисправность канала 1 (вх) \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_08 := {type_module}.ch[1].Status.{type_break} OR {type_module}.ch[1].Status.Failure OR {type_module}.ch[1].Status.LowerADC OR {type_module}.ch[1].Status.UpperADC;	// Неисправность канала 2 (вх) \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_09 := {type_module}.ch[2].Status.{type_break} OR {type_module}.ch[2].Status.Failure OR {type_module}.ch[2].Status.LowerADC OR {type_module}.ch[2].Status.UpperADC;	// Неисправность канала 3 (вх) \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_10 := {type_module}.ch[3].Status.{type_break} OR {type_module}.ch[3].Status.Failure OR {type_module}.ch[3].Status.LowerADC OR {type_module}.ch[3].Status.UpperADC;	// Неисправность канала 4 (вх) \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_11 := {type_module}.ch[4].Status.{type_break} OR {type_module}.ch[4].Status.Failure OR {type_module}.ch[4].Status.LowerADC OR {type_module}.ch[4].Status.UpperADC;	// Неисправность канала 5 (вх) \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_12 := {type_module}.ch[5].Status.{type_break} OR {type_module}.ch[5].Status.Failure OR {type_module}.ch[5].Status.LowerADC OR {type_module}.ch[5].Status.UpperADC;	// Неисправность канала 6 (вх) \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_13 := {type_module}.ch[6].Status.{type_break} OR {type_module}.ch[6].Status.Failure OR {type_module}.ch[6].Status.LowerADC OR {type_module}.ch[6].Status.UpperADC;	// Неисправность канала 7 (вх) \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_14 := {type_module}.ch[7].Status.{type_break} OR {type_module}.ch[7].Status.Failure OR {type_module}.ch[7].Status.LowerADC OR {type_module}.ch[7].Status.UpperADC;	// Неисправность канала 8 (вх) \n\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_15 := {type_module}.ch[0].Status.UpperElectrical OR {type_module}.ch[0].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 1 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_16 := {type_module}.ch[1].Status.UpperElectrical OR {type_module}.ch[1].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 2 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_17 := {type_module}.ch[2].Status.UpperElectrical OR {type_module}.ch[2].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 3 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_18 := {type_module}.ch[3].Status.UpperElectrical OR {type_module}.ch[3].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 4 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_19 := {type_module}.ch[4].Status.UpperElectrical OR {type_module}.ch[4].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 5 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_20 := {type_module}.ch[5].Status.UpperElectrical OR {type_module}.ch[5].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 6 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_21 := {type_module}.ch[6].Status.UpperElectrical OR {type_module}.ch[6].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 7 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_22 := {type_module}.ch[7].Status.UpperElectrical OR {type_module}.ch[7].Status.LowerElectrical;	// Выход за пределы эл.ед. канала 8 \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_23 := {type_module}.self.moduleStatus.NoOuterPowerSupply;	// Нет внешнего питания (вых.) \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_24 := {type_module}.self.moduleStatus.self.moduleStatus.Breakage0;	// Обрыв канала 1 (вых.) \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_25 := {type_module}.self.moduleStatus.self.moduleStatus.Breakage1;	// Обрыв канала 2 (вых.) \n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_module}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def di_16_021(self):
        """
        функция генерации кода для
        R500-DI-16-021 [SM 16DI AC220V]
        :return:
        """
        codePLC = list()

        if self.modul.startswith('R500-DI-16-021 [SM 16DI AC220V]'):
            type_module = f'DI16021_{self.verPdoSdo}_IN'
        else:
            type_module = 'ERROR********/// '

        # код сбора STATE
        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_module} := {self.box}_{self.unit_pos}.Inputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0;\n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat; \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль установлен в слоте\n\n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 1); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := ({self.box}_{self.unit_pos}.ActiveBusNum = 2); // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(WORD_TO_LWORD({type_module}.Discrets), 7);\n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_module}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def di_16_032(self):
        """
        функция генерации кода для
        R500-DI-16-032 [SM 16DI AC220V]
        :return: codePLC = list()
        """
        codePLC = list()

        if self.modul.startswith('R500-DI-16-032 [SM 16DI AC220V]'):
            type_module = f'DI16032_{self.verPdoSdo}_IN'
        else:
            type_module = 'ERROR********/// '

        # код сбора STATE
        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_module} := {self.box}_{self.unit_pos}.Inputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0;\n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat; \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль установлен в слоте\n\n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 2) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 1); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := ({self.box}_{self.unit_pos}.ActiveBusNum = 2); // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')

        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(BYTE_TO_LWORD({type_module}.PowerState), 7); \n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(WORD_TO_LWORD({type_module}.OC), 10); \n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(WORD_TO_LWORD({type_module}.SC), 26); \n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(WORD_TO_LWORD({type_module}.Discrets), 42); \n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_module}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def di_32_011(self):
        """
        функция генерации кода для
        R500-DI-32-011 [SM 32DI DC24V]
        R500-DI-32-012 [SM 32DI DC24V]
        R500-DI-32-013 [SM 32DI DC24V]
        R500-DI-32-111 [SM 32DI DC24V]
        :return: codePLC = list()
        """
        codePLC = list()

        if self.modul.startswith('R500-DI-32-011 [SM 32DI DC24V]'):
            type_module = f'DI32011_{self.verPdoSdo}_IN'
        elif self.modul.startswith('R500-DI-32-012 [SM 32DI DC24V]'):
            type_module = f'DI32012_{self.verPdoSdo}_IN'
        elif self.modul.startswith('R500-DI-32-013 [SM 32DI DC24V]'):
            type_module = f'DI32013_{self.verPdoSdo}_IN'
        elif self.modul.startswith('R500-DI-32-111 [SM 32DI DC24V]'):
            type_module = f'DI32111_{self.verPdoSdo}_IN'
        else:
            type_module = 'ERROR********/// '

        # код сбора STATE
        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_module} := {self.box}_{self.unit_pos}.Inputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0;\n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat; \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль установлен в слоте\n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 0); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := ({self.box}_{self.unit_pos}.ActiveBusNum = 1); // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')

        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(DWORD_TO_LWORD({type_module}.Discrets), 7); \n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_module}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def do_16_021(self):
        """
        функция генерации кода для
        R500-DO-16-021 [SM 16DO AC220V]
        :return: codePLC = list()
        """
        codePLC = list()

        if self.modul.startswith('R500-DO-16-021 [SM 16DO AC220V]'):
            type_moduleInput = f'DO16021_{self.verPdoSdo}_IN'
            type_moduleOutput = f'DO16021_{self.verPdoSdo}_OUT'
        else:
            type_moduleInput = 'ERROR********///'
            type_moduleOutput = 'ERROR********///'

        # код сбора STATE
        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_moduleInput} := {self.box}_{self.unit_pos}.Inputs;\n')
        codePLC.append(f'\t{type_moduleOutput} := {self.box}_{self.unit_pos}.Outputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0;\n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_moduleInput}.ModuleHeartbeat; \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_moduleInput}.ModuleHeartbeat;	// Модуль установлен в слоте\n\n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 0); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(
                f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(WORD_TO_LWORD({type_moduleOutput}.Discrets), 7); \n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_moduleInput}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def do_32_011(self):
        """
        функция генерации кода для
        R500-DO-32-011 [SM 32DO DC24V]
        :return: codePLC = list()
        """
        codePLC = list()

        if self.modul.startswith('R500-DO-32-011 [SM 32DO DC24V]'):
            type_moduleInput = f'DO32011_{self.verPdoSdo}_IN'
            type_moduleOutput = f'DO32011_{self.verPdoSdo}_OUT'
        else:
            type_moduleInput = 'ERROR********///'
            type_moduleOutput = 'ERROR********///'

        # код сбора STATE
        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_moduleInput} := {self.box}_{self.unit_pos}.Inputs;\n')
        codePLC.append(f'\t{type_moduleOutput} := {self.box}_{self.unit_pos}.Outputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0;\n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_moduleInput}.ModuleHeartbeat; \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_moduleInput}.ModuleHeartbeat;	// Модуль установлен в слоте\n\n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 0); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(
                f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(DWORD_TO_LWORD({type_moduleOutput}.Discrets), 7); \n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_moduleInput}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def do_32_012(self):
        """
        функция генерации кода для
        R500-DO-32-012 [SM 32DO DC24V]
        R500-DO-32-013 [SM 32DO DC24V]
        :return: codePLC = list()
        """
        codePLC = list()

        if self.modul.startswith('R500-DO-32-012 [SM 32DO DC24V]'):
            type_moduleInput = f'DO32012_{self.verPdoSdo}_IN'
            type_moduleOutput = f'DO32012_{self.verPdoSdo}_OUT'
        elif self.modul.startswith('R500-DO-32-013 [SM 32DO DC24V]'):
            type_moduleInput = f'DO32013_{self.verPdoSdo}_IN'
            type_moduleOutput = f'DO32013_{self.verPdoSdo}_OUT'
        else:
            type_moduleInput = 'ERROR********///'
            type_moduleOutput = 'ERROR********///'

        # код сбора STATE
        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_moduleInput} := {self.box}_{self.unit_pos}.Inputs;\n')
        codePLC.append(f'\t{type_moduleOutput} := {self.box}_{self.unit_pos}.Outputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0;\n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_moduleInput}.ModuleHeartbeat; \n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_moduleInput}.ModuleHeartbeat;	// Модуль установлен в слоте\n\n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(
                f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(
                f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_07 := {type_moduleInput}.PowerState.IntPowerState_0; // Внутреняя шина 1\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_08 := {type_moduleInput}.PowerState.IntPowerState_1; // Внутреняя шина 2\n')

        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(DWORD_TO_LWORD({type_moduleOutput}.Discrets), 9); \n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_moduleInput}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def do_32_041(self):
        """
        функция генерации кода для
        R500-DO-32-041 [SM 32DO DC24V]
        :return: codePLC = list()
        """
        codePLC = list()

        if self.modul.startswith('R500-DO-32-041 [SM 32DO DC24V]'):
            type_moduleInput = f'DO32041_{self.verPdoSdo}_IN'
            type_moduleOutput = f'DO32041_{self.verPdoSdo}_OUT'
        else:
            type_moduleInput = 'ERROR********///'
            type_moduleOutput = 'ERROR********///'

        # код сбора STATE
        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_moduleInput} := {self.box}_{self.unit_pos}.Inputs;\n')
        codePLC.append(f'\t{type_moduleOutput} := {self.box}_{self.unit_pos}.Outputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0;\n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_moduleInput}.ModuleHeartbeat; \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_moduleInput}.ModuleHeartbeat;	// Модуль установлен в слоте\n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 0); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := ({self.box}_{self.unit_pos}.ActiveBusNum = 1); // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_07 := ({type_moduleInput}.PowerState.IntPowerState_0; // Внутреняя шина 1\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_08 := ({type_moduleInput}.PowerState.IntPowerState_1; // Внутреняя шина 2\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_09 := ({type_moduleInput}.PowerState.ExtPowerState_0; // Внешняя шина 1\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_10 := ({type_moduleInput}.PowerState.ExtPowerState_1; // Внешняя шина 2\n')

        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(DWORD_TO_LWORD({type_moduleInput}.OpenLoadState), 11); // Обрыв \n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old :=  {type_moduleInput}.ModuleHeartbeat; \n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_LOCAL := STR_LWORD.LWORD_IMAGE;\n')
            codePLC.append(
                f'\t{self.name_db}.{self.box}_{self.unit_pos}_LOCAL2 := {type_moduleInput}.OvervoltageState OR SHL(DWORD_TO_LWORD({type_moduleInput}.OverloadState), 32); \n')
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_LOCAL3 := {type_moduleOutput}.Discrets; \n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE2 := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL2;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE3 := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL3;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE2 := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE2;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE3 := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE3;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE2 := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE2;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE3 := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE3;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE2 := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL2;\n')
            codePLC.append(f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE3 := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL3;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE; \n')
            codePLC.append(
                f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE2 := {type_moduleInput}.OvervoltageState OR SHL(DWORD_TO_LWORD({type_moduleInput}.OverloadState), 32); \n')
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE3 := {type_moduleOutput}.Discrets; \n\n')
        return codePLC

    def ds_32_011(self):
        """
        функция генерации кода для
        R500-DS-32-011 [SM 24DI 8DO DC24V]
        :return: codePLC = list()
        """
        codePLC = list()

        if self.modul.startswith('R500-DS-32-011 [SM 24DI 8DO DC24V]'):
            type_moduleInput = f'DS32011_{self.verPdoSdo}_IN'
            type_moduleOutput = f'DS32011_{self.verPdoSdo}_OUT'
        else:
            type_moduleInput = 'ERROR********///'
            type_moduleOutput = 'ERROR********///'

        # код сбора STATE
        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_moduleInput} := {self.box}_{self.unit_pos}.Inputs;\n')
        codePLC.append(f'\t{type_moduleOutput} := {self.box}_{self.unit_pos}.Outputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0;\n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_moduleInput}.ModuleHeartbeat; \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_moduleInput}.ModuleHeartbeat;	// Модуль установлен в слоте\n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(
                f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(
                f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(DWORD_TO_LWORD({type_moduleInput}.Byte_0_7), 7); \n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(DWORD_TO_LWORD({type_moduleInput}.Byte_8_15), 14); \n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(DWORD_TO_LWORD({type_moduleInput}.Byte_16_23), 21); \n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(DWORD_TO_LWORD({type_moduleOutput}.Discrets), 29); \n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_moduleInput}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def ds_32_012(self):
        """
        функция генерации кода для
        R500-DS-32-012 [SM 24DI 8DO DC24V]
        :return: codePLC = list()
        """
        codePLC = list()

        if self.modul.startswith('R500-DS-32-012 [SM 24DI 8DO DC24V]'):
            type_moduleInput = f'DS32012_{self.verPdoSdo}_IN'
            type_moduleOutput = f'DS32012_{self.verPdoSdo}_OUT'
        else:
            type_moduleInput = 'ERROR********///'
            type_moduleOutput = 'ERROR********///'

        # код сбора STATE
        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_moduleInput} := {self.box}_{self.unit_pos}.Inputs;\n')
        codePLC.append(f'\t{type_moduleOutput} := {self.box}_{self.unit_pos}.Outputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0;\n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_moduleInput}.ModuleHeartbeat; \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_moduleInput}.ModuleHeartbeat;	// Модуль установлен в слоте\n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 0); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := ({self.box}_{self.unit_pos}.ActiveBusNum = 1); // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_07 := ({self.box}_{self.unit_pos}.PowerState.IntPowerState_0; // Внутреняя шина 1\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_08 := ({self.box}_{self.unit_pos}.PowerState.IntPowerState_1; // Внутреняя шина 2\n')

        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(BYTE_TO_LWORD({type_moduleInput}.Byte_0_7), 9); \n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(BYTE_TO_LWORD({type_moduleInput}.Byte_8_15), 16); \n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(BYTE_TO_LWORD({type_moduleInput}.Byte_16_23), 24); \n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(BYTE_TO_LWORD({type_moduleOutput}.Discrets), 31); \n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_moduleInput}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def cp_02_021(self):
        """
        функция генерации кода для
        R500-CP-02-021 [2 ETHERNET]
        :return: codePLC = list()
        """
        codePLC = list()

        if self.modul.startswith('R500-CP-02-021 [2 ETHERNET]'):
            type_module = f'CP02021_{self.verPdoSdo}_IN'
        else:
            type_module = 'ERROR********/// '

        # код сбора STATE
        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_module} := {self.box}_{self.unit_pos}.Inputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0;\n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat; \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль установлен в слоте\n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 0); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := ({self.box}_{self.unit_pos}.ActiveBusNum = 1); // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(BYTE_TO_LWORD({type_module}.LinkStatus), 7); \n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_module}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def cp_04_011(self):
        """
        функция генерации кода для
        R500-CP-04-011 [4 RS485]
        :return: codePLC = list()
        """
        codePLC = list()

        if self.modul.startswith('R500-CP-04-011 [4 RS485]'):
            type_module = f'CP04011_{self.verPdoSdo}_IN'
        else:
            type_module = 'ERROR********/// '

        # код сбора STATE
        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_module} := {self.box}_{self.unit_pos}.Inputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0;\n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat; \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль установлен в слоте\n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 0); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := ({self.box}_{self.unit_pos}.ActiveBusNum = 1); // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_module}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def cp_06_111(self):
        """
        функция генерации кода для
        R500-CP-06-111 [6 ETHERNET]
        :return: codePLC = list()
        """
        codePLC = list()

        if self.modul.startswith('R500-CP-06-111 [6 ETHERNET]'):
            type_module = f'CP06111_{self.verPdoSdo}_IN'
        else:
            type_module = 'ERROR********/// '

        # код сбора STATE
        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_module} := {self.box}_{self.unit_pos}.Inputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0;\n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat; \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_module}.ModuleHeartbeat;	// Модуль установлен в слоте\n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 0); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := ({self.box}_{self.unit_pos}.ActiveBusNum = 1); // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(BYTE_TO_LWORD({type_module}.LinkStatus), 7); \n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(BYTE_TO_LWORD({type_module}.Mode), 13); \n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(BYTE_TO_LWORD({type_module}.PortStatus), 19); \n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_module}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

    def da_03_011(self):
        """
        функция генерации кода для
        R500-DA-03-011 [SM 3FI 1FO 6DI 6DO]
        R500-DA-03-021 [SM 3FI 1FO 6DI 6DO])
        :return: codePLC = list()
        """
        codePLC = list()

        if self.modul.startswith('R500-DA-03-011 [SM 3FI 1FO 6DI 6DO]'):
            type_moduleInput = f'DA03011_{self.verPdoSdo}_IN'
            type_moduleOutput = f'DA03011_{self.verPdoSdo}_OUT'
        elif self.modul.startswith('R500-DA-03-021 [SM 3FI 1FO 6DI 6DO]'):
            type_moduleInput = f'DA03021_{self.verPdoSdo}_IN'
            type_moduleOutput = f'DA03021_{self.verPdoSdo}_OUT'
        else:
            type_moduleInput = 'ERROR********/// '
            type_moduleOutput = 'ERROR********/// '

        match self.verPdoSdo:
            case '34':
                type_break = 'Break'
                type_do = 'Discrets'
            case _:
                type_break = 'ERROR********///'
                type_do = 'ERROR********///'

        # код сбора STATE
        codePLC.append(f'\t// {self.box}_{self.unit_pos} - {self.modul}\n\n')

        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexLock();\n')
        codePLC.append(f'\t{type_moduleInput} := {self.box}_{self.unit_pos}.Inputs;\n')
        codePLC.append(f'\t{type_moduleOutput} := {self.box}_{self.unit_pos}.Outputs;\n')
        # codePLC.append(f'\t{self.box}_{self.unit_pos}.SharedMutexUnlock();\n\n')

        codePLC.append(f'\tSTR_LWORD.LWORD_IMAGE := 0;\n\n')

        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_00 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_moduleInput}.ModuleHeartbeat; \n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_01 := {self.box}_{self.unit_pos}.HwError;	// Модуль неисправен\n')
        codePLC.append(
            f'\tSTR_LWORD._LWORD.BIT_02 := {self.box}_{self.unit_pos}_HeartBeat_old <> {type_moduleInput}.ModuleHeartbeat;	// Модуль установлен в слоте\n')
        if self.systemRes:
            if self.crateRes:  # Находимся на резервированном крейте
                codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := FALSE; // B2 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
                codePLC.append(f'\tELSE\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := FALSE; // B1 (зеленый)\n')
                codePLC.append(f'\tSTR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
                codePLC.append(f'\tEND_IF\n\n')
            else:
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_03 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_LEFT_MASTER; // B1 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_04 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_LEFT_SLAVE; // B1 (желтый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_05 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 1) AND*) PLC_RIGHT_MASTER; // B2 (зеленый)\n')
                codePLC.append(
                    f'\tSTR_LWORD._LWORD.BIT_06 := (*({self.box}_{self.unit_pos}.ActiveBusNum = 0) AND*) PLC_RIGHT_SLAVE; // B2 (желтый)\n')
        else:
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_03 := ({self.box}_{self.unit_pos}.ActiveBusNum = 0); // B1 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_04 := FALSE; // B1 (желтый)\n')
            codePLC.append(f'\tSTR_LWORD._LWORD.BIT_05 := ({self.box}_{self.unit_pos}.ActiveBusNum = 1); // B2 (зеленый)\n')
            codePLC.append(f'\t// STR_LWORD._LWORD.BIT_06 := FALSE; // B2 (желтый)\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_07 := ({type_moduleInput}.Freq1 > 0.0); // Наличие сигнала на CH1\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_08 := {type_moduleInput}.Invalid1; // Превышение частоты OV1\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_09 := ({type_moduleInput}.Freq2 > 0.0); // Наличие сигнала на CH2\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_10 := {type_moduleInput}.Invalid2; // Превышение частоты OV2\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_11 := ({type_moduleInput}.Freq3 > 0.0); // Наличие сигнала на CH3\n')
        codePLC.append(f'\tSTR_LWORD._LWORD.BIT_12 := {type_moduleInput}.Invalid3; // Превышение частоты OV3\n')

        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(DWORD_TO_LWORD({type_moduleInput}.DI), 13); \n\n')
        codePLC.append(
            f'\tSTR_LWORD.LWORD_IMAGE := STR_LWORD.LWORD_IMAGE OR SHL(DWORD_TO_LWORD({type_moduleOutput}.{type_do}), 19); \n\n')

        codePLC.append(f'\t{self.box}_{self.unit_pos}_HeartBeat_old := {type_moduleInput}.ModuleHeartbeat;\n\n')

        if self.crateRes:
            codePLC.append(f'\t{self.name_db}.{self.box}_LOCAL := STR_DWORD.DWORD_IMAGE;\n\n')

            codePLC.append(f'\t// Заполнение итоговых переменных, которые будут перервадаться на ВУ\n')
            codePLC.append(f'\tIF GLOBAL.IsDefaultPlc THEN\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(f'\tELSE\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_REMOTE;\n')
            codePLC.append(
                f'\t\t{self.name_db}.{self.box}_{self.unit_pos_res}_STATE := {self.name_db}.{self.box}_{self.unit_pos}_LOCAL;\n')
            codePLC.append(f'\tEND_IF\n\n')
        else:
            codePLC.append(f'\t{self.name_db}.{self.box}_{self.unit_pos}_STATE := STR_LWORD.LWORD_IMAGE;\n\n')
        return codePLC

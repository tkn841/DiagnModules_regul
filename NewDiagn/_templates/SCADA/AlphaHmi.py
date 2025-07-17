class AlphaHmi:
    def __init__(self):
        self.dispatch_table = {'R500-ST-02-012': '',
                               'R500-ST-02-022': '',

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

                               # 'R500-AI-16-012 [SM 16AI I]': '',

                               'R500-AO-08-011 [SM 8AO I]': self.ao_08_011,
                               'R500-AO-08-021 [SM 8AO I]': self.ao_08_011,
                               'R500-AO-08-031 [SM 8AO I]': self.ao_08_011,

                               'R500-AS-08-011 [SM 8AI I]': self.as_08_011,

                               'R500-DI-16-021 [SM 16DI AC220V]': self.di_16_021,

                               'R500-DI-16-031 [SM 16DI AC220V]': self.di_16_031,

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

                               'R500-DA-03-011 [SM 3FI 1FO 6DI 6DO] ENC': self.da_03_011,

                               'R500-EMPTY': self.empty}
        self.name = ''
        self.x = ''
        self.y = ''
        self.width = ''
        self.height = ''
        self.tagName = ''
        self.Box_UnitPos = ''
        self.TypeModule = ''
        self.Res = ''
        self.Bit = 0
        self.uuid = ''

    def extend_str(self):
        """
        Это общие строки для модулей ввода вывода
        """
        codeHmi = list()

        codeHmi.append(f'\t\t<designed target="X" value="{self.x}" ver="5"/>')
        codeHmi.append(f'\t\t<designed target="Y" value="{self.y}" ver="5"/>')
        codeHmi.append(f'\t\t<designed target="Rotation" value="0" ver="5"/>')
        codeHmi.append(f'\t\t<designed target="Width" value="{self.width}" ver="5"/>')
        codeHmi.append(f'\t\t<designed target="Height" value="{self.height}" ver="5"/>')
        codeHmi.append(f'\t\t<init target="tagName" ver="5" value="{self.tagName}"/>')
        codeHmi.append(f'\t\t<init target="_Box_UnitPos" ver="5" value="{self.Box_UnitPos}"/>')
        codeHmi.append(f'\t\t<init target="_TypeModule" ver="5" value="{self.TypeModule}"/>')
        codeHmi.append(f'\t</object>')
        return codeHmi

    def cpu(self):
        """
            функция генерации кода для
            R500-CU-00-061
            R500-CU-00-051
            R500-CU-00-161
        """
        codeHmi = list()

        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_CPU_R500" base-type-id="03b20986-a6b7-4e6c-b151-fe0adad85e24" ver="5" description="" cardinal="1">')
        codeHmi.append(f'\t\t<designed target="X" value="{self.x}" ver="5"/>')
        codeHmi.append(f'\t\t<designed target="Y" value="{self.y}" ver="5"/>')
        codeHmi.append(f'\t\t<designed target="Rotation" value="0" ver="5"/>')
        codeHmi.append(f'\t\t<designed target="Width" value="{self.width}" ver="5"/>')
        codeHmi.append(f'\t\t<designed target="Height" value="{self.height}" ver="5"/>')
        codeHmi.append(f'\t\t<init target="tagName" ver="5" value="{self.tagName}"/>')
        codeHmi.append(f'\t\t<init target="Box_UnitPos" ver="5" value="{self.Box_UnitPos}"/>')
        codeHmi.append(f'\t\t<init target="TypeModule" ver="5" value="{self.TypeModule}"/>')
        codeHmi.append(f'\t\t<init target="Res" ver="5" value="{self.Res}"/>')
        codeHmi.append(f'\t</object>')

        return codeHmi

    def ps(self):
        """
            функция генерации кода для
            R500-PP-00-011 [PS 75W]
        """
        codeHmi = list()

        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_PS" base-type-id="a79b6887-631f-4ef3-a973-06cd179e37d2" ver="5" description="" cardinal="1">')
        codeHmi.append(f'\t\t<designed target="X" value="{self.x}" ver="5"/>')
        codeHmi.append(f'\t\t<designed target="Y" value="{self.y}" ver="5"/>')
        codeHmi.append(f'\t\t<designed target="Rotation" value="0" ver="5"/>')
        codeHmi.append(f'\t\t<designed target="Width" value="{self.width}" ver="5"/>')
        codeHmi.append(f'\t\t<designed target="Height" value="{self.height}" ver="5"/>')
        codeHmi.append(f'\t\t<init target="tagName" ver="5" value="{self.tagName}"/>')
        codeHmi.append(f'\t\t<init target="_Box_UnitPos" ver="5" value="{self.Box_UnitPos}"/>')
        codeHmi.append(f'\t\t<init target="_Type" ver="5" value="{self.TypeModule}"/>')
        codeHmi.append(f'\t\t<init target="_Bit" ver="5" value="{self.Bit}"/>')
        codeHmi.append(f'\t</object>')

        return codeHmi

    def ai_08_021(self):
        """
            функция генерации кода для
            R500-AI-08-021 [SM 8AI I]
            R500-AI-08-041 [SM 8AI I]
            R500-AI-08-051 [SM 8AI I]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_AI_08_041" base-type-id="6dbd0052-235f-49ed-978a-2f691588f8cc" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def ai_08_022(self):
        """
            функция генерации кода для
            R500-AI-08-022 [SM 8AI I]
            R500-AI-08-042 [SM 8AI I]
            R500-AI-08-052 [SM 8AI I]
            R500-AI-08-242 [SM 8AI I]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_AI_08_042" base-type-id="1c32cc1f-c1c9-4e97-ad22-f127b13b60c1" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def ai_08_031(self):
        """
            функция генерации кода для
            R500-AI-08-031 [SM 8AI RTD/TC]
            R500-AI-08-131 [SM 8AI RTD/TC]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_AI_08_131" base-type-id="f5a82118-ff84-4a46-961d-f4cc5b1cba4b" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def ai_08_142(self):
        """
            функция генерации кода для
            R500-AI-08-142 [SM 8AI I]
            R500-AI-08-342 [SM 8AI I]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_AI_08_142" base-type-id="ba8f42ef-216e-4fed-843f-bc9da571400d" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def ai_16_011(self):
        """
            функция генерации кода для
            R500-AI-16-011 [SM 16AI I]
            R500-AI-16-081 [SM 16AI I]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_AI_16_011" base-type-id="d3663fee-e5ad-498d-9093-d013a4db54ba" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def ao_08_011(self):
        """
            функция генерации кода для
            R500-AO-08-011 [SM 8AO I]
            R500-AO-08-021 [SM 8AO I]
            R500-AO-08-031 [SM 8AO I]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_AO_08_011" base-type-id="81115869-be20-45b8-97ba-9745e81e67b7" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def as_08_011(self):
        """
            функция генерации кода для
            R500-AS-08-011 [SM 8AI I]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_AS_08_011" base-type-id="0f39db33-7763-4914-b302-5d2856cd6e30" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def cp_02_021(self):
        """
            функция генерации кода для
            R500-CP-02-021
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_CP_02_021" base-type-id="e93afbc3-b5d1-497f-87f3-991bd4849563" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def cp_04_011(self):
        """
            функция генерации кода для
            R500-CP-04-011 [4 RS485]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_CP_04_011" base-type-id="01a8ef09-dc86-409f-978f-b5e5c92b00ed" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def cp_06_111(self):
        """
            функция генерации кода для
            R500-CP-06-111 [6 ETHERNET]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_CP_06_111" base-type-id="81749a21-14ed-45ab-93e9-7ee992792069" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def da_03_011(self):
        """
            функция генерации кода для
            R500-DA-03-011 [SM 3FI 1FO 6DI 6DO] ENC
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_DA_03_011" base-type-id="6c09ffec-1f04-44d9-a07c-f04cc0313079" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def di_16_021(self):
        """
            функция генерации кода для
            R500-DI-16-021 [SM 16DI AC220V]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_DI_16_021" base-type-id="b2dc5c7b-b9fe-4112-9cb8-3e8d1dd669af" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def di_16_031(self):
        """
            функция генерации кода для
            R500-DI-16-031 [SM 16DI AC220V]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_DI_16_031" base-type-id="0652838a-9a09-4e0a-80ab-6d501c80b414" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def di_16_032(self):
        """
            функция генерации кода для
            R500-DI-16-032 [SM 16DI AC220V]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_DI_16_032" base-type-id="ab5b68e1-780b-4721-a3f0-3b0b081ef505" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def di_32_011(self):
        """
            функция генерации кода для
            R500-DI-32-011 [SM 32DI DC24V]
            R500-DI-32-012 [SM 32DI DC24V]
            R500-DI-32-013 [SM 32DI DC24V]
            R500-DI-32-111 [SM 32DI DC24V]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_DI_32_011" base-type-id="acc9108d-c484-4632-bdd8-015259b40542" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def do_16_021(self):
        """
            функция генерации кода для
            R500-DO-16-021 [SM 16DO AC220V]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_DO_16_021" base-type-id="b14832e0-a84a-4b8c-bb93-47d5171f6160" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def do_32_011(self):
        """
            функция генерации кода для
            R500-DO-32-011 [SM 32DO DC24V]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_DO_32_011" base-type-id="e1bc7037-0dad-432e-9d88-4bae02db94f1" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def do_32_012(self):
        """
            функция генерации кода для
            R500-DO-32-012 [SM 32DO DC24V]
            R500-DO-32-013 [SM 32DO DC24V]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_DO_32_012" base-type-id="4f02a40b-1a28-4353-afe7-63c8e62b54a2" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def do_32_041(self):
        """
            функция генерации кода для
            R500-DO-32-041 [SM 32DO DC24V]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_DO_32_041" base-type-id="46524b0e-8d80-48dd-8d13-13e4451f21cb" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def ds_32_011(self):
        """
            функция генерации кода для
            R500-DS-32-011 [SM 24DI 8DO DC24V]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_DS_32_011" base-type-id="532c4978-b74f-4927-974c-27702f0c8aad" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def ds_32_012(self):
        """
            функция генерации кода для
            R500-DS-32-012 [SM 24DI 8DO DC24V]
        """
        codeHmi = list()
        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_DS_32_012" base-type-id="f1aaae63-eac4-464c-802b-5ce7ee001b8c" ver="5" description="" cardinal="1">')
        codeHmi.extend(self.extend_str())
        return codeHmi

    def empty(self):
        """
            функция генерации кода для пустого модуля
        """
        codeHmi = list()

        codeHmi.append(f'\t<object access-modifier="private" name="{self.name}" display-name="{self.name}" uuid="{self.uuid}" base-type="TYPE_MODULE_R500_EMPTY" base-type-id="49fd4368-2ba3-4c9d-9605-c4ba610e46b9" ver="5" description="" cardinal="1">')
        codeHmi.append(f'\t\t<designed target="X" value="{self.x}" ver="5"/>')
        codeHmi.append(f'\t\t<designed target="Y" value="{self.y}" ver="5"/>')
        codeHmi.append(f'\t\t<designed target="Rotation" value="0" ver="5"/>')
        codeHmi.append(f'\t\t<designed target="Width" value="{self.width}" ver="5"/>')
        codeHmi.append(f'\t\t<designed target="Height" value="{self.height}" ver="5"/>')
        codeHmi.append(f'\t\t<init target="_TypeModule" ver="5" value="{self.TypeModule}"/>')
        codeHmi.append(f'\t\t<init target="_Box_UnitPos" ver="5" value="{self.Box_UnitPos}"/>')
        codeHmi.append(f'\t</object>')

        return codeHmi


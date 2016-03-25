# coding=utf-8
# Copyright (c) 2015 EMC Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from __future__ import unicode_literals

from unittest import TestCase

from hamcrest import assert_that, equal_to, instance_of, only_contains, raises

from storops.exception import UnityResourceNotFoundError
from storops.unity.enums import EnclosureTypeEnum, DiskTypeEnum
from storops.unity.resource.cifs_server import UnityCifsServerList
from storops.unity.resource.cifs_share import UnityCifsShareList, \
    UnityCifsShare
from storops.unity.resource.dns_server import UnityFileDnsServerList
from storops.unity.resource.filesystem import UnityFileSystemList
from storops.unity.resource.health import UnityHealth
from storops.unity.resource.interface import UnityFileInterfaceList
from storops.unity.resource.lun import UnityLunList
from storops.unity.resource.nas_server import UnityNasServer, \
    UnityNasServerList
from storops.unity.resource.nfs_server import UnityNfsServerList
from storops.unity.resource.nfs_share import UnityNfsShareList
from storops.unity.resource.pool import UnityPoolList
from storops.unity.resource.port import UnityIpPortList
from storops.unity.resource.sp import UnityStorageProcessor, \
    UnityStorageProcessorList
from storops.unity.resource.system import UnitySystemList, UnitySystem, \
    UnityDpeList, UnityDpe, UnityVirusChecker, UnityVirusCheckerList, \
    UnityBasicSystemInfo, UnityBasicSystemInfoList
from test.unity.rest_mock import t_rest, patch_rest, t_unity

__author__ = 'Cedric Zhuang'


class UnitySystemTest(TestCase):
    @patch_rest()
    def test_get_properties(self):
        system = UnitySystem(cli=t_rest())
        assert_that(system.existed, equal_to(True))
        assert_that(system.health, instance_of(UnityHealth))
        assert_that(system.name, equal_to('FNM00151200215'))
        assert_that(system.model, equal_to('Unity 500'))
        assert_that(system.serial_number, equal_to('FNM00151200215'))
        assert_that(system.internal_model, equal_to('OBERON 25 DRIVE CHASSIS'))
        assert_that(system.platform, equal_to('Oberon_DualSP'))
        assert_that(system.mac_address, equal_to('08:00:1B:FF:EA:CD'))
        assert_that(system.is_eula_accepted, equal_to(True))
        assert_that(system.is_upgrade_complete, equal_to(True))
        assert_that(system.is_auto_failback_enabled, equal_to(True))
        assert_that(system.current_power, equal_to(469))
        assert_that(system.avg_power, equal_to(474))

    @patch_rest()
    def test_init_by_ip(self):
        system = UnitySystem('10.244.223.66', 'admin', 'Password123!')
        assert_that(system.model, equal_to('Unity 500'))

    @patch_rest()
    def test_get_all(self):
        systems = UnitySystemList(cli=t_rest())
        assert_that(len(systems), equal_to(1))

    @patch_rest()
    def test_get_sp_all(self):
        unity = t_unity()
        sps = unity.get_sp()
        assert_that(sps, instance_of(UnityStorageProcessorList))
        assert_that(len(sps), equal_to(2))

    @patch_rest()
    def test_get_spa(self):
        unity = t_unity()
        sp = unity.get_sp('spa')
        assert_that(sp, instance_of(UnityStorageProcessor))

    @patch_rest()
    def test_get_sp_by_name(self):
        unity = t_unity()
        sp = unity.get_sp(name='SP A')
        assert_that(sp, instance_of(UnityStorageProcessor))
        assert_that(sp.id, equal_to('spa'))

    @patch_rest()
    def test_get_lun_list(self):
        unity = t_unity()
        lun_list = unity.get_lun()
        assert_that(lun_list, instance_of(UnityLunList))
        assert_that(len(lun_list), equal_to(5))

    @patch_rest()
    def test_get_pools(self):
        unity = t_unity()
        pools = unity.get_pool()
        assert_that(pools, instance_of(UnityPoolList))
        assert_that(len(pools), equal_to(2))

    @patch_rest()
    def test_get_nas_servers(self):
        unity = t_unity()
        nas_servers = unity.get_nas_server()
        assert_that(nas_servers, instance_of(UnityNasServerList))
        assert_that(len(nas_servers), equal_to(3))

    @patch_rest()
    def test_create_nas_server(self):
        unity = t_unity()
        sp = unity.get_sp(_id='spa')
        pool = unity.get_pool(_id='pool_1')
        nas_server = unity.create_nas_server('nas3', sp, pool)
        assert_that(nas_server.existed, equal_to(True))

    @patch_rest()
    def test_get_ip_ports(self):
        unity = t_unity()
        ip_ports = unity.get_ip_port()
        assert_that(ip_ports, instance_of(UnityIpPortList))
        assert_that(len(ip_ports), equal_to(8))

    @patch_rest()
    def test_get_file_interface(self):
        unity = t_unity()
        fi_list = unity.get_file_interface()
        assert_that(fi_list, instance_of(UnityFileInterfaceList))
        assert_that(len(fi_list), equal_to(1))

    @patch_rest()
    def test_get_cifs_server(self):
        unity = t_unity()
        cifs_servers = unity.get_cifs_server()
        assert_that(cifs_servers, instance_of(UnityCifsServerList))
        assert_that(len(cifs_servers), equal_to(1))

    @patch_rest()
    def test_get_nfs_server(self):
        unity = t_unity()
        nfs_servers = unity.get_nfs_server()
        assert_that(nfs_servers, instance_of(UnityNfsServerList))
        assert_that(len(nfs_servers), equal_to(1))

    @patch_rest()
    def test_get_dns_server(self):
        unity = t_unity()
        dns_servers = unity.get_dns_server()
        assert_that(dns_servers, instance_of(UnityFileDnsServerList))
        assert_that(len(dns_servers), equal_to(1))

    @patch_rest()
    def test_get_file_system(self):
        unity = t_unity()
        filesystems = unity.get_filesystem()
        assert_that(filesystems, instance_of(UnityFileSystemList))
        assert_that(len(filesystems), equal_to(3))

    @patch_rest()
    def test_get_cifs_share(self):
        unity = t_unity()
        shares = unity.get_cifs_share()
        assert_that(shares, instance_of(UnityCifsShareList))
        assert_that(len(shares), equal_to(1))

    @patch_rest()
    def test_get_nfs_share(self):
        unity = t_unity()
        shares = unity.get_nfs_share()
        assert_that(shares, instance_of(UnityNfsShareList))
        assert_that(len(shares), equal_to(2))

    @patch_rest()
    def test_system_info(self):
        unity = t_unity()
        assert_that(unity.info, instance_of(UnityBasicSystemInfo))

    @patch_rest()
    def test_system_get_cifs_share_by_name(self):
        unity = t_unity()
        cs = unity.get_cifs_share(name='cs1')
        assert_that(cs, instance_of(UnityCifsShare))
        assert_that(cs.name, equal_to('cs1'))

    @patch_rest()
    def test_system_get_fs_by_name_not_found(self):
        def f():
            unity = t_unity()
            unity.get_filesystem(name='not_found')

        assert_that(f, raises(UnityResourceNotFoundError,
                              'UnityFileSystem:not_found'))


class UnityDpeTest(TestCase):
    @patch_rest()
    def test_get_properties(self):
        dpe = UnityDpe('dpe', cli=t_rest())
        assert_that(dpe.existed, equal_to(True))
        assert_that(dpe.health, instance_of(UnityHealth))
        assert_that(dpe.needs_replacement, equal_to(False))
        assert_that(dpe.slot_number, equal_to(0))
        assert_that(dpe.name, equal_to('DPE'))
        assert_that(dpe.manufacturer, equal_to(''))
        assert_that(dpe.model, equal_to('OBERON 25 DRIVE CHASSIS'))
        assert_that(dpe.emc_part_number, equal_to('100-542-901-05'))
        assert_that(dpe.emc_serial_number, equal_to('CF2CV150500005'))
        assert_that(dpe.vendor_part_number, equal_to(''))
        assert_that(dpe.vendor_serial_number, equal_to(''))
        assert_that(dpe.bus_id, equal_to(0))
        assert_that(dpe.current_power, equal_to(429))
        assert_that(dpe.avg_power, equal_to(397))
        assert_that(dpe.max_power, equal_to(429))
        assert_that(dpe.current_temperature, equal_to(26))
        assert_that(dpe.avg_temperature, equal_to(26))
        assert_that(dpe.max_temperature, equal_to(26))
        assert_that(dpe.current_speed, equal_to(12000000000))
        assert_that(dpe.max_speed, equal_to(12000000000))
        assert_that(dpe.parent_system, instance_of(UnitySystem))
        assert_that(dpe.enclosure_type,
                    equal_to(EnclosureTypeEnum.MIRANDA_12G_SAS_DPE))
        assert_that(dpe.drive_types,
                    only_contains(DiskTypeEnum.SAS, DiskTypeEnum.SAS_FLASH_2))

    @patch_rest()
    def test_get_all(self):
        dpe_list = UnityDpeList(cli=t_rest())
        assert_that(len(dpe_list), equal_to(1))


class UnityVirusCheckerTest(TestCase):
    @patch_rest()
    def test_get_properties(self):
        checker = UnityVirusChecker('cava_2', cli=t_rest())
        assert_that(checker.existed, equal_to(True))
        assert_that(checker.nas_server, instance_of(UnityNasServer))
        assert_that(checker.is_enabled, equal_to(False))

    @patch_rest()
    def test_get_all(self):
        checker_list = UnityVirusCheckerList(cli=t_rest())
        assert_that(len(checker_list), equal_to(1))


class UnityBasicSystemInfoTest(TestCase):
    @patch_rest()
    def test_get_properties(self):
        info = UnityBasicSystemInfo(t_rest())
        assert_that(info.id, equal_to('0'))
        assert_that(info.existed, equal_to(True))
        assert_that(info.name, equal_to('FNM00151200215'))
        assert_that(info.software_version, equal_to('4.0.0'))
        assert_that(info.earliest_api_version, equal_to('4.0'))
        assert_that(info.model, equal_to('Unity 500'))
        assert_that(info.api_version, equal_to("4.0"))

    @patch_rest()
    def test_get_all(self):
        info_list = UnityBasicSystemInfoList(cli=t_rest())
        assert_that(len(info_list), equal_to(1))

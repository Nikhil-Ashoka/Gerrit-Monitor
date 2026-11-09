# 📊 Gerrit Activity Report
**Generated:** 2026-11-09 19:23:19 UTC
**Projects:** openbmc/webui-vue, openbmc/phosphor-debug-collector, openbmc/phosphor-inventory-manager, openbmc/phosphor-logging, openbmc/bmcweb
**Total Changes:** 106

---

## Project: [openbmc/webui-vue](https://gerrit.openbmc.org/q/project:openbmc/webui-vue)
**Period:** 2026-11-02 to 2026-11-09 (7 days)
**Changes:** 3


## 🔍 Open MRs (2)

### [Dumps: Show size in GB, MB or KB based on magnitude](https://gerrit.openbmc.org/c/96820)
- **Change #:** 96820
- **Author:** Vedangi Mittal
- **Updated:** 2026-11-06 06:48:02.000000000

### [Fail CI if npm rewrites package-lock.json](https://gerrit.openbmc.org/c/95592)
- **Change #:** 95592
- **Author:** Jason Westover
- **Updated:** 2026-11-03 07:03:31.000000000

## ❌ Abandoned MRs (1)

### [Add support for SimpleUpdate in firmware update](https://gerrit.openbmc.org/c/73116)
- **Change #:** 73116
- **Author:** Jackie14
- **Updated:** 2026-11-02 00:08:18.000000000

---

## Project: [openbmc/phosphor-debug-collector](https://gerrit.openbmc.org/q/project:openbmc/phosphor-debug-collector)
**Period:** 2026-11-02 to 2026-11-09 (7 days)
**Changes:** 26


## ✅ Merged MRs (2)

### [Fix typos using typos tool](https://gerrit.openbmc.org/c/96866)
- **Change #:** 96866
- **Author:** George Liu
- **Changes:** +1 / -1 lines
- **Updated:** 2026-11-06 06:20:45.000000000

### [bmc-dump: exit child with _exit() when execl fails](https://gerrit.openbmc.org/c/95363)
- **Change #:** 95363
- **Author:** Suvedha Balamurali
- **Changes:** +3 / -1 lines
- **Updated:** 2026-11-03 12:19:58.000000000

## 🔍 Open MRs (23)

### [dreport: prevent option and command injection via the elog path](https://gerrit.openbmc.org/c/96768)
- **Change #:** 96768
- **Author:** bvanassche
- **Updated:** 2026-11-09 14:11:44.000000000

### [bmc dump: validate the CreateDump FilePath](https://gerrit.openbmc.org/c/95728)
- **Change #:** 95728
- **Author:** Alex Chen
- **Updated:** 2026-11-09 12:08:09.000000000

### [core-monitor: dump core files left from before startup](https://gerrit.openbmc.org/c/96069)
- **Change #:** 96069
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-09 09:18:43.000000000

### [test: add BMC dump manager unit tests](https://gerrit.openbmc.org/c/96057)
- **Change #:** 96057
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-05 16:37:11.000000000

### [dump: share create dump helper between monitors](https://gerrit.openbmc.org/c/96151)
- **Change #:** 96151
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-05 09:30:27.000000000

### [dreport: preserve create_archive return status](https://gerrit.openbmc.org/c/95935)
- **Change #:** 95935
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-05 07:00:41.000000000

### [dump: free PLDM instance id when openPLDM fails](https://gerrit.openbmc.org/c/96498)
- **Change #:** 96498
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-05 05:20:03.000000000

### [test: add unit tests for ramoops manager](https://gerrit.openbmc.org/c/96088)
- **Change #:** 96088
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-05 05:16:08.000000000

### [bmc-dump: validate the FilePath parameter of CreateDump](https://gerrit.openbmc.org/c/96769)
- **Change #:** 96769
- **Author:** bvanassche
- **Updated:** 2026-11-05 00:26:18.000000000

### [bmc-dump: restrict the core and ramoops dump paths](https://gerrit.openbmc.org/c/96770)
- **Change #:** 96770
- **Author:** bvanassche
- **Updated:** 2026-11-05 00:26:15.000000000

### [test: add OpenPOWER dump manager notify tests](https://gerrit.openbmc.org/c/96380)
- **Change #:** 96380
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-04 12:14:09.000000000

### [dump: fix use after free when replacing a stale system dump entry](https://gerrit.openbmc.org/c/96390)
- **Change #:** 96390
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-04 10:51:56.000000000

### [test: add dump offload unit tests](https://gerrit.openbmc.org/c/96377)
- **Change #:** 96377
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-04 07:30:32.000000000

### [dump: remove unused cereal serialization from elog watch](https://gerrit.openbmc.org/c/96655)
- **Change #:** 96655
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-04 07:11:33.000000000

### [dreport: fix cleanup path after failed copies](https://gerrit.openbmc.org/c/95961)
- **Change #:** 95961
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-04 06:33:33.000000000

### [elog: migrate ID persistence to JSON and handle I/O errors](https://gerrit.openbmc.org/c/96691)
- **Change #:** 96691
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-04 06:24:31.000000000

### [bmc-dump: validate dump ids parsed from names](https://gerrit.openbmc.org/c/95395)
- **Change #:** 95395
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-04 04:51:33.000000000

### [dreport: exit with an error code when it fails](https://gerrit.openbmc.org/c/95732)
- **Change #:** 95732
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-04 04:50:29.000000000

### [watch: align the inotify buffer and bound-check events](https://gerrit.openbmc.org/c/96273)
- **Change #:** 96273
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-03 16:18:39.000000000

### [pldm: validate EID value read from file](https://gerrit.openbmc.org/c/96530)
- **Change #:** 96530
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-03 14:37:23.000000000

### [dump: remove unused bus in system dump createDump](https://gerrit.openbmc.org/c/96516)
- **Change #:** 96516
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-03 13:58:50.000000000

### [dreport: harden check_size error handling](https://gerrit.openbmc.org/c/96004)
- **Change #:** 96004
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-03 13:02:35.000000000

### [dreport: enforce size limit across plugin subshells](https://gerrit.openbmc.org/c/96654)
- **Change #:** 96654
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-02 12:38:00.000000000

## ❌ Abandoned MRs (1)

### [dump: don't abort on elog id list read or write errors](https://gerrit.openbmc.org/c/96284)
- **Change #:** 96284
- **Author:** Suvedha Balamurali
- **Updated:** 2026-11-04 06:51:02.000000000

---

## Project: [openbmc/phosphor-inventory-manager](https://gerrit.openbmc.org/q/project:openbmc/phosphor-inventory-manager)
**Period:** 2026-11-02 to 2026-11-09 (7 days)
**Changes:** 1


## ✅ Merged MRs (1)

### [Fix typos using typos tool](https://gerrit.openbmc.org/c/96882)
- **Change #:** 96882
- **Author:** George Liu
- **Changes:** +2 / -2 lines
- **Updated:** 2026-11-06 22:13:47.000000000

---

## Project: [openbmc/phosphor-logging](https://gerrit.openbmc.org/q/project:openbmc/phosphor-logging)
**Period:** 2026-11-02 to 2026-11-09 (7 days)
**Changes:** 17


## ✅ Merged MRs (9)

### [Fix typos using typos tool](https://gerrit.openbmc.org/c/96885)
- **Change #:** 96885
- **Author:** George Liu
- **Changes:** +6 / -6 lines
- **Updated:** 2026-11-06 22:27:07.000000000

### [lg2: Add is_log_flag type trait](https://gerrit.openbmc.org/c/96667)
- **Change #:** 96667
- **Author:** bvanassche
- **Changes:** +57 / -0 lines
- **Updated:** 2026-11-04 23:15:54.000000000

### [lg2: Return header_str by value from header_str_conversion](https://gerrit.openbmc.org/c/95447)
- **Change #:** 95447
- **Author:** bvanassche
- **Changes:** +6 / -1 lines
- **Updated:** 2026-11-03 23:43:22.000000000

### [lg2: Fix static initialization order problem in lg2_logger.cpp](https://gerrit.openbmc.org/c/95446)
- **Change #:** 95446
- **Author:** bvanassche
- **Changes:** +71 / -7 lines
- **Updated:** 2026-11-03 23:43:22.000000000

### [lg2: Do not read past the end of string_view values](https://gerrit.openbmc.org/c/95445)
- **Change #:** 95445
- **Author:** bvanassche
- **Changes:** +31 / -4 lines
- **Updated:** 2026-11-03 23:43:22.000000000

### [lg2: Constrain header_str constructor to string literal arrays](https://gerrit.openbmc.org/c/95443)
- **Change #:** 95443
- **Author:** bvanassche
- **Changes:** +18 / -3 lines
- **Updated:** 2026-11-03 23:43:22.000000000

### [test: Verify that misuse of the lg2 API fails to compile](https://gerrit.openbmc.org/c/95442)
- **Change #:** 95442
- **Author:** bvanassche
- **Changes:** +52 / -0 lines
- **Updated:** 2026-11-03 23:43:22.000000000

### [meson: Honor prefix when installing systemd service files](https://gerrit.openbmc.org/c/96193)
- **Change #:** 96193
- **Author:** bvanassche
- **Changes:** +1 / -0 lines
- **Updated:** 2026-11-03 15:53:41.000000000

### [cper: Disable cper-processor by default](https://gerrit.openbmc.org/c/96361)
- **Change #:** 96361
- **Author:** bvanassche
- **Changes:** +1 / -0 lines
- **Updated:** 2026-11-03 14:21:50.000000000

## 🔍 Open MRs (6)

### [log_manager: remove cleared entry files in the background](https://gerrit.openbmc.org/c/96896)
- **Change #:** 96896
- **Author:** aasaitha0219
- **Updated:** 2026-11-09 06:43:40.000000000

### [log_manager: stage artifacts too, keep kept-entry files safe](https://gerrit.openbmc.org/c/96897)
- **Change #:** 96897
- **Author:** aasaitha0219
- **Updated:** 2026-11-07 00:37:12.000000000

### [phal-next: Changes to support phal_next (#136)](https://gerrit.openbmc.org/c/96904)
- **Change #:** 96904
- **Author:** serasusan
- **Updated:** 2026-11-06 19:04:09.000000000

### [PEL: enable guard and deconfigure](https://gerrit.openbmc.org/c/96815)
- **Change #:** 96815
- **Author:** serasusan
- **Updated:** 2026-11-06 18:29:44.000000000

### [lg2: Document and test string literal values](https://gerrit.openbmc.org/c/96668)
- **Change #:** 96668
- **Author:** bvanassche
- **Updated:** 2026-11-04 23:05:36.000000000

### [lg2: Do not convert string literal values to header_str](https://gerrit.openbmc.org/c/95126)
- **Change #:** 95126
- **Author:** bvanassche
- **Updated:** 2026-11-04 22:53:10.000000000

## 🚧 Work In Progress (1)

### [PEL: Add GPIO SRCS](https://gerrit.openbmc.org/c/96750)
- **Change #:** 96750
- **Author:** Brendan Singer
- **Updated:** 2026-11-06 21:57:42.000000000

## ❌ Abandoned MRs (1)

### [cper: default disable CPER processing](https://gerrit.openbmc.org/c/96677)
- **Change #:** 96677
- **Author:** Patrick Williams
- **Updated:** 2026-11-03 05:08:32.000000000

---

## Project: [openbmc/bmcweb](https://gerrit.openbmc.org/q/project:openbmc/bmcweb)
**Period:** 2026-11-02 to 2026-11-09 (7 days)
**Changes:** 59


## ✅ Merged MRs (4)

### [OWNERS: add myself as a reviewer](https://gerrit.openbmc.org/c/96703)
- **Change #:** 96703
- **Author:** Oliver Brewka
- **Changes:** +1 / -0 lines
- **Updated:** 2026-11-06 17:53:59.000000000

### [test: add unit tests for Cable handlers](https://gerrit.openbmc.org/c/95845)
- **Change #:** 95845
- **Author:** JY-Voon
- **Changes:** +151 / -0 lines
- **Updated:** 2026-11-06 16:37:14.000000000

### [Redfish: Include Details in VirtualMedia 404s](https://gerrit.openbmc.org/c/95386)
- **Change #:** 95386
- **Author:** Joel Pullokaran Jesin
- **Changes:** +1 / -2 lines
- **Updated:** 2026-11-04 06:00:26.000000000

### [Uniform unit test file naming](https://gerrit.openbmc.org/c/95167)
- **Change #:** 95167
- **Author:** Oliver Brewka
- **Changes:** +9 / -13 lines
- **Updated:** 2026-11-02 21:04:00.000000000

## 🔍 Open MRs (43)

### [test: add unit tests for PCIeSlots handlers](https://gerrit.openbmc.org/c/95847)
- **Change #:** 95847
- **Author:** JY-Voon
- **Updated:** 2026-11-09 17:24:50.000000000

### [Match D-Bus errors by errName instead of string literals](https://gerrit.openbmc.org/c/96857)
- **Change #:** 96857
- **Author:** Patrick Williams
- **Updated:** 2026-11-09 16:38:27.000000000

### [Align VM websocket buffers with NBD cap](https://gerrit.openbmc.org/c/93785)
- **Change #:** 93785
- **Author:** tsankowx
- **Updated:** 2026-11-09 13:46:06.000000000

### [port: add SFP and link properties](https://gerrit.openbmc.org/c/96676)
- **Change #:** 96676
- **Author:** andychung113
- **Updated:** 2026-11-09 10:04:29.000000000

### [port: add NIC, PCIe link and transceiver metrics](https://gerrit.openbmc.org/c/96675)
- **Change #:** 96675
- **Author:** andychung113
- **Updated:** 2026-11-09 10:04:04.000000000

### [control: add ResetToDefaults action for Controls](https://gerrit.openbmc.org/c/89357)
- **Change #:** 89357
- **Author:** JY-Voon
- **Updated:** 2026-11-09 10:02:08.000000000

### [Return 404 for OperatingConfigs of unknown CPU](https://gerrit.openbmc.org/c/96924)
- **Change #:** 96924
- **Author:** JY-Voon
- **Updated:** 2026-11-09 07:36:57.000000000

### [test: add unit tests for OperatingConfig handlers](https://gerrit.openbmc.org/c/95842)
- **Change #:** 95842
- **Author:** JY-Voon
- **Updated:** 2026-11-09 07:00:47.000000000

### [control: add Chassis Controls for ClockLimit](https://gerrit.openbmc.org/c/87387)
- **Change #:** 87387
- **Author:** Ender
- **Updated:** 2026-11-09 04:39:19.000000000

### [processor: support PATCH for clock speed](https://gerrit.openbmc.org/c/90503)
- **Change #:** 90503
- **Author:** Ender
- **Updated:** 2026-11-09 04:39:16.000000000

### [processor: add DataSourceUri to clock range](https://gerrit.openbmc.org/c/88783)
- **Change #:** 88783
- **Author:** Ender
- **Updated:** 2026-11-09 04:39:14.000000000

### [processor: add clock speed support](https://gerrit.openbmc.org/c/87279)
- **Change #:** 87279
- **Author:** Ender
- **Updated:** 2026-11-09 03:51:13.000000000

### [routing: authorize before moving upgrade socket](https://gerrit.openbmc.org/c/96575)
- **Change #:** 96575
- **Author:** Alex Chen
- **Updated:** 2026-11-07 01:45:04.000000000

### [http2: apply logged-out body limit before auth](https://gerrit.openbmc.org/c/96474)
- **Change #:** 96474
- **Author:** Alex Chen
- **Updated:** 2026-11-07 01:20:51.000000000

### [http_body: enforce accumulated body limit](https://gerrit.openbmc.org/c/96200)
- **Change #:** 96200
- **Author:** Alex Chen
- **Updated:** 2026-11-07 01:04:58.000000000

### [NetworkProtocol: report SSH for OpenSSH too](https://gerrit.openbmc.org/c/96917)
- **Change #:** 96917
- **Author:** aasaitha0219
- **Updated:** 2026-11-07 00:47:13.000000000

### [telemetry: match dot-delimited children in InvalidArgs handling](https://gerrit.openbmc.org/c/96908)
- **Change #:** 96908
- **Author:** Patrick Williams
- **Updated:** 2026-11-07 00:09:10.000000000

### [Extract PowerSupply HEAD callback](https://gerrit.openbmc.org/c/96890)
- **Change #:** 96890
- **Author:** Joel Pullokaran Jesin
- **Updated:** 2026-11-06 23:07:50.000000000

### [telemetry: handle sdbusplus generated events](https://gerrit.openbmc.org/c/96724)
- **Change #:** 96724
- **Author:** Patrick Williams
- **Updated:** 2026-11-06 20:57:51.000000000

### [Multi-host support for Managers](https://gerrit.openbmc.org/c/85599)
- **Change #:** 85599
- **Author:** Oliver Brewka
- **Updated:** 2026-11-06 17:57:08.000000000

### [UpdateService: support ForceUpdate in multipart push](https://gerrit.openbmc.org/c/92596)
- **Change #:** 92596
- **Author:** DHRUV RATHI
- **Updated:** 2026-11-06 16:22:10.000000000

### [test: add unit tests for SubProcessor handlers](https://gerrit.openbmc.org/c/95841)
- **Change #:** 95841
- **Author:** JY-Voon
- **Updated:** 2026-11-06 14:43:43.000000000

### [Multi-host Storage Item Get](https://gerrit.openbmc.org/c/95026)
- **Change #:** 95026
- **Author:** bencenagy-9esec
- **Updated:** 2026-11-06 09:54:59.000000000

### [Multi-host Storage Controller Collection Get](https://gerrit.openbmc.org/c/95027)
- **Change #:** 95027
- **Author:** bencenagy-9esec
- **Updated:** 2026-11-06 09:21:32.000000000

### [Storage: Map Drive encryption from LockedStatus](https://gerrit.openbmc.org/c/96491)
- **Change #:** 96491
- **Author:** Joel Pullokaran Jesin
- **Updated:** 2026-11-06 08:57:49.000000000

### [trigger: add unit tests for enum conversion](https://gerrit.openbmc.org/c/94569)
- **Change #:** 94569
- **Author:** Eric Liu
- **Updated:** 2026-11-06 07:02:02.000000000

### [Redfish: Reuse mapper results for Switch GETs](https://gerrit.openbmc.org/c/94729)
- **Change #:** 94729
- **Author:** Joel Pullokaran Jesin
- **Updated:** 2026-11-06 06:46:58.000000000

### [pcie: add PCIeFunction BusNumber](https://gerrit.openbmc.org/c/96674)
- **Change #:** 96674
- **Author:** andychung113
- **Updated:** 2026-11-06 01:47:35.000000000

### [Fix typos using typos tool](https://gerrit.openbmc.org/c/96789)
- **Change #:** 96789
- **Author:** George Liu
- **Updated:** 2026-11-05 19:16:19.000000000

### [Add null and empty guards before dereference](https://gerrit.openbmc.org/c/96275)
- **Change #:** 96275
- **Author:** Ishita Agarwal
- **Updated:** 2026-11-05 19:12:14.000000000

### [task: Add unit tests for task eviction](https://gerrit.openbmc.org/c/94586)
- **Change #:** 94586
- **Author:** shivrajnt
- **Updated:** 2026-11-05 10:44:07.000000000

### [http: address clang-tidy warnings on ARM32](https://gerrit.openbmc.org/c/96719)
- **Change #:** 96719
- **Author:** vijays51
- **Updated:** 2026-11-05 01:20:17.000000000

### [led: add unit tests](https://gerrit.openbmc.org/c/94531)
- **Change #:** 94531
- **Author:** Eric Liu
- **Updated:** 2026-11-04 11:44:02.000000000

### [parse_registries: add additional registries](https://gerrit.openbmc.org/c/94454)
- **Change #:** 94454
- **Author:** Patrick Williams
- **Updated:** 2026-11-04 08:13:05.000000000

### [Fix int overflow, uninit, and SSL error handling](https://gerrit.openbmc.org/c/96274)
- **Change #:** 96274
- **Author:** Ishita Agarwal
- **Updated:** 2026-11-03 09:47:44.000000000

### [error_messages: take string_view value arguments](https://gerrit.openbmc.org/c/95853)
- **Change #:** 95853
- **Author:** Dhruv Goyal
- **Updated:** 2026-11-02 23:42:50.000000000

### [chassis: Use association for Chassis.Reset Action](https://gerrit.openbmc.org/c/96296)
- **Change #:** 96296
- **Author:** Janet Adkins
- **Updated:** 2026-11-02 21:26:21.000000000

### [led: Check for an empty LED group service map](https://gerrit.openbmc.org/c/96495)
- **Change #:** 96495
- **Author:** Eric Liu
- **Updated:** 2026-11-02 20:07:13.000000000

### [Add Redfish ComponentIntegrity resource](https://gerrit.openbmc.org/c/88828)
- **Change #:** 88828
- **Author:** garybeihl
- **Updated:** 2026-11-02 15:48:48.000000000

### [Fix system dump task completion Location](https://gerrit.openbmc.org/c/96388)
- **Change #:** 96388
- **Author:** shivrajnt
- **Updated:** 2026-11-02 14:53:33.000000000

### [EventService: fix MessageIds validation](https://gerrit.openbmc.org/c/96204)
- **Change #:** 96204
- **Author:** shivrajnt
- **Updated:** 2026-11-02 09:09:41.000000000

### [rhi: Support Redfish Hostinterface schema](https://gerrit.openbmc.org/c/82853)
- **Change #:** 82853
- **Author:** Thu Nguyen
- **Updated:** 2026-11-02 05:53:05.000000000

### [fix(session): return 204 on SessionService PATCH](https://gerrit.openbmc.org/c/96496)
- **Change #:** 96496
- **Author:** kennyliu9535
- **Updated:** 2026-11-02 02:07:11.000000000

## 🚧 Work In Progress (8)

### [HostLogger rework](https://gerrit.openbmc.org/c/78786)
- **Change #:** 78786
- **Author:** Oliver Brewka
- **Updated:** 2026-11-09 17:27:19.000000000

### [Storage Drives Collection fix for the chassis](https://gerrit.openbmc.org/c/93422)
- **Change #:** 93422
- **Author:** bencenagy-9esec
- **Updated:** 2026-11-06 10:11:16.000000000

### [Storage Drive Items fix for the chassis](https://gerrit.openbmc.org/c/93509)
- **Change #:** 93509
- **Author:** bencenagy-9esec
- **Updated:** 2026-11-06 09:58:15.000000000

### [Storage Drives link fix for the chassis](https://gerrit.openbmc.org/c/93414)
- **Change #:** 93414
- **Author:** bencenagy-9esec
- **Updated:** 2026-11-06 09:55:27.000000000

### [Storage: Unpack Drive properties by type](https://gerrit.openbmc.org/c/95783)
- **Change #:** 95783
- **Author:** Joel Pullokaran Jesin
- **Updated:** 2026-11-05 05:55:47.000000000

### [Redfish: Reject malformed pagination values](https://gerrit.openbmc.org/c/96735)
- **Change #:** 96735
- **Author:** Joel Pullokaran Jesin
- **Updated:** 2026-11-05 04:54:26.000000000

### [Minimize usage of Inventory.Decorator.ManagedHost](https://gerrit.openbmc.org/c/87160)
- **Change #:** 87160
- **Author:** Oliver Brewka
- **Updated:** 2026-11-04 19:01:26.000000000

### [parse_registries: Add Device message registry](https://gerrit.openbmc.org/c/96399)
- **Change #:** 96399
- **Author:** Eric Yang
- **Updated:** 2026-11-02 06:42:11.000000000

## ❌ Abandoned MRs (4)

### [Multi-host Systems Storage Drives Get](https://gerrit.openbmc.org/c/95028)
- **Change #:** 95028
- **Author:** bencenagy-9esec
- **Updated:** 2026-11-06 09:06:42.000000000

### [bmcweb: Validate SPDM action nonce](https://gerrit.openbmc.org/c/95259)
- **Change #:** 95259
- **Author:** Florian Sorin
- **Updated:** 2026-11-04 14:51:30.000000000

### [bmcweb: Omit empty SPDM action public key](https://gerrit.openbmc.org/c/95260)
- **Change #:** 95260
- **Author:** Florian Sorin
- **Updated:** 2026-11-04 14:50:30.000000000

### [add null and empty-container guards before dereference](https://gerrit.openbmc.org/c/96289)
- **Change #:** 96289
- **Author:** Ishita Agarwal
- **Updated:** 2026-11-03 09:47:58.000000000

---

*Report generated by Gerrit Activity Monitor*
*Gerrit Instance: https://gerrit.openbmc.org*

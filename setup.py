#!/usr/bin/env python3

from opencore.build import OpenCoreBuild


if __name__ == '__main__':
    build = OpenCoreBuild('Volumes/EFI')
    build.kexts = [
        {
            'project': 'Lilu',
            'repo': 'acidanthera',
            'version': '1.5.6'
        },
        {
            'project': 'FeatureUnlock',
            'repo': 'acidanthera',
            'version': '1.0.3'
        },
        {
            'project': 'WhateverGreen',
            'repo': 'acidanthera',
            'version': '1.5.4'
        }
    ]
    build.patches = [
        {
            'Base': '_early_random',
            'Find': build.unhexlify('00 74 23 48 8B'),
            'Identifier': 'kernel',
            'Limit': 800,
            'MinKernel': '20.4.0',
            'Replace': build.unhexlify('00 EB 23 48 8B')
        },
        {
            'Base': '_register_and_init_prng',
            'Find': build.unhexlify('BA 48 01 00 00 31 F6'),
            'Identifier': 'kernel',
            'Limit': 256,
            'MinKernel': '20.4.0',
            'Replace': build.unhexlify('BA 48 01 00 00 EB 05')
        }
    ]
    build.write_tree()

    settings = {
        'DeviceProperties': {
            'Add': {
                'PciRoot(0x0)/Pci(0x3,0x0)/Pci(0x0,0x0)': {
                    'agdpmod': build.unhexlify('70 69 6B 65 72 61 00'),
                    'rebuild-device-tree': build.unhexlify('00'),
                    'shikigva': build.unhexlify('50'),
                    'unfairgva': build.unhexlify('01 00 00 00')
                },
                'PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)': {
                    'built-in': build.unhexlify('00')
                }
            }
        },
        'Kernel': {
            'Quirks': {
                'DisableLinkeditJettison': True,
                'SetApfsTrimTimeout': 9999999
            },
            'Scheme': {
                'KernelArch': 'x86_64'
            }
        },
        'Misc': {
            'Boot': {
                'ConsoleAttributes': 15,
                'HideAuxiliary': True,
                'PollAppleHotKeys': True,
                'PickerMode': 'External',
                'ShowPicker': True,
                'Timeout': 10
            },
            'Security': {
                'AllowSetDefault': True,
                'BlacklistAppleUpdate': True,
                'ExposeSensitiveData': 3,
                'ScanPolicy': 0,
                'Vault': 'Optional'
            }
        },
        'NVRAM': {
            'Add': {
                '4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14': {
                    'DefaultBackgroundColor': build.unhexlify('00 00 00 00'),
                    'UIScale': build.unhexlify('02')
                }
            },
            'Delete': {
                '4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14': [
                    'DefaultBackgroundColor',
                    'UIScale'
                ]
            }
        },
        'PlatformInfo': {
            'SMBIOS': {
                'BIOSVersion': '9999.0.0.0.0',
                'BoardProduct': 'Mac-7BA5B2D9E42DDD94'
            },
            'PlatformNVRAM': {
                'FirmwareFeatures': build.unhexlify('03 54 0c c0 08 00 00 00'),
                'FirmwareFeaturesMask': build.unhexlify('3f ff 1f ff 08 00 00 00'),
            },
            'UpdateNVRAM': True,
            'UpdateSMBIOS': True
        },
        'UEFI': {
            'AppleInput': {
                'AppleEvent': 'Builtin'
            },
            'ConnectDrivers': True,
            'Drivers': [
                {
                    'Arguments': '',
                    'Comment': '',
                    'Enabled': True,
                    'Path': 'OpenCanopy.efi'
                },
                {
                    'Arguments': '',
                    'Comment': '',
                    'Enabled': True,
                    'Path': 'OpenRuntime.efi'
                },
                {
                    'Arguments': '',
                    'Comment': '',
                    'Enabled': True,
                    'Path': 'ExFatDxeLegacy.efi'
                }
            ],
            'Output': {
                'ProvideConsoleGop': True,
                'Resolution': 'Max'
            },
            'ProtocolOverrides': {
                'AppleBootPolicy': True,
                'AppleUserInterfaceTheme': True
            },
            'Quirks': {
                'RequestBootVarRouting': True
            }
        }
    }
    build.write_plist(settings)
    build.run_misc_tasks()

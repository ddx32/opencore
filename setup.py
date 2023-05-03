#!/usr/bin/env python3

from opencore.build import OpenCoreBuild


if __name__ == '__main__':
    build = OpenCoreBuild('Volumes/EFI')
    build.kexts = [
        {
            'project': 'ASPP-Override',
            'properties': {
                'ExecutablePath': '',
                'MinKernel': '21.4.0'
            },
            'repo': 'dortania',
            'version': '1.0.1'
        },
        {
            'project': 'Lilu',
            'repo': 'acidanthera',
            'version': '1.6.4'
        },
        {
            'project': 'FeatureUnlock',
            'repo': 'acidanthera',
            'version': '1.1.4'
        },
        {
            'project': 'WhateverGreen',
            'repo': 'acidanthera',
            'version': '1.6.4'
        },
        {
            'project': 'NoAVXFSCompressionTypeZlib',
            'properties': {
                'MinKernel': '21.5.0'
            },
            'repo': 'dortania',
            'version': '12.3.1'
        }
    ]
    build.write_tree()

    settings = {
        'DeviceProperties': {
            'Add': {
                'PciRoot(0x0)/Pci(0x3,0x0)/Pci(0x0,0x0)': {
                    'rebuild-device-tree': 0,
                    'unfairgva': 1
                }
            }
        },
        'Kernel': {
            'Quirks': {
                'DisableLinkeditJettison': True,
                'SetApfsTrimTimeout': 0,
                'ThirdPartyDrives': True
            }
        },
        'Misc': {
            'Boot': {
                'HideAuxiliary': True,
                'LauncherOption': 'Full',
                'PollAppleHotKeys': True,
                'PickerMode': 'External',
                'PickerVariant': 'Default',
                'ShowPicker': True,
                'Timeout': 15
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
                '7C436110-AB2A-4BBB-A880-FE41995C9F82': {
                    'boot-args': '-no_compat_check'
                }
            },
            'Delete': {
                '7C436110-AB2A-4BBB-A880-FE41995C9F82': ['boot-args']
            }
        },
        'PlatformInfo': {
            'DataHub': {
                'BoardProduct': 'Mac-27AD2F918AE68F61'
            },
            'PlatformNVRAM': {
                'FirmwareFeatures': build.unhexlify('03 54 0C C0 08 00 00 00'),
                'FirmwareFeaturesMask': build.unhexlify('3F FF 1F FF 08 00 00 00')
            },
            'SMBIOS': {
                'BoardProduct': 'Mac-27AD2F918AE68F61'
            },
            'UpdateNVRAM': True,
            'UpdateSMBIOS': True,
            'UpdateDataHub': True
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
                    'LoadEarly': False,
                    'Path': 'OpenCanopy.efi'
                },
                {
                    'Arguments': '',
                    'Comment': '',
                    'Enabled': True,
                    'LoadEarly': False,
                    'Path': 'OpenRuntime.efi'
                },
                {
                    'Arguments': '',
                    'Comment': '',
                    'Enabled': True,
                    'LoadEarly': False,
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

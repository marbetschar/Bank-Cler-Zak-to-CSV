# Bank Cler Zak to CSV

Export Bank Cler Zak transactions to CSV format

- [Usage](#Usage)
- [Development](#Development)
- [Troubleshooting](#Troubleshooting)

## Usage

### Prerequisites

Since 2024, Zak limits requests to their API to registered devices. That said, for this export to work,
you need to register this export with them by requesting an additional security code:

https://www.cler.ch/de/info/zak/zak-onboarding/login-hilfe/aktivierungscode-bestellen

### Export to CSV

To export all your Bank Cler Zak transactions, run the following command on your machine:

```shell
# You can find the app_version from the Google Play store page from your Android device.
# Its a concatenated string containing the version and build number of the Bank Cler Zak
# app in the following format: 3.54.0.12168
python app.py --username=<zak-username> --password=<zak-password> --app-version=<app_version>
```

This will create a `Zak.csv` file in the project root containing all your transactions from Zak.

## Development

### Prerequisites

Make sure you have the following tools installed:

**Computer:**

- adb
- unzip
- [APKEditor](https://github.com/REAndroid/APKEditor)
- [apk-mitm](https://github.com/niklashigi/apk-mitm)
- [mitmproxy](https://mitmproxy.org/)

**Android:**

- [SAI](https://f-droid.org/en/packages/com.aefyr.sai.fdroid/)

### Export APKS

Install [SAI](https://github.com/Aefyr/SAI) on your Android phone next to the Bank Cler Zak app.
Use it to export the Zak app into a splitted *.apks file and store it your Android's Download folder.

### Transfer APKS to Computer

Then, connect your phone with ADB to your computer and copy the APKS file:

```bash
adb pull storage/emulated/0/Download/*.apks ~/Downloads/BankClerZak.apks
```

### Merge the splitted APKS into Standalone APK

Merging is required because the `apktool` (which is used by `apk-mitm` under the hood) has trouble to correctly
decode and encode resources of Splitted APKS files - even though it doesn't throw any error, the app is likely to crash with some
sort of NullPointerException because it is no longer able to find certain resources.

```bash
unzip BankClerZak.apks -d BankClerZak
java -jar APKEditor.jar m -i BankClerZak
00.000 I: [MERGE] Using: APKEditor version 1.4.1, ARSCLib version 1.3.5
      -i = BankClerZak           
      -o = BankClerZak_merged.apk
...                                                                                                                                                                                            
04.621 I: [MERGE] Saved to: BankClerZak_merged.apk
```

### Patch Standalone APK

Patching essentially enables trust for certificates installed by the user on the Android system. This is what actually
allows us to use a proxy.

```bash
apk-mitm BankClerZak_merged.apk
```

### Install Patched Standalone APK on Android

```bash
adb install BankClerZak_merged-patched.apk
```

### Test everything is working

On your Android device, make sure you are connecting to the internet through mitmproxy.
Then start the Bank Cler Zak app - it should now successfully retrieve data through mitmproxy.

### Start Developing

You are now all set to start inspecting requests and responses. Go ahead and start developing!

## Troubleshooting

In case the app crashes, you can check the reason for it using the following command:

```bash
adb logcat -b crash
```

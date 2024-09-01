# Bank Cler Zak to CSV

Export Bank Cler Zak transactions to CSV format

## Usage

To export all your Bank Cler Zak transactions, run the following command on your machine:

```shell
# You can find the app_version from the Google Play store page from your Android device.
# Its a concatenated string containing the version and build number of the Bank Cler Zak
# app in the following format: 3.54.0.12168
python app.py --username=<zak-username> --password=<zak-password> --app-version=<app_version>
```

This will create a `Zak.csv` file in the project root containing all your transactions from Zak.
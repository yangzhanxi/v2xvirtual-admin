from services.license_management.v2x_license import LicenseFile

if __name__ == "__main__":
    f = LicenseFile()
    f.read()
    f.parse()
    print(f.licenses)

    licenses = [lic.to_json() for lic in f.licenses]
    print(licenses)

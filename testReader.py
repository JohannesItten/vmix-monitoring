import common.ConfigReader as ConfigReader


def main():
    r = ConfigReader.ConfigReader()
    # print(r.read_front('front.yaml'))
    print(r.read_vmixes_ws('vmixes.yaml'))


if __name__ == '__main__':
    main()

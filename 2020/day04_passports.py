import re


def parse_passports(lines):
    passports = []
    passport = {}
    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line == "":
            passports.append(passport)
            passport = {}
            continue

        details = cleaned_line.split(" ")
        for item in details:
            key, value = item.split(":")
            passport[key] = value

    passports.append(passport)
    return passports


def find_valid_passports(passports):
    valid_passports = []
    for passport in passports:
        if len(passport) == 8:
            valid_passports.append(passport)
            continue

        if len(passport) == 7 and "cid" not in passport.keys():
            valid_passports.append(passport)
            continue
    return valid_passports


def test_find_valid_passports():
    TEST_INPUT="""ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
    byr:1937 iyr:2017 cid:147 hgt:183cm

    iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
    hcl:#cfa07d byr:1929

    hcl:#ae17e1 iyr:2013
    eyr:2024
    ecl:brn pid:760753108 byr:1931
    hgt:179cm

    hcl:#cfa07d eyr:2025 pid:166559648
    iyr:2011 ecl:brn hgt:59in"""
    passports = parse_passports(TEST_INPUT.split("\n"))
    valid_passports = find_valid_passports(passports)

    assert len(valid_passports) == 2


def valid_year(passport, field, min_year, max_year):
    year = passport[field]
    try:
        year = int(year)
    except ValueError:
        return False
    if min_year <= year <= max_year:
        return True
    return False


def valid_height(passport):
    height = passport["hgt"]
    height_format_matches = re.match(r"[0-9]+(in|cm)", height)
    if not height_format_matches:
        return False

    measurement = int(height[:-2])
    if height.endswith("cm"):
        if 150 <= measurement <= 193:
            return True
    elif height.endswith("in"):
        if 59 <= measurement <= 76:
            return True
    return False

def find_valid_passports_part_2(passports):
    valid_passports = []
    for passport in passports:
        valid_fields = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
        if valid_fields.difference(passport.keys()):
            continue

        if not valid_year(passport, "byr", 1920, 2002):
            continue
        if not valid_year(passport, "iyr", 2010, 2020):
            continue
        if not valid_year(passport, "eyr", 2020, 2030):
            continue

        if not valid_height(passport):
            continue

        hair_color = passport["hcl"]
        valid_color = re.match(r"#[0-9a-f]{6}", hair_color)
        if not valid_color:
            continue

        eye_color = passport["ecl"].lower()
        valid_color = eye_color in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        if not valid_color:
            continue

        passport_id = passport["pid"]
        valid_passport_id = re.match(r"^[0-9]{9}$", passport_id)
        if not valid_passport_id:
            continue

        valid_passports.append(passport)

    return valid_passports


def test_find_valid_passports_part_2__all_valid():
    TEST_INPUT = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""
    passports = parse_passports(TEST_INPUT.split("\n"))

    valid_passports = find_valid_passports_part_2(passports)

    assert len(valid_passports) == 4


def test_find_valid_passports_part_2__not_valid():
    TEST_INPUT = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""
    passports = parse_passports(TEST_INPUT.split("\n"))

    valid_passports = find_valid_passports_part_2(passports)

    assert len(valid_passports) == 0


if __name__ == "__main__":
    with open("2020/data/day04_input.txt") as f:
        passports = parse_passports(f.readlines())

    valid_passports = find_valid_passports(passports)
    print(f"Number of valid passports is {len(valid_passports)}")


    valid_passports = find_valid_passports_part_2(passports)
    print(f"Number of valid passports for part two is {len(valid_passports)}")

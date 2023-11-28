from sql_app.persistence import get_settings

if __name__ == "__main__":
    s = get_settings("mapto")
    print(s)
    print({k: len(v) for k, v in s.items()})

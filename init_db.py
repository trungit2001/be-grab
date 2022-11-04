from app.database import Base, engine, metadata


def create_database():
    return Base.metadata.create_all(bind=engine)


def main():
    if metadata:
        print("[WARNING] Check the database exists. You may want to delete? (y/N):", end=' ')
        choose = input()
        if choose in ["y", "Y"]:
            metadata.drop_all()
            metadata.create_all()
            create_database()
            print("[INFO] Database created!")
        else:
            print("[INFO] Database exists, cannot be initialized!")


if __name__ == "__main__":
    main()
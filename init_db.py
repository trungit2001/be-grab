from app.database import engine, metadata
from app.services import create_database
from app.models import User, Post


def main():
    stmt = '''
        SELECT 
            schemaname as schema_name,
            relname as table_name, 
            n_live_tup as record_count 
        FROM pg_stat_user_tables WHERE n_live_tup > 0;
    '''
    conn = engine.connect()
    result = conn.execute(stmt).fetchall()
    conn.close()

    if result:
        print("[WARNING] Check the database exists data. You may want to delete? (Y/n):", end=' ')
        choose = input()
        if choose in ["y", "Y"]:
            metadata.drop_all(tables=[
                User.__table__,
                Post.__table__
            ])
            print("[INFO] Database deleted!")

            metadata.create_all()
            create_database()
            print("[INFO] Database initialized!")
        else:
            print("[INFO] Database exists, cannot be initialized!")
    else:
        create_database()
        print("[INFO] Database initialized!")


if __name__ == "__main__":
    main()
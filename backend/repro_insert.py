import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.repositories.order_repo import OrderRepository


def main():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, future=True)
    SessionLocal = sessionmaker(bind=engine, future=True)

    s = SessionLocal()
    repo = OrderRepository(s)
    try:
        with s.begin():
            o = repo.create(external_id='TEST-TRACE-123', customer_id=None)
            print('created', o.id)
    except Exception as e:
        print('EXC TYPE:', type(e))
        print('EXC:', e)
        print('\nFULL TRACEBACK:')
        traceback.print_exc()

        # Print SQLAlchemy/DB specific attributes if present
        if hasattr(e, 'orig'):
            print('\nEXCEPTION orig:')
            print(type(e.orig), repr(e.orig))
            try:
                traceback.print_exception(type(e.orig), e.orig, e.orig.__traceback__)
            except Exception:
                pass

        if hasattr(e, '__cause__') and e.__cause__:
            print('\nEXCEPTION __cause__:')
            print(type(e.__cause__), e.__cause__)
            try:
                traceback.print_exception(type(e.__cause__), e.__cause__, e.__cause__.__traceback__)
            except Exception:
                pass

        if hasattr(e, 'exceptions'):
            print('\nEXCEPTION GROUP MEMBERS:')
            for ex in getattr(e, 'exceptions', []):
                print(' -', type(ex), ex)
                try:
                    traceback.print_exception(type(ex), ex, ex.__traceback__)
                except Exception:
                    pass

    finally:
        s.close()


if __name__ == '__main__':
    main()

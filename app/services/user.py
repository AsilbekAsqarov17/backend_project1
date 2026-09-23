from psycopg import sql

#User Create function
def user_create(user, db):
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO users(username, email, age, is_active) " \
            "VALUES (%s, %s, %s, %s)",
            (user.username, user.email, user.age, user.is_active)
        )
        db.commit()
        return "User created Successfully!"
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()

#Get all Users function
def get_users(db):
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT * FROM users"
        )
        return cursor.fetchall()
    finally:
        cursor.close()


#Get User by ID
def get_user_by_id(user_id, db):
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT * FROM users " \
            "WHERE id = %s",(user_id,)
        )
        return cursor.fetchone()
    finally:
        cursor.close()


#Replace User 
def user_replace(user, user_id, db):
    cursor = db.cursor()

    try:
        cursor.execute(
            "UPDATE users " \
            "SET username=%s, email=%s, age=%s,is_active=%s "
            "WHERE id=%s",
            (user.username, user.email, user.age, user.is_active, user_id)
        )
        update_count = cursor.rowcount
        db.commit()
        return update_count
    except Exception as e:
        db.rollback()
        print(f"DEBUG UPDATE ERROR: {e}")
        return None
    finally:
        cursor.close()


#Update User 
def user_update(user_id, column_name, value, db):
    cursor = db.cursor()

    try:
        query = sql.SQL(
            "UPDATE users " \
            "SET {} = %s WHERE id=%s"
        ).format(sql.Identifier(column_name))

        cursor.execute(query,(value, user_id))
        update_count = cursor.rowcount
        db.commit()
        return update_count
    except Exception as e:
        db.rollback()
        print(f"DEBUG UPDATE ERROR: {e}")
        return None
    finally:
        cursor.close()


#Delete User
def user_delete(user_id, db):
    cursor = db.cursor()

    try:
        cursor.execute(
            "DELETE FROM users WHERE id = %s", (user_id,)
        )
        deleted_count = cursor.rowcount
        db.commit()
        return deleted_count
    except Exception as e:
        db.rollback()
        print(f"DEBUG UPDATE ERROR: {e}")
        return None
    finally:
        cursor.close()
from psycopg import sql

def task_create(task, db):
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO tasks(title, description, completed,priority,user_id) " \
            "VALUES (%s, %s,%s,%s, %s)",
            (task.title, task.description, task.completed, task.priority, task.user_id)
        )
        db.commit()
        return "Task created Successfully!"
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()

def get_tasks(filters, db):
    cursor = db.cursor()
    try:
        where_clauses = []
        params = []

        if filters.completed is not None:
            where_clauses.append(sql.SQL("completed = %s"))
            params.append(filters.completed)

        if filters.priority is not None:
            where_clauses.append(sql.SQL("priority = %s"))
            params.append(filters.priority)

        if filters.user_id is not None:
            where_clauses.append(sql.SQL("user_id = %s"))
            params.append(filters.user_id)

        where_stmt = sql.SQL("")
        if where_clauses:
            where_stmt = sql.SQL("WHERE ") + sql.SQL(" AND ").join(where_clauses)

        count_query = sql.SQL("SELECT COUNT(*) FROM tasks ") + where_stmt
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()[0]

        sort_column = filters.sort_by if filters.sort_by else "id"
        order_direction = sql.SQL("DESC") if filters.order.lower() == "desc" else sql.SQL("ASC")
        
        query_parts = [
            sql.SQL("SELECT * FROM tasks"),
            where_stmt,
            sql.SQL("ORDER BY {} {}").format(sql.Identifier(sort_column), order_direction),
            sql.SQL("LIMIT %s OFFSET %s")
        ]

        final_query = sql.SQL(" ").join(query_parts)
        
        paginated_params = params + [filters.limit, filters.skip]
        cursor.execute(final_query, paginated_params)
        tasks = cursor.fetchall()

        return tasks, total_count
    finally:
        cursor.close()

def task_get_by_id(task_id, db):
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT * FROM tasks WHERE id = %s", (task_id,)
        )
        return cursor.fetchone()
    finally:
        cursor.close()

def check_user_exists(user_id: int, db) -> bool:
    cursor = db.cursor()
    try:
        cursor.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
        return cursor.fetchone() is not None
    finally:
        cursor.close()

def task_get_by_userid(user_id, db):
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT * FROM tasks WHERE user_id = %s", (user_id,)
        )
        return cursor.fetchall()
    finally:
        cursor.close()

def task_replace(task_id:int,task, db):
    cursor = db.cursor()

    try:
        cursor.execute(
            "UPDATE tasks " \
            "SET title = %s, description = %s, completed = %s, priority = %s, user_id = %s"
            " WHERE id=%s",
            (task.title, task.description, task.completed, task.priority, task.user_id, task_id)
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

def task_update(task_id:int, column_name:str, value, db):
    cursor = db.cursor()

    try:
        query = sql.SQL(
            "UPDATE tasks " \
            "SET {} = %s WHERE id=%s"
        ).format(sql.Identifier(column_name))

        cursor.execute(query,(value, task_id))
        update_count = cursor.rowcount
        db.commit()
        return update_count
    except Exception as e:
        db.rollback()
        print(f"DEBUG UPDATE ERROR: {e}")
        return None
    finally:
        cursor.close()

def task_delete(task_id, db):
    cursor = db.cursor()

    try:
        cursor.execute(
            "DELETE FROM tasks WHERE id = %s", (task_id,)
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
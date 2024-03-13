from bottle import delete, get, post, put, request, redirect, static_file, template
import x
from icecream import ic
import time

##############################
@get("/favicon.ico")
def _():
    return static_file("favicon.ico", ".")

################################
@get("/")
def _():
    try:
        x.disable_cache()
        users = x.db({"query":"FOR user IN users RETURN user"})
        ic(users)
        return template("index.html", users=users["result"])
    except Exception as ex:
        ic(ex)
        return "system under maintainance"
    finally:
        pass

##############################
@get("/app.css")
def _():
    return static_file("app.css", ".")

##############################
@get("/mixhtml.js")
def _():
    return static_file("mixhtml.js", ".")

##############################
@post("/users")
def _():
    try:
        user_name = x.validate_user_name()
        last_name = request.forms.get("user_last_name")
        current_time_epoch = int(time.time())
        user = {
            "name": user_name,
            "last_name": last_name,
            "updated_at": current_time_epoch 
        }
        res = x.db({"query": "INSERT @doc IN users RETURN NEW", "bindVars": {"doc": user}})
        print(res)
        html = template("_user.html", user=res["result"][0])
        return f"""
        <template mix-target="#users" mix-top>
            {html}
        </template>
        """
    except Exception as ex:
        ic(ex)
        if "user_name" in str(ex):
            return f"""
            <template mix-target="#message">
                {ex.args[1]}
            </template>
            """            
    finally:
        pass

##############################
@delete("/users/<key>")
def _(key):
    try:
        ic(key)
        res = x.db({"query":"""
                    FOR user IN users
                    FILTER user._key == @key
                    REMOVE user IN users RETURN OLD""", 
                    "bindVars":{"key":key}})
        print(res)
        return f"""
        <template mix-target="[id='{key}']" mix-replace></template>
        """
    except Exception as ex:
        ic(ex)
    finally:
        pass

##############################
@post("/users/<key>/update")
def update_user(key):
    try:
        user_name = x.validate_user_name()
        last_name = request.forms.get("user_last_name")
        # Get the current time in epoch format
        current_time_epoch = int(time.time())
        user = {
            "name": user_name,
            "last_name": last_name,
            "updated_at": current_time_epoch  # Set updated_at to current time in epoch format
        }
        res = x.db({"query": "UPDATE @key WITH @doc IN users RETURN NEW", "bindVars": {"key": key, "doc": user}})
        print(res)
        return f"User {key} updated successfully"
    except Exception as ex:
        ic(ex)
        return "Failed to update user"
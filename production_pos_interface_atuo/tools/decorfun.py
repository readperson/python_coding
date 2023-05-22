from tools.logconfig.logingconfig import loging


def fun_info_name(fun_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            loging(fun_name.center(50, "*"))
            return func(*args, **kwargs)

        return wrapper

    return decorator

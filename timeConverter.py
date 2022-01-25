def time_converter(d):
    d = float(d)
    if d < 60:
        message = f"{round(d, 2)} секунд"
        return message
    elif d >= 60 and d <= 3600:
        d = d // 60
        if d == 1:
            return "минут"
        else:
            return f"{d} минут"
    elif d > 3600 and d <= 86400:
        hour = d // 3600
        c = d % 3600
        m = c // 60
        return f"{hour} цаг {m} минут"
    elif d > 86400:
        d = d // 86400
        return "{} өдөр".format(d)
def step(context):
    print("Test step executed")
    context.data["msg"] = "hello"
    return "next"
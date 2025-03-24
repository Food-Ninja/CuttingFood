from pattern.en import conjugate, PARTICIPLE


def get_fruit_part_question(food: str, part: str) -> str:
    return f"Is a(n) {part} an anatomical part of a(n) {food}?"


def get_cutting_position_question(verb: str) -> str:
    try:
        participle = conjugate(verb, tense=PARTICIPLE)
    except:
        participle = f"{verb}ing"
    return f"When {participle} a specific fruit or vegetable, where should the knife be placed - in the middle or at the end of the object?"


def get_cutting_tool_question(food: str) -> str:
    return f"When cutting a(n) {food}, what tool should be used?"


def get_peeling_tool_question(food: str) -> str:
    return f"When peeling a(n) {food}, what tool should be used?"


def get_prior_task_question(verb: str) -> str:
    try:
        participle = conjugate(verb, tense=PARTICIPLE)
    except:
        participle = f"{verb}ing"
    return f"When {participle} a specific fruit or vegetable, what other cutting task - if any - should be executed before?"


def get_repetitions_question(verb: str) -> str:
    try:
        participle = conjugate(verb, tense=PARTICIPLE)
    except:
        participle = f"{verb}ing"
    return f"When {participle} a specific fruit or vegetable, how many cuts need to be made - exactly one or more than one?"


def get_action_target_question(verb: str) -> str:
    try:
        participle = conjugate(verb, tense=PARTICIPLE)
    except:
        participle = f"{verb}ing"
    return f"When {participle} a specific fruit or vegetable, what is the target to perform the object on - the whole food or only a specific part?"

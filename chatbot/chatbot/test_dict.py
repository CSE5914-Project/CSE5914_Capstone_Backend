question_list = ["What language do you speak?",  "What genre would you like to watch?", "are you over 18?"]
robot_question = [{"questionCode": i, "questionString": q} for i,q in enumerate(question_list)]
print(robot_question)
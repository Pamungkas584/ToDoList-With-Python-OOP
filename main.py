import method
import class_todo

to = class_todo.ToDoList()

while True :
    method.welcome_menu()
    user_input = input("(1/2/3/4/5/6/7/8/9)> ")
    
    match user_input:
        case "1" : method.show_task(to)
        case "2" : method.add_task(to)
        case "3" : method.remove_task(to)
        case "4" : method.complete_task(to)
        case "5" : method.undo(to)
        case "6" : method.redo(to)
        case "7" : method.reminder(to)
        case "8" : method.show_complete_task(to)
        case "9" : break
        case _:print("Option tidak tersedia")
    
    input("")
    